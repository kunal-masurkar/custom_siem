"""Main Flask app for Custom SIEM API."""
from flask import Flask, jsonify, request
from api.routes.logs import logs_bp
from api.routes.rules import rules_bp
from api.routes.alerting import alerting_bp
from api.routes.export import export_bp
from typing import Any

app = Flask(__name__)

API_KEY = "changeme123"  # In production, load from env or config

def require_api_key(view_func):
    """Decorator to require API key for protected endpoints."""
    def wrapper(*args, **kwargs):
        if request.endpoint in ("index", "health"):
            return view_func(*args, **kwargs)
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

@app.route('/')
@require_api_key
def index() -> Any:
    """Root endpoint for API status."""
    return jsonify({"message": "Custom SIEM API is running."})

@app.route('/health')
def health() -> Any:
    """Health check endpoint."""
    return jsonify({"status": "ok"})

# Register blueprints with API key protection
def protect_blueprint(bp):
    for rule in bp.url_map.iter_rules():
        endpoint = rule.endpoint.split(".")[-1]
        view_func = bp.view_functions[endpoint]
        bp.view_functions[endpoint] = require_api_key(view_func)
    return bp

app.register_blueprint(protect_blueprint(logs_bp))
app.register_blueprint(protect_blueprint(rules_bp))
app.register_blueprint(protect_blueprint(alerting_bp))
app.register_blueprint(protect_blueprint(export_bp))

if __name__ == '__main__':
    app.run(debug=True) 
