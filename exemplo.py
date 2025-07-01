from flask import Flask, request, redirect, render_template_string, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

ALERT_FILE = os.path.join(os.path.dirname(__file__), 'alerts.json')

LOGIN_TEMPLATE = """
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>Login</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
</head>
<body class='bg-light'>
  <div class='container py-5'>
    <div class='row justify-content-center'>
      <div class='col-md-4'>
        <div class='card shadow-sm'>
          <div class='card-body'>
            <h3 class='card-title mb-4 text-center'>Login</h3>
            {% if error %}<div class='alert alert-danger'>{{ error }}</div>{% endif %}
            <form method='post'>
              <div class='mb-3'>
                <input class='form-control' type='text' name='username' placeholder='Username' required>
              </div>
              <div class='mb-3'>
                <input class='form-control' type='password' name='password' placeholder='Password' required>
              </div>
              <button class='btn btn-primary w-100' type='submit'>Login</button>
            </form>
            <div class='text-center mt-3'>
              <a href="{{ url_for('register') }}">Register</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

ASSETS_TEMPLATE = """
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>Ativos</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
</head>
<body class='bg-light'>
  <div class='container py-4'>
    <div class='d-flex justify-content-end mb-3'>
      <span class='me-2'>Logado como {{ session['user'] }}</span>
      <a class='btn btn-sm btn-secondary' href="{{ url_for('logout') }}">Sair</a>
    </div>
    <ul class='list-group'>
    {% for alert in alerts %}
      <li class='list-group-item'>{{ alert }}</li>
    {% endfor %}
    </ul>
  </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>Register</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
</head>
<body class='bg-light'>
  <div class='container py-5'>
    <div class='row justify-content-center'>
      <div class='col-md-4'>
        <div class='card shadow-sm'>
          <div class='card-body'>
            <h3 class='card-title mb-4 text-center'>Register</h3>
            {% if error %}<div class='alert alert-danger'>{{ error }}</div>{% endif %}
            <form method='post'>
              <div class='mb-3'>
                <input class='form-control' type='text' name='username' placeholder='Username' required>
              </div>
              <div class='mb-3'>
                <input class='form-control' type='password' name='password' placeholder='Password' required>
              </div>
              <button class='btn btn-primary w-100' type='submit'>Create account</button>
            </form>
            <div class='text-center mt-3'>
              <a href="{{ url_for('login') }}">Back to login</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('assets'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            return render_template_string(REGISTER_TEMPLATE, error='Usuario ja existe')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['user'] = username
        return redirect(url_for('assets'))
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
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

@app.before_first_request
def init_db():
    db.create_all()

if __name__ == '__main__':
    app.run(port=8000)