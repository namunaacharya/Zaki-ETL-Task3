import zipfile
import gzip
import ijson
import json
import os
from io import BytesIO
from decimal import Decimal

def extract_import(zip, logger):
    logger.info("Starting extract process")

    def con_decimal(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    output_path = os.path.join(os.getcwd(), 'output_files')
    os.makedirs(output_path, exist_ok=True)

    nrpr_path = os.path.join(output_path, 'nrpr.json')

    with zipfile.ZipFile(zip, 'r') as outer_zip:
        for name in outer_zip.namelist():
            if name.endswith('.json.gz'):
                with outer_zip.open(name) as new_file:
                    with gzip.open(BytesIO(new_file.read()), 'rt', encoding='utf-8') as f:
                        with open(nrpr_path, 'w') as nrpr_file:
                            for item in ijson.items(f, 'in_network.item'):
                                nrpr_file.write(json.dumps(item, default=con_decimal) + '\n')

    logger.info("File extracted successfully")
    return nrpr_path