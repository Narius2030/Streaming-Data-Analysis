import sys
sys.path.append('./')

import json
import glob
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError
from core.config import get_settings


class ElasticHandlers(Elasticsearch):
    def __init__(self, api_key:str, host:str) -> None:
        self.es = Elasticsearch(api_key=api_key, hosts=host)
    
    def create_documents(self, filepathes:str, index:str):
        documents = []
        for path in filepathes:
            with open(path, 'r') as file:
                resp = json.load(file)
                rows = resp['data']
                _type = resp['type']
                for row in rows:
                    for key, val in row.items():
                        if (key in ['first_air_date', 'release_date']) and (val == ""):
                            row[key] = "2024-01-01"
                        elif (val == ""):
                            row[key] = "N/A"
                    row['type'] = _type
                    documents.append(row)
                    # _id = { "index": { "_index": "films", "_id": row['id']}}
                    # documents += [_id, row]
        return documents

    def ingest_data(self, documents:list, string_id:str, updatable_fields:list, index:str=None, pipeline:str="ent-search-generic-ingestion"):
        try:
            for row in documents:
                doc = {}
                _id = row[string_id]
                for field in updatable_fields:
                    doc[field] = row[field]
                self.es.update(index=index, 
                               id=_id, 
                               doc=doc, 
                               upsert=row,
                               doc_as_upsert=True)
            # self.es.bulk(operations=documents, pipeline=pipeline)
            print("Data was ingested successfully to Elasticsearch ✔")
        except Exception as exc:
            raise BadRequestError(str(exc) + '❌')
            
    def delete_documents(self, index:str, num_docs:int):
        resp = self.es.search(index=index, body={"size": num_docs})
        documents = resp['hits']['hits']
        for doc in documents:
            try:
                _id = doc['_id']
                self.es.delete(index=index, id=str(_id))
            except Exception as exc:
                raise BadRequestError(str(exc) + '❌')


if __name__=='__main__':
    settings = get_settings()
    
    handler = ElasticHandlers(
        host=settings.ELASTIC_HOST,
        api_key=settings.TMDB_INDEX_KEY,
    )
    documents = handler.create_documents(index="tmdb-index", path="./logs/*.json")
    # handler.ingest_data(documents, index="tmdb-index")
    # handler.delete_documents("films", len(documents))
    