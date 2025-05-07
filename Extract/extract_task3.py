import ijson
import pandas as pd

rate = []
provider = []

with open('files/MagnaCarePPO_In-Network.json','r') as f:
    for item in ijson.items(f, 'in_network.item'):
        rate.append(item)

    f.seek(0)

    for data in ijson.items(f, 'provider_references.item'):
        provider.append(data)

rate_df = pd.DataFrame(rate)
provider_df = pd.DataFrame(provider)

print(rate_df)
print(provider_df)

rate_df.to_json('files/rate.json',orient='records',indent=3)
provider_df.to_json('files/provider.json',orient='records',indent=3)

rate_df.to_parquet('files/rate.parquet',index=False)
provider_df.to_parquet('files/provider.parquet',index=False)

