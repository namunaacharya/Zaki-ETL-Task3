import argparse
import logging
from etl import ETL
from api import as_sort, des_sort

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
    logger = logging.getLogger("Logger")

    parser = argparse.ArgumentParser(description="ETL processing or API planet sorting")
    parser.add_argument('--zip_path', help='ZIP file path for ETL')
    parser.add_argument('--apiA',action='store_true', help="Enter 'apiA' or 'apiD' for planet sorting")
    parser.add_argument('--apiD',action='store_true', help="Enter 'apiA' or 'apiD' for planet sorting")

    args = parser.parse_args()

    if args.zip_path:
        etl = ETL()
        etl.execute(args,logger)
    elif args.apiA:
        as_sort(logger)
    elif args.apiD:
        des_sort(logger)
    else:
        logger.info("Either --zip_path for ETL process or --apiA, --apiD for planet sorting")

if __name__ == "__main__":
    main()