import psycopg2
from pyspark.sql import SparkSession

def load_import(rate_path,provider_path):
    spark = SparkSession.builder .appName("Postgres") .config("spark.jars", "/home/namuna-acharya/jars/postgresql-42.5.6.jar") .getOrCreate()

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
    CREATE TABLE IF NOT EXISTS provider(
        provider_group_id INT,
        npi BIGINT,
        tin_type SMALLINT,
        tin TEXT
    );
    """

    cursor.execute(provider_table)
    connection.commit()

    in_network_table= """
    CREATE TABLE IF NOT EXISTS in_network(
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
    cursor.execute(in_network_table)
    connection.commit()

    in_network = spark.read.parquet(rate_path)
    provider = spark.read.parquet(provider_path)

    in_network.write.jdbc(url=jdbc_url,table="in_network_table",mode="append", properties=jdbc_properties)
    provider.write.jdbc(url=jdbc_url,table="provider_table",mode="append", properties=jdbc_properties)

    cursor.close()
    connection.close()
