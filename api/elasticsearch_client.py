"""Elasticsearch client utility for Custom SIEM API."""
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT', '9200')
ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER')
ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')


def get_es_client() -> 'Elasticsearch':
    """Create and return an Elasticsearch client using environment variables."""
    if ELASTICSEARCH_USER and ELASTICSEARCH_PASSWORD:
        es = Elasticsearch(
            hosts=[{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}],
            http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
            scheme="http"
        )
    else:
        es = Elasticsearch(
            hosts=[{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}],
            scheme="http"
        )
    return es 
