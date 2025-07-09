from flask import Blueprint, request, jsonify
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

alerting_bp = Blueprint('alerting', __name__)

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')

@alerting_bp.route('/alert', methods=['POST'])
def trigger_alert():
    alert = request.json
    message = alert.get('message', 'Alert!')
    send_alert(message)
    return jsonify({"message": "Alert triggered", "alert": alert}), 200

def send_alert(message):
    # Send to Slack
    if SLACK_TOKEN and SLACK_CHANNEL:
        try:
            client = WebClient(token=SLACK_TOKEN)
            client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        except SlackApiError as e:
            print(f"Slack error: {e.response['error']}")
    # Send Email
    if EMAIL_HOST and EMAIL_USER and EMAIL_PASS and EMAIL_TO:
        try:
            msg = MIMEText(message)
            msg['Subject'] = 'SIEM Alert'
            msg['From'] = EMAIL_USER
            msg['To'] = EMAIL_TO
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        except Exception as e:
            print(f"Email error: {e}") 