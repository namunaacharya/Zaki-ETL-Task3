import argparse
import logging
from etl_nrpr import ETL

def main():
    logging.basicConfig(filename="ETLnrpr.log",encoding='utf-8',level=logging.INFO,
                        format='%(asctime)s : %(message)s')
    logger = logging.getLogger("Logger")

    parser = argparse.ArgumentParser(description="ETL processing.")
    parser.add_argument('--zip', required=True, help='ZIP file path for ETL')
    parser.add_argument('--prov', required=True, help='Provider detail zipfile path')
    parser.add_argument('--bill', required=True, help='Billing detail zipfile path')

    args = parser.parse_args()

    etl = ETL()
    etl.execute(args,logger)

if __name__ == "__main__":
    main()