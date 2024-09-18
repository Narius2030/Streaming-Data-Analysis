import sys
sys.path.append('./')

import json
import polars as pl
import glob
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError, NotFoundError

def create_documents(path:str="./logs/*.json"):
    documents = []
    for path in glob.glob(path):
        with open(path, 'r') as file:
            resp = json.load(file)
            rows = resp['data']
            _type = resp['type']
            for row in rows:
                # _id = { "index": { "_index": index, "_id": row['id']}}
                for key, val in row.items():
                    if (key in ['first_air_date', 'release_date']) and (val == ""):
                        row[key] = "2024-01-01"
                    elif (val == ""):
                        row[key] = "N/A"
                row['type'] = _type
                documents.append(row)
    return documents


def ingest_data(es, index:str, documents:list):
    # es.bulk(operations=datarows, pipeline="ent-search-generic-ingestion")
    try:
        for row in documents:
            _id = row['id']
            es.index(index=index, id=_id, document=row)
    except BadRequestError as exc:
        raise Exception(str(exc))
        

def delete_documents(es, index:str, num_docs:int):
    resp = es.search(index=index, body={"size": num_docs})
    documents = resp['hits']['hits']
    for doc in documents:
        try:
            _id = doc['_id']
            es.delete(index=index, id=str(_id))
        except Exception as exc:
            print(str(exc))


if __name__=='__main__':
    documents = create_documents(index='films')
    print(len(documents))

    es = Elasticsearch(
        hosts="https://1bb948ea706f49129cedb435f9951d06.asia-southeast1.gcp.elastic-cloud.com:443",
        api_key="MkUwbEE1SUJDQlJXa2FMWmhJODQ6ZzRLeHg0U3BUTS1PVlhYYWNrWmRUUQ==",
    )
    
    # ingest_data(es, "films", documents)
    # delete_documents(es, "films", len(documents))
    