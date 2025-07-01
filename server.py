from flask import Flask, request, jsonify
import logging
import os
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

ALERT_FILE = os.path.join(os.path.dirname(__file__), 'alerts.json')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info('Received webhook: %s', data)
    body = str(data)
    if isinstance(data, dict) and 'text' in data:
        body = data['text']
    _store_alert(body)
    send_email('TradingView Alert', body)
    return jsonify({'status': 'received'}), 200

def send_email(subject: str, body: str) -> None:
    """Send an email using Gmail's SMTP server."""
    user = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_PASS')
    to_addr = os.getenv('TO_EMAIL')

    if not all([user, password, to_addr]):
        app.logger.error('GMAIL_USER, GMAIL_PASS, and TO_EMAIL must be set')
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to_addr

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
    except Exception as e:
        app.logger.error('Failed to send email: %s', e)

def _store_alert(alert: str) -> None:
    """Append alert text to the alerts file with timestamp."""
    entry = f"{datetime.utcnow().isoformat()} - {alert}"
    try:
        if os.path.exists(ALERT_FILE):
            with open(ALERT_FILE, 'r') as f:
                try:
                    alerts = json.load(f)
                except json.JSONDecodeError:
                    alerts = []
        else:
            alerts = []
        alerts.append(entry)
        with open(ALERT_FILE, 'w') as f:
            json.dump(alerts, f)
    except Exception as e:
        app.logger.error('Failed to store alert: %s', e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)