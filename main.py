import sys
from Extract import extract
from Scrub import scrub
from Load import load

def main():
    zip_path = sys.argv[1]

    in_path,prov_path = extract.extract_import(zip_path)
    rate_path,provider_path = scrub.scrub_import(in_path,prov_path)
    load.load_import(rate_path,provider_path)

if __name__ == "__main__":
    main()
