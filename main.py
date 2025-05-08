from Extract.extract import extract_import
from Scrub.scrub import scrub_import
from Load.load import load_import

def main():
    extract_import()
    scrub_import()
    load_import()

if __name__ == "__main__":
    main()