import argparse
import logging
from etl import ETL
from api import API

def main():
    parser = argparse.ArgumentParser(description="ETL processing using ZIP file.")
    parser.add_argument("--zip_path", required=True, help="ZIP file path")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
    logger = logging.getLogger("ETLLogger")
    etl = ETL()
    etl.execute(args,logger)

if __name__ == "__main__":
    main()



