"""Rules route for Custom SIEM API."""
from flask import Blueprint, request, jsonify
from typing import List, Dict, Any

rules_bp = Blueprint('rules', __name__)

# In-memory rules store (for demo)
rules: List[Dict] = []

@rules_bp.route('/rules', methods=['GET'])
def list_rules() -> Any:
    """List all correlation rules."""
    return jsonify({"rules": rules})

@rules_bp.route('/rules', methods=['POST'])
def add_rule() -> Any:
    """Add a new correlation rule."""
    rule = request.json
    rules.append(rule)
    return jsonify({"message": "Rule added", "rule": rule}), 201

# Example: Evaluate rules on a log event (to be called from log ingestion or search)
def evaluate_rules(log_event):
    matched = []
    for rule in rules:
        # Simple example: match if all key-value pairs in rule['conditions'] are in log_event
        if all(log_event.get(k) == v for k, v in rule.get('conditions', {}).items()):
            matched.append(rule)
    return matched 
