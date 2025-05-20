import zipfile
import gzip
import ijson
import json
import os
from io import BytesIO
from decimal import Decimal

def extract_import(zip_path,prov_path, logger):
    logger.info("Starting extract process")

    def con_decimal(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    output_path = os.path.join(os.getcwd(), 'output_files')
    os.makedirs(output_path, exist_ok=True)

    nrpr_path = os.path.join(output_path, 'nrpr.json')
    pro_path =  os.path.join(output_path, 'provider_details')

    with zipfile.ZipFile(zip_path, 'r') as outer_zip:
        for name in outer_zip.namelist():
            if name.endswith('.json.gz'):
                with outer_zip.open(name) as new_file:
                    with gzip.open(BytesIO(new_file.read()), 'rt', encoding='utf-8') as f:
                        with open(nrpr_path, 'w') as nrpr_file:
                            for item in ijson.items(f, 'in_network.item'):
                                nrpr_file.write(json.dumps(item, default=con_decimal) + '\n')

    with zipfile.ZipFile(prov_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.endswith('.parquet'):
                with z.open(file_name) as parquet_file:
                    with open(pro_path, 'wb') as f_out:
                        f_out.write(parquet_file.read())

    logger.info("File extracted successfully")
    return nrpr_path,pro_path