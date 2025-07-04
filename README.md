# TradingView Webhook Receiver

A simple Flask app to receive TradingView alerts via webhook.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server to receive TradingView alerts:

```bash
python server.py
```

TradingView should send POST requests to `http://<server_ip>:5000/webhook` with JSON payloads.

If the JSON includes a `text` field, that value becomes the body of the notification email. Otherwise the entire JSON payload is sent as the message.
Alerts are also appended to `alerts.json` so they can be viewed later in the member area.

### Email Notifications

Set the following environment variables before running the server so it can send emails using Gmail:

```
export GMAIL_USER="your@gmail.com"
export GMAIL_PASS="app_password"
export TO_EMAIL="destination@example.com"
```

Use an [App Password](https://support.google.com/accounts/answer/185833) for `GMAIL_PASS` if you have two-factor authentication enabled.

### Member Area

`exemplo.py` provides a very small front-end where you can log in and view the
alerts saved in `alerts.json`.

Run it separately:

```bash
python exemplo.py
```

Login credentials default to `admin`/`password` but can be configured with the
environment variables `APP_USER` and `APP_PASS`.  Set `SECRET_KEY` to control the
Flask session secret.