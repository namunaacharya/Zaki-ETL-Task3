import argparse
import logging
from etl import ETL

def main():
    logging.basicConfig(filename="ETLprocess.log",encoding='utf-8',level=logging.INFO,
                        format='%(asctime)s : %(message)s')
    logger = logging.getLogger("Logger")

    parser = argparse.ArgumentParser(description="ETL processing using zip file.")
    parser.add_argument('--zip_path', help='ZIP file path for ETL')

    args = parser.parse_args()

    etl = ETL()
    etl.execute(args,logger)

if __name__ == "__main__":
    main()