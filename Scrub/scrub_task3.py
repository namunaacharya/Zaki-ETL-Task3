from pyspark.sql import SparkSession
from pyspark.sql.functions import explode,col,expr,when
from pyspark.sql.types import ArrayType, IntegerType, ShortType

spark = SparkSession.builder.appName('ETL').config("spark.driver.memory", "4g").getOrCreate()
spark

rate_file = spark.read.option('multiline','True').json('files/rate.json')
provider_file = spark.read.option('multiline','True').json('files/provider.json')


# Flatten provider file
provider_file.printSchema()

provider_df = provider_file.withColumn("provider", explode("provider_groups"))
provider_npi = provider_df.withColumn("provider_npi", explode("provider.npi"))

provider_flat = provider_npi.select(
    "provider_group_id",
    col("provider_npi").alias("npi"),
    col("provider.tin.type").alias("tin_type"),
    col("provider.tin.value").alias("tin")
)

provider_flat.show(truncate=False)

# Flatten rate file
rate_file.printSchema()

rate_df = rate_file.withColumn("rates", explode("negotiated_rates"))
id_df = rate_df.withColumn("provider_group_id",explode("rates.provider_references"))
price_df = id_df.withColumn("prices",explode("rates.negotiated_prices"))

rate_flat = price_df.select(
    "billing_code",
    "billing_code_type",
    "negotiation_arrangement",
    col("provider_group_id").alias("provider_group_id"),    
    col("prices.billing_class").alias("billing_class"),
    col("prices.billing_code_modifier").alias("billing_code_modifier"),
    col("prices.negotiated_rate").alias("negotiated_rate"),
    col("prices.negotiated_type").alias("negotiated_type"),
    col("prices.service_code").alias("service_code")
)
rate_flat.show()

rate_flat.printSchema()


# Cleaning rate file

rate_filtered = rate_flat.filter(rate_flat.billing_code.isNotNull() & (rate_flat.billing_code != ""))
rate_filtered.show()


#  Verify null
rate_filtered.filter(rate_filtered.billing_code_modifier.isNotNull()).count()


# Cleaning provider file
provider_flat.show()
provider_replaced = provider_flat.withColumn("tin_type",
                    when(col("tin_type") == "ein", 1)
                    .when(col("tin_type") == "npi", 2))
provider_cleaned = provider_replaced.withColumn('tin', expr("REPLACE(tin, '-', '')"))
provider_cleaned.show()
provider_cleaned.printSchema()


# Cast the datatype of tin type to small integer
provider_cast = provider_cleaned.withColumn("tin_type", col("tin_type").cast(ShortType()))
provider_cast.printSchema()

rate_filtered.printSchema()


# Cast the datatype of service code to array of integer
rate_cast = rate_filtered.withColumn("service_code",col("service_code").cast(ArrayType(IntegerType())))
rate_cast.printSchema()

rate_cast.write.parquet("files/rate_data.parquet")
provider_cast.write.parquet("files/provider_data.parquet")

