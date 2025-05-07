import psycopg2
from pyspark.sql import SparkSession

spark = SparkSession.builder .appName("Postgres") .config("spark.jars", "/home/namuna-acharya/jars/postgresql-42.5.6.jar") .getOrCreate()
spark

port = 5432
database = "postgres"
host = "localhost"
user = "postgres"
password = "sql123"

jdbc_url = "jdbc:postgresql://localhost:5432/postgres"
jdbc_properties = {
    "user": user,
    "password": password,
    "driver": "org.postgresql.Driver"
}

connection = psycopg2.connect(
    host= host,   
    dbname = database,
    user= user,        
    password=password,
    port= port)

cursor = connection.cursor()

provider_table = """
CREATE TABLE IF NOT EXISTS provider_table(
    provider_group_id BIGINT,
    npi BIGINT,
    tin_type SMALLINT,
    tin TEXT
);
"""

cursor.execute(provider_table)
connection.commit()

in_network_table= """
CREATE TABLE IF NOT EXISTS in_network_table(
    billing_code TEXT,
    billing_code_type TEXT,
    negotiation_arrangement TEXT,    
    provider_group_id BIGINT,     
    billing_class TEXT,
    billing_code_modifier TEXT[],
    negotiated_rate DOUBLE PRECISION,    
    negotiated_type TEXT,
    service_code INTEGER[]
);
"""
cursor.execute(in_network_table)
connection.commit()

provider = spark.read.parquet("files/provider_data.parquet")
in_network = spark.read.parquet("files/rate_data.parquet")

provider.write.jdbc(url=jdbc_url,table="provider_table",mode="append", properties=jdbc_properties)
in_network.write.jdbc(url=jdbc_url,table="in_network_table",mode="append", properties=jdbc_properties)

cursor.close()
connection.close()

