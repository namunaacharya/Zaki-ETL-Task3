from pyspark.sql.functions import explode,col,expr,when,array,concat_ws
from pyspark.sql.types import ArrayType, IntegerType, ShortType, LongType

def scrub_import(in_path,prov_path,pro_path,etl,logger):
    logger.info("Starting transform process")

    spark = etl.spark

    rate_file = spark.read.json(in_path)
    provider_file = spark.read.json(prov_path)
    p_file = spark.read.json(pro_path)

    rate_file.printSchema()
    provider_file.printSchema()

    # Flatten provider file
    provider_flat = (provider_file.selectExpr("provider_group_id", "explode(provider_groups) as provider")  
    .selectExpr("*", "explode(provider.npi) as provider_npi") 
    .selectExpr(
        "provider_group_id",
        "provider_npi as npi",
        "provider.tin.type as tin_type",
        "provider.tin.value as tin"
    ))

    provider_replaced = provider_flat.withColumn("tin_type",
                        when(col("tin_type") == "ein", 1)
                        .when(col("tin_type") == "npi", 2))
    provider_cleaned = provider_replaced.withColumn('tin', expr("REPLACE(tin, '-', '')"))
    provider_prov = provider_cleaned.withColumn("provider_group_id", col("provider_group_id").cast(IntegerType()))
    provider_cast = provider_prov.withColumn("tin_type", col("tin_type").cast(ShortType())) \
                            .withColumn("tin", col("tin").cast(LongType()))

    #New provider file
    p_loc = p_file.selectExpr("*", "loc.lat as lat", "loc.lon as lon") \
              .drop("loc")

    p_merge = p_loc.withColumn("provider_full_name", concat_ws(" ","provider_first_name", "provider_middle_name","provider_last_name")) \
        .withColumn("prv_taxonomy",array("prv_taxonomy_1_code", "prv_taxonomy_2_code", "prv_taxonomy_3_code")) \
        .withColumn("prv_specialty",array("prv_specialty_1_desc", "prv_specialty_2_desc", "prv_specialty_3_desc"))

    p_drop = p_merge.drop("prv_fax","prv_type_desc","provider_first_name","provider_last_name","provider_middle_name","provider_name_prefix_text",
                        ("prv_taxonomy_1_code"),("prv_taxonomy_2_code"),("prv_taxonomy_3_code"),("prv_specialty_1_desc"),("prv_specialty_2_desc"),("prv_specialty_3_desc"))

    p_cleaned = p_drop.withColumn("prv_taxonomy",expr("filter(prv_taxonomy, x -> x IS NOT NULL AND x != '')")) \
        .withColumn("prv_specialty",expr("filter(prv_specialty, x -> x IS NOT NULL AND x != '')"))

    p_map = p_cleaned.withColumn("prv_type_code",
                            when(col("prv_type_code") == "P", 1)
                            .when(col("prv_type_code") == "F", 2))

    p_cast = p_map.withColumn("prv_type_code", col("prv_type_code").cast(ShortType())) \
                .withColumn("npi", col("npi").cast(LongType()))
    
    #Join two provider table
    
    n_provider_table = provider_cast.join(p_cast,on ="npi",how= "inner")

    excluded_npi = provider_cast.join(p_cast,on="npi",how="left_anti")

    # Flatten rate file
    rate_df = rate_file.withColumn("rates", explode("negotiated_rates"))
    id_df = rate_df.withColumn("provider_group_id",explode("rates.provider_references"))
    price_df = id_df.withColumn("prices",explode("rates.negotiated_prices"))

    rate_flat = price_df.selectExpr(
        "billing_code",
        "billing_code_type",
        "negotiation_arrangement",
        "provider_group_id",    
        "prices.billing_class as billing_class",
        "prices.billing_code_modifier as billing_code_modifier",
        "prices.negotiated_rate as negotiated_rate",
        "prices.negotiated_type as negotiated_type",
        "prices.service_code as service_code"
    )
 
    rate_filtered = rate_flat.filter(rate_flat.billing_code.isNotNull() & (rate_flat.billing_code != ""))

    rate_prov = rate_filtered.withColumn("provider_group_id", col("provider_group_id").cast(IntegerType()))
    rate_cast = rate_prov.withColumn("service_code",col("service_code").cast(ArrayType(IntegerType())))
   
    rate_cast.printSchema()   
    n_provider_table.printSchema()
    
    rate_path = "output_file/rate_table.parquet"
    provider_path = "output_file/provider_table.parquet"
    excluded_path ="output_file/excluded.csv"

    rate_cast.write.mode("overwrite").parquet(rate_path)
    n_provider_table.write.mode("overwrite").parquet(provider_path)
    excluded_npi.write.mode("overwrite").option("header", "true").option("delimiter", ",").csv(excluded_path)

    return rate_path,provider_path
