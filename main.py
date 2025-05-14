import logging
from etl import ETL

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
    logger = logging.getLogger("ETLLogger")
    etl = ETL()
    etl.execute(logger)

if __name__ == "__main__":
    main()



