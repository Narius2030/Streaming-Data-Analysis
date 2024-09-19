import json
from core.config import get_settings
import pandas as pd
import glob


settings = get_settings()    

def create_documents():
    documents = []
    for path in glob.glob('./logs/*.json'):
        with open(path, "r", encoding="utf-8") as file:
            resp = json.load(file)
            rows = resp['data']
            _type = resp['type']
            _page = resp['page']
            for row in rows:
                for key, val in row.items():
                    if (key in ['first_air_date', 'release_date']) and (val == ""):
                        row[key] = "2024-01-01"
                    elif (val == ""):
                        row[key] = "N/A"
                row['type'] = _type
                row['page'] = _page
                documents.append(row)
    return documents


if __name__ == "__main__":
    documents = create_documents()
    # print(documents[:5])
    
    df = pd.DataFrame(documents)
    print(df.loc[0])
