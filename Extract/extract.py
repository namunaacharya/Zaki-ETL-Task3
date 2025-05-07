import zipfile
import ijson
import json
from decimal import Decimal

def con_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
zip_files = [
   "/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/MagnaCarePPO_In-Network.zip",
   "/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/MagnaCarePPO_In-Network1.zip"
]

prov_item=[]

with open('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/in_network_file.json','w') as in_file:
    for z in zip_files:
        with zipfile.ZipFile(z, 'r') as file:
            for data in file.namelist():
                with file.open(data, 'r') as f:
                    for item in ijson.items(f, 'in_network.item'):
                        in_file.write(json.dumps(item, default=con_decimal) + '\n')

                with file.open(data, 'r') as f:
                    for item in ijson.items(f, 'provider_references.item'):
                        prov_item.append(item)
                    
with open('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/provider_file.json','w') as prov_file:
    prov_file.write(json.dumps(prov_item,default=con_decimal) + '\n')



