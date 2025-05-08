import sys
from Extract import extract
from Scrub import scrub
from Load import load

def main():
    zip_path = sys.argv[1]

    extract_path = extract.extract_import(zip_path)
    scrub_path = scrub.scrub_import(extract_path)
    load.load_import(scrub_path)

if __name__ == "__main__":
    main()
