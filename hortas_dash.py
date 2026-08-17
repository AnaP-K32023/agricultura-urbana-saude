from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'horta-flask-secret-key'

# Criar diretórios
os.makedirs('static/data', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# ================= DADOS DE EXEMPLO =================
def carregar_dados():
    """Dados de exemplo das hortas"""
    dados = [
        {
            'centro_saude': 'CS Rio Vermelho',
            'regiao': 'Norte',
            'horta_ativa': True,
            'lat': -27.4835,
            'lon': -48.4265,
            'responsavel': 'Jardim Saúde Ativa',
            'plantas_medicinais': 'Erva baleeira, Espinheira santa, Boldo, Hortelã',
            'dia_grupo_horta': 'Quarta-feira 14h',
            'multirao': '15/07/2026',
            'data_atualizacao': '2026-06-15'
        },
        {
            'centro_saude': 'CS Barra da Lagoa',
            'regiao': 'Norte',
            'horta_ativa': True,
            'lat': -27.4532,
            'lon': -48.4781,
            'responsavel': 'Maria Silva',
            'plantas_medicinais': 'Hortelã, Boldo, Melissa, Alecrim',
            'dia_grupo_horta': 'Terça-feira 09h',
            'multirao': 'Não',
            'data_atualizacao': '2026-06-10'
        },
        {
            'centro_saude': 'CS Campeche',
            'regiao': 'Sul',
            'horta_ativa': True,
            'lat': -27.6823,
            'lon': -48.4821,
            'responsavel': 'Carlos Alberto',
            'plantas_medicinais': 'Erva baleeira, Manjericão, Alfavaca',
            'dia_grupo_horta': 'Sexta-feira 16h',
            'multirao': '20/07/2026',
            'data_atualizacao': '2026-06-12'
        },
        {
            'centro_saude': 'CS Trindade',
            'regiao': 'Centro',
            'horta_ativa': False,
            'lat': -27.5823,
            'lon': -48.5221,
            'responsavel': 'Fernanda Lima',
            'plantas_medicinais': 'Guaco, Boldo, Alfavaca',
            'dia_grupo_horta': '',
            'multirao': '',
            'data_atualizacao': '2026-06-01'
        }
    ]
    return pd.DataFrame(dados)

# ================= ROTAS =================
@app.route('/')
def index():
    return render_template('index.html', titulo="Horta Urbana")

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', titulo="Mapa das Hortas")

@app.route('/hortas')
def hortas():
    df = carregar_dados()
    return render_template('hortas.html', titulo="Nossas Hortas", hortas=df.to_dict('records'))

@app.route('/api/hortas')
def api_hortas():
    df = carregar_dados()
    
    # Converter para GeoJSON
    features = []
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['lon']), float(row['lat'])]
            },
            "properties": {
                "nome": row['centro_saude'],
                "regiao": row['regiao'],
                "ativa": bool(row['horta_ativa']),
                "responsavel": row['responsavel'],
                "plantas_medicinais": row['plantas_medicinais'],
                "dia_grupo_horta": row['dia_grupo_horta'],
                "multirao": row['multirao'],
                "data_atualizacao": row['data_atualizacao']
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Salvar GeoJSON
    with open('static/data/hortas.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    return jsonify(geojson)

@app.route('/api/resumo')
def api_resumo():
    df = carregar_dados()
    total = len(df)
    ativas = len(df[df['horta_ativa'] == True])
    
    return jsonify({
        "total_hortas": total,
        "hortas_ativas": ativas,
        "regioes": df['regiao'].unique().tolist(),
        "total_responsaveis": df['responsavel'].nunique(),
        "total_plantas": df['plantas_medicinais'].str.split(',').explode().nunique()
    })

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)
if __name__ == '__main__': #PARA ONRENDER
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)