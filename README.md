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
