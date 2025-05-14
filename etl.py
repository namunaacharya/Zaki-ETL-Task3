import yaml
import argparse
from Extract import extract
from Scrub import scrub
from Load import load
from pyspark.sql import SparkSession

class ETL:
    def __init__(self):

        with open('container.yml','r') as file:
            sp = yaml.safe_load(file)

        self.cores = sp['SPARK']['EXECUTOR']['CORES']
        self.instances = sp['SPARK']['EXECUTOR']['INSTANCES']
        self.executor_memory = sp['SPARK']['EXECUTOR']['MEMORY']
        self.driver_memory = sp['SPARK']['DRIVER']['MEMORY']

        self.port = sp['POSTGRES']['PORT']
        self.host = sp['POSTGRES']['HOST']
        self.user = sp['POSTGRES']['USER']
        self.database = sp['POSTGRES']['DATABASE']
        self.password = sp['POSTGRES']['PASSWORD']

        self.spark = SparkSession.builder.appName("etl").config("spark.driver.memory", self.driver_memory).getOrCreate()
        
    def execute(self,logger):
            parser = argparse.ArgumentParser(description="ETL processing using ZIP file.")
            parser.add_argument("--zip_path", required=True, help="ZIP file path")

            args = parser.parse_args()

            in_path, prov_path = extract.extract_import(args.zip_path,logger)
            rate_path, provider_path = scrub.scrub_import(in_path, prov_path,self,logger)
            load.load_import(rate_path, provider_path, self,logger) 



        

    

        

    
