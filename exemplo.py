from flask import Flask, request, redirect, render_template_string, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

ALERT_FILE = os.path.join(os.path.dirname(__file__), 'alerts.json')

# Simple credentials from env vars
USER = os.getenv('APP_USER', 'admin')
PASSWORD = os.getenv('APP_PASS', 'password')

LOGIN_TEMPLATE = """
<!doctype html>
<title>Login</title>
{% if error %}<p style='color:red;'>{{ error }}</p>{% endif %}
<form method=post>
  <input type=text name=username placeholder=Username required>
  <input type=password name=password placeholder=Password required>
  <button type=submit>Login</button>
</form>
"""

ASSETS_TEMPLATE = """
<!doctype html>
<title>Ativos</title>
<p>Logado como {{ session['user'] }} | <a href="{{ url_for('logout') }}">Sair</a></p>
<ul>
{% for alert in alerts %}
  <li>{{ alert }}</li>
{% endfor %}
</ul>
"""

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('assets'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USER and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('assets'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Credenciais invalidas')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/ativos')
def assets():
    if 'user' not in session:
        return redirect(url_for('login'))
    alerts = []
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, 'r') as f:
            try:
                alerts = json.load(f)
            except json.JSONDecodeError:
                alerts = []
    return render_template_string(ASSETS_TEMPLATE, alerts=alerts)

if __name__ == '__main__':
    app.run(port=8000)