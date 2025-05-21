import gzip
import json
import os

def extract_import(input, logger):
    logger.info("Starting extract process")

    output_path = os.path.join(os.getcwd(), 'output_files')
    os.makedirs(output_path, exist_ok=True)

    nrpr_file = os.path.join(output_path, 'nrpr.json')

    for files in os.listdir(input):
        if files.endswith('.json.gz'):
            file_path = os.path.join(input, files)
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                        item = json.load(f)
                        with open(nrpr_file, 'w', encoding='utf-8') as nrpr:
                            json.dump(item, nrpr)

    logger.info("File extracted successfully")
    return nrpr_file

