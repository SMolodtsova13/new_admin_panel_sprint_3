from elasticsearch import Elasticsearch, helpers
from typing import List



class ElasticsearchLoader:
    def __init__(self, es_client: Elasticsearch, index_name: str):
        self.es = es_client
        self.index = index_name

    def bulk_upload(self, docs: List[dict]) -> None:
        actions = [
            {
                "_index": self.index,
                "_id": doc['id'],
                "_source": doc
            }
            for doc in docs
        ]
        helpers.bulk(self.es, actions)
