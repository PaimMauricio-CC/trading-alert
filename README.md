# TradingView Webhook Receiver

A simple Flask app to receive TradingView alerts via webhook.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server:

```bash
python server.py
```

TradingView should send POST requests to `http://<server_ip>:5000/webhook` with JSON payloads.


### Email Notifications

Set the following environment variables before running the server so it can send emails using Gmail:

```
set GMAIL_USER="your@gmail.com"
set GMAIL_PASS="app_password"
set TO_EMAIL="destination@example.com"
```

##Use an [App Password](https://support.google.com/accounts/answer/185833) for `GMAIL_PASS` if you have two-factor authentication enabled.
##=======

