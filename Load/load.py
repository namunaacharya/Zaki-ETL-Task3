import psycopg2

def load_import(rate_path,provider_path,etl,logger):
    logger.info("Starting load process")
    
    spark = etl.spark
    port = etl.port
    host = etl.host
    user = etl.user
    database = etl.database
    password = etl.password

    jdbc_url = f"jdbc:postgresql://{host}:{port}/{database}"
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

    cursor.execute("DROP TABLE IF EXISTS provider_table;")
    cursor.execute("DROP TABLE IF EXISTS rate_table;")
   
    provider_table = """
    CREATE TABLE provider_table(
        provider_group_id INT,
        npi BIGINT,
        tin_type SMALLINT,
        tin BIGINT,
        prv_city VARCHAR(255),
        prv_phone VARCHAR(15),
        prv_state CHAR(2),
        prv_street_1 VARCHAR(255),
        prv_type_code INT,
        prv_zip VARCHAR(10),
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        provider_full_name VARCHAR(255),
        prv_taxonomy TEXT[],
        prv_specialty TEXT[]
    );
    """

    cursor.execute(provider_table)
    connection.commit()

    rate_table= """
    CREATE TABLE rate_table(
        billing_code VARCHAR(10),
        billing_code_type VARCHAR(10),
        negotiation_arrangement VARCHAR(5),    
        provider_group_id INT,     
        billing_class VARCHAR(15),
        billing_code_modifier TEXT[],
        negotiated_rate DOUBLE PRECISION,    
        negotiated_type VARCHAR(12),
        service_code INTEGER[]
    );
    """
    cursor.execute(rate_table)
    connection.commit()

    network_data = spark.read.parquet(rate_path)
    provider_data = spark.read.parquet(provider_path)
    
    provider_data.show(5)   
    network_data.show(5)

    provider_data.write.jdbc(url=jdbc_url,table="provider_table",mode="append", properties=jdbc_properties)
    network_data.write.jdbc(url=jdbc_url,table="rate_table",mode="append", properties=jdbc_properties)

    cursor.close()
    connection.close()