from elasticsearch import Elasticsearch

client = Elasticsearch(
  hosts="https://1bb948ea706f49129cedb435f9951d06.asia-southeast1.gcp.elastic-cloud.com:443",
  api_key="YUUyMC1KRUJDQlJXa2FMWlVZNDk6UHMtZmRUQ3NUQmkyZzBZT2twUmV4dw==",
  # ca_certs="./http_ca.crt",
  # verify_certs=True
)

# API key should have cluster monitor rights
client.info()

documents = [
  { "index": { "_index": "supermarket-sales", "_id": "9780553351927"}},
  {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "supermarket-sales", "_id": "9780441017225"}},
  {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "supermarket-sales", "_id": "9780451524935"}},
  {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "supermarket-sales", "_id": "9781451673319"}},
  {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "supermarket-sales", "_id": "9780060850524"}},
  {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
  { "index": { "_index": "supermarket-sales", "_id": "9780385490818"}},
  {"name": "The Handmaid's Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311, "_extract_binary_content": True, "_reduce_whitespace": True, "_run_ml_inference": True},
]

client.bulk(operations=documents, pipeline="ent-search-generic-ingestion")