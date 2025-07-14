# Custom SIEM (Security Information & Event Management)

Aggregate, normalize, and analyze logs from various systems (network, firewall, OS) with real-time search, threat hunting, correlation rules, alerting, and dashboard export.

---

## 📚 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Directory Structure](#-directory-structure)
- [Setup & Installation](#-setup--installation)
- [API Authentication & Security](#api-authentication--security)
- [API Endpoints](#-api-endpoints)
- [Testing & Code Quality](#testing--code-quality)
- [Configuration](#-configuration)
- [Extending the Project](#-extending-the-project)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features
- **Real-time log ingestion** (via Logstash)
- **Query-based threat hunting** (Elasticsearch + Flask API)
- **Correlation rules for events** (customizable in Python)
- **Alerting system** (Email/Slack notifications)
- **Dashboard export** (PDF generation)
- **API key authentication** for all endpoints
- **Input validation** and error handling
- **Automated testing and CI/CD**

---

## 🏗️ Architecture

```
Log Sources (Network, Firewall, OS)
        │
    [Logstash]
        │
 [Elasticsearch] <──> [Kibana]
        │
    [Flask API]
        │
   [Alerting/Export]
```

- **Logstash**: Collects and normalizes logs from various sources.
- **Elasticsearch**: Stores and indexes logs for fast search and analysis.
- **Kibana**: Visualizes and explores log data.
- **Flask API**: Provides endpoints for queries, rule management, alerting, and exports.

---

## 📁 Directory Structure

```
custom_siem/
│
├── api/                # Flask app and API endpoints
│   ├── app.py
│   ├── elasticsearch_client.py
│   ├── routes/
│   └── rules/
│
├── logstash/           # Logstash configs
│   └── pipelines/
│
├── elasticsearch/      # Elasticsearch configs/scripts
│
├── kibana/             # Saved dashboards/visualizations
│
├── alerting/           # Email/Slack alert scripts
│
├── export/             # PDF export scripts
│
├── tests/              # Unit and integration tests
│
├── requirements.txt
├── SIEM_Project_Plan.txt
└── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kunal-masurkar/custom_siem.git
   cd custom_siem
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with the following (edit as needed):
   ```ini
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_USER=youruser
   ELASTICSEARCH_PASSWORD=yourpass
   SLACK_TOKEN=xoxb-...
   SLACK_CHANNEL=#alerts
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USER=your@email.com
   EMAIL_PASS=yourpassword
   EMAIL_TO=recipient@email.com
   API_KEY=changeme123  # Set your API key here
   ```

4. **Set up ELK stack (Elasticsearch, Logstash, Kibana):**
   - Use Docker or install locally.
   - Place Logstash pipeline configs in `logstash/pipelines/`.
   - Place Kibana dashboards in `kibana/`.

5. **Run the Flask API:**
   ```bash
   python -m api.app
   ```
   (Always run from the project root!)

---

## API Authentication & Security

- **All API endpoints (except `/` and `/health`) require an API key.**
- Pass your API key in the `X-API-KEY` header with every request:
  ```http
  X-API-KEY: changeme123
  ```
- Input validation is enforced on endpoints (e.g., `/logs/search` expects a string for `q`).
- Error responses are returned as JSON with appropriate status codes (e.g., 401 Unauthorized, 400 Bad Request).

---

## 🔍 API Endpoints

| Endpoint              | Method | Description                                 | Auth Required |
|-----------------------|--------|---------------------------------------------|--------------|
| `/logs/search`        | GET    | Search logs in Elasticsearch                | Yes          |
| `/rules`              | GET    | List all correlation rules                  | Yes          |
| `/rules`              | POST   | Add a new correlation rule                  | Yes          |
| `/alert`              | POST   | Trigger an alert (email/Slack)              | Yes          |
| `/export/pdf`         | POST   | Export a dashboard as a PDF                 | Yes          |
| `/`                   | GET    | API status                                  | No           |
| `/health`             | GET    | Health check                                | No           |

### Example: Search Logs
```
GET /logs/search?q=failed+login
X-API-KEY: changeme123
```
**Response:**
```json
{
  "results": [ ... ],
  "query": "failed login"
}
```
**Error Example:**
```json
{
  "error": "Unauthorized"
}
```

### Example: Add a Correlation Rule
```
POST /rules
X-API-KEY: changeme123
Content-Type: application/json
{
  "name": "Failed SSH Login",
  "conditions": {"event_type": "ssh", "status": "failed"}
}
```

### Example: Trigger an Alert
```
POST /alert
X-API-KEY: changeme123
Content-Type: application/json
{
  "message": "Suspicious activity detected!"
}
```

### Example: Export Dashboard as PDF
```
POST /export/pdf
X-API-KEY: changeme123
Content-Type: application/json
{
  "dashboard": "Network Overview"
}
```

---

## Testing & Code Quality

- **Unit and integration tests** are in the `tests/` directory.
- Run all tests with:
  ```bash
  pytest
  ```
- **Continuous Integration (CI)** is set up with GitHub Actions to run tests and linting on every push and pull request.
- All Python code uses **type hints** and **docstrings** for clarity and maintainability.
- Input validation is enforced using `marshmallow`.

---

## 🛠️ Configuration
- **Logstash:** Configure pipelines in `logstash/pipelines/` to parse and forward logs to Elasticsearch.
- **Elasticsearch:** No special config needed for demo; tune as needed for production.
- **Kibana:** Import dashboards/visualizations from `kibana/`.
- **Flask API:** All endpoints are in `api/routes/`.
- **Alerting:** Configure Slack and email credentials in `.env`.
- **API Key:** Set your API key in `.env` as `API_KEY`.

---

## 🧩 Extending the Project
- Add more advanced correlation rules (time windows, sequences, etc.)
- Integrate with more log sources (cloud, containers, etc.)
- Build a frontend UI for easier management
- Use Kibana’s reporting API for real dashboard exports
- Add authentication and RBAC to the API
- Integrate threat intelligence feeds
- Add automated response (SOAR-like features)

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

**Code Quality Guidelines:**
- Write unit tests for new features or bug fixes.
- Use type hints and docstrings in all Python code.
- Follow PEP8 and run `flake8` for linting.
- Ensure all tests pass before submitting a PR.

---

## 📄 License
[MIT](LICENSE) 

## 👥 Author

| Name | GitHub | LinkedIn |
|------|--------|----------|
| **Kunal Masurkar** | [GitHub](https://github.com/kunal-masurkar) | [LinkedIn](https://linkedin.com/in/kunal-masurkar-8494a123a) |
