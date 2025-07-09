from flask import Flask, jsonify
from api.routes.logs import logs_bp
from api.routes.rules import rules_bp
from api.routes.alerting import alerting_bp
from api.routes.export import export_bp

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Custom SIEM API is running."})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

app.register_blueprint(logs_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(alerting_bp)
app.register_blueprint(export_bp)

if __name__ == '__main__':
    app.run(debug=True) 