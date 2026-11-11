from flask import Flask, jsonify, request, render_template
import json, os, threading, time

app = Flask(__name__)
DATA_FILE = 'data.json'
lock = threading.Lock()

def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {}

def save(d):
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f)

dados = load()
ultima_att = time.time()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dados')
def get_dados():
    return jsonify({'dados': dados, 'ts': ultima_att})

@app.route('/api/atualizar', methods=['POST'])
def atualizar():
    global dados, ultima_att
    body = request.get_json()
    n = str(body['n'])
    with lock:
        if body['status'] == 'disponivel':
            dados.pop(n, None)
        else:
            dados[n] = {'status': body['status'], 'nome': body.get('nome', '')}
        ultima_att = time.time()
        save(dados)
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
