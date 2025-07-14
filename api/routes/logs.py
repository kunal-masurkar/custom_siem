"""Logs route for Custom SIEM API."""
from flask import Blueprint, request, jsonify
from api.elasticsearch_client import get_es_client
from typing import Any
from marshmallow import Schema, fields, ValidationError

logs_bp = Blueprint('logs', __name__)

class SearchLogsSchema(Schema):
    q = fields.Str(required=False)

@logs_bp.route('/logs/search', methods=['GET'])
def search_logs() -> Any:
    """Search logs in Elasticsearch with optional query string."""
    schema = SearchLogsSchema()
    try:
        args = schema.load(request.args)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    query = args.get('q', '')
    es = get_es_client()
    body = {
        "query": {
            "query_string": {
                "query": query if query else "*"
            }
        }
    }
    try:
        res = es.search(index="logs-*", body=body, size=50)
        hits = res['hits']['hits']
        results = [hit['_source'] for hit in hits]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"results": results, "query": query}) 
