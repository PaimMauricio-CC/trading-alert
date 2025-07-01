from flask import Flask, render_template_string

app = Flask(__name__)

# Rota principal que renderiza a lista de ativos
@app.route('/')
def index():
    # Dados de exemplo -- substitua por sua fonte de dados (API, WebSocket, etc.)
    assets = [
        {
            'symbol': 'AUDCAD',
            'description': 'Australian Dollar vs Canadian Dollar',
            'icon': 'fas fa-check-circle',
            'indicators': [
                {'status': 'green', 'timeframe': 'S', 'text': 'Deu alerta de compra.'},
                {'status': 'green', 'timeframe': 'D', 'text': ''},
                {'status': 'green', 'timeframe': '4H', 'text': 'Bollinger abriu. Deu alerta de compra.'},
                {'status': 'red',   'timeframe': 'H', 'text': ''},
                {'status': 'red',   'timeframe': '15', 'text': 'Mudou tendência.'}
            ],
            'last_capture': '01/07/2025, 08:15:09',
            'price': '$0.89563'
        },
        {
            'symbol': 'AUDJPY',
            'description': 'Australian Dollar vs Japanese Yen',
            'icon': 'fas fa-check-circle',
            'indicators': [
                {'status': 'green', 'timeframe': 'S', 'text': ''},
                {'status': 'red',   'timeframe': 'D', 'text': ''},
                {'status': 'red',   'timeframe': '4H', 'text': ''},
                {'status': 'red',   'timeframe': 'H', 'text': ''},
                {'status': 'green', 'timeframe': '15', 'text': 'Bollinger abriu.'}
            ],
            'last_capture': '01/07/2025, 08:15:07',
            'price': '$94.07'
        },
        # ... adicione mais ativos conforme necessário
    ]
    categories = ['Ações BR', 'Futuros BR', 'Fundos BR', 'NASDAQ', 'NYSE', 'Fundos EUA', 'Futuros EUA', 'Forex', 'Indices CFDs', 'Commodities CFDs', 'Crypto', 'Crypto CFDs', 'Lista 1']
    active_category = 'Lista 1'
    return render_template_string(TEMPLATE, assets=assets, categories=categories, active_category=active_category)

# Template HTML + CSS (com Bootstrap e Font Awesome)
TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Lista de ativos</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.14.0/css/all.css">
    <style>
        body { background-color: #1e1e2f; color: #fff; }
        .card { background-color: #2d2d3c; margin-bottom: 20px; }
        .card-header { display:flex; align-items:center; }
        .card-header .icon { font-size: 1.5rem; margin-right: 10px; }
        .card-header .title { flex-grow:1; font-weight:bold; }
        .card-header .fas { margin-left:10px; cursor:pointer; }
        .tab-bar { position: fixed; bottom:0; width:100%; background-color:#2d2d3c; padding:10px; }
        .tab-bar .nav-link { color:#ccc; }
        .tab-bar .active { font-weight:bold; color:#fff; }
        .indicator { display:flex; align-items:center; margin-bottom:5px; }
        .indicator .dot { width:10px; height:10px; border-radius:50%; margin-right:5px; }
        .indicator.green .dot { background-color:green; }
        .indicator.red .dot { background-color:red; }
        .indicator .label { margin-left:auto; background-color:#3d3d4d; padding:2px 6px; border-radius:4px; }
        .footer { font-size:0.8rem; color:#aaa; margin-top:10px; }
    </style>
</head>
<body>
<nav class="navbar navbar-dark bg-dark">
    <button class="btn btn-dark"><i class="fas fa-bars"></i></button>
    <span class="navbar-brand mx-auto">Lista de ativos</span>
    <div>
        <i class="fas fa-search"></i>
        <i class="fas fa-filter"></i>
        <i class="fas fa-sort"></i>
        <i class="fas fa-cloud-upload-alt"></i>
        <i class="fas fa-sync-alt"></i>
    </div>
</nav>
<div class="container mt-3 mb-5">
    <div class="row">
    {% for asset in assets %}
        <div class="col-md-6 col-lg-4">
            <div class="card">
                <div class="card-header">
                    <i class="icon {{ asset.icon }}"></i>
                    <div class="title">{{ asset.symbol }}</div>
                    <i class="fas fa-comment"></i>
                    <i class="fas fa-bell"></i>
                    <i class="fas fa-star"></i>
                </div>
                <div class="card-body">
                    <div>{{ asset.description }}</div>
                    {% for ind in asset.indicators %}
                    <div class="indicator {{ ind.status }}">
                        <div class="dot"></div>
                        <div>{{ ind.text }}</div>
                        <div class="label">{{ ind.timeframe }}</div>
                    </div>
                    {% endfor %}
                    <div class="footer">Última captura: {{ asset.last_capture }} – {{ asset.price }}</div>
                </div>
            </div>
        </div>
    {% endfor %}
    </div>
</div>
<nav class="tab-bar">
    <ul class="nav nav-pills justify-content-center">
        {% for cat in categories %}
        <li class="nav-item">
            <a class="nav-link {% if cat==active_category %}active{% endif %}" href="#">{{ cat }}</a>
        </li>
        {% endfor %}
    </ul>
</nav>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)