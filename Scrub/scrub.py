def scrub_import():
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.appName('python').config("spark.driver.memory", "4g").getOrCreate()
        spark

        rate_file = spark.read.option('multiline','True').json('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/network_file.json')
        provider_file = spark.read.option('multiline','True').json('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/provider_file.json')

        rate_file.printSchema()

        provider_file.printSchema()

