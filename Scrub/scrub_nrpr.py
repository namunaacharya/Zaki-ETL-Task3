
def scrub_import(nrpr_path,prov,bill,etl,logger):
    logger.info("Starting transform process")

    spark = etl.spark

    nrpr_file = spark.read.json(nrpr_path)
    pro_file = spark.read.parquet(prov)

    nrpr_file.printSchema()
    pro_file.printSchema()

    pro_file.show()
