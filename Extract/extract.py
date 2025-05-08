def extract_import():
        import zipfile
        import ijson
        import json
        from decimal import Decimal

        def con_decimal(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        zip = "/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/MagnaCarePPO_In-Network.zip"

        with open('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/network_file.json','w') as in_file, \
            open('/home/namuna-acharya/Desktop/zakipoint/Zaki-ETL-Task3/files/provider_file.json','w') as prov_file:
 
             with zipfile.ZipFile(zip, 'r') as file:
                for data in file.namelist():
                    with file.open(data, 'r') as f:
                        for item in ijson.items(f, 'in_network.item'):
                            in_file.write(json.dumps(item, default=con_decimal) + '\n')

                        f.seek(0)

                        for item in ijson.items(f, 'provider_references.item'):
                            prov_file.write(json.dumps(item, default=con_decimal) + '\n')
                    

if __name__ == "__main__":
        extract_import()

