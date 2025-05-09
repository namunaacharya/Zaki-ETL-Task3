import psycopg2
from pyspark.sql import SparkSession

def load_import(rate_path,provider_path):
    spark = SparkSession.builder .appName("Postgres").config("spark.jars","/home/namuna-acharya/spark/jars/postgresql-42.6.0.jar").getOrCreate()
    
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
   
    provider_ref = """
    CREATE TABLE IF NOT EXISTS provider_ref(
        provider_group_id INT,
        npi BIGINT,
        tin_type SMALLINT,
        tin TEXT
    );
    """
    cursor.execute(provider_ref)
    connection.commit()

    network= """
    CREATE TABLE IF NOT EXISTS network(
        billing_code TEXT,
        billing_code_type TEXT,
        negotiation_arrangement TEXT,    
        provider_group_id INT,     
        billing_class TEXT,
        billing_code_modifier TEXT[],
        negotiated_rate DOUBLE PRECISION,    
        negotiated_type TEXT,
        service_code INTEGER[]
    );
    """
    cursor.execute(network)
    connection.commit()

    network_data = spark.read.parquet(rate_path)
    provider_data = spark.read.parquet(provider_path)
    
    provider_data.show(5)   
    network_data.show(5)

    provider_data.write.jdbc(url=jdbc_url,table="provider_ref",mode="append", properties=jdbc_properties)
    network_data.write.jdbc(url=jdbc_url,table="network",mode="append", properties=jdbc_properties)

    cursor.close()
    connection.close()