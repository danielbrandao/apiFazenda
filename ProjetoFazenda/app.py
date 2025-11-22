# app.py (Parte 1)
from flask import Flask, render_template, jsonify, request

# app.py (Parte 2)
import json
import os

# Inicializa a aplicação Flask
app = Flask(__name__)

# Nome do arquivo JSON que simula o nosso "banco de dados" da fazenda
DADOS_FAZENDA = 'fazenda_data.json'

def carregar_dados():
    """Carrega os dados do nosso arquivo JSON."""
    with open(DADOS_FAZENDA,'r', encoding='UTF-8') as f:
        return json.load(f)

def salvar_dados(dados):
    """Salva os dados no nosso arquivo JSON."""
    with open(DADOS_FAZENDA, 'w', encoding='UTF-8') as f:
        json.dump(dados, f, indent=4)

#Criando uma ROTA
@app.route('/')
def home():
    return "<h1>Bem-vindo à API da Fazenda Inteligente!</h1><p>Acesse /dashboard para o painel de controle.</p>"

# --- Rota do Frontend (para HTML) ---
@app.route('/dashboard')
def dashboard():
    """Serve a página principal do nosso dashboard."""
    # O Flask procura 'index.html' na pasta 'templates'
    return render_template('index.html')

@app.route('/api/sensores/solo', methods=['GET'])
def get_sensores_solo():
  dados = carregar_dados()
  return jsonify(dados['sensores_solo'])

@app.route('/api/sensores/solo/<sensor_id>/historico', methods=['GET'])
def get_historico_solo(sensor_id):
    dados = carregar_dados()
    chave_historico = f"historico_{sensor_id}"
    if chave_historico in dados:
        return jsonify(dados[chave_historico])
    else:
        return jsonify({"erro": "Histórico não encontrado para o sensor"}), 404

@app.route('/api/irrigadores', methods=['GET'])
def get_irrigadores():
  dados = carregar_dados()
  return jsonify(dados['irrigadores'])

@app.route('/api/irrigadores/<irrigador_id>/status', methods=['POST'])
def set_irrigador_status(irrigador_id):
    dados = carregar_dados()
    novo_status = request.json.get('status')

    if not novo_status:
        return jsonify({"erro": "Novo status não fornecido"}), 400

    irrigador_encontrado = False
    for irrigador in dados.get('irrigadores', []):
        if irrigador['id'] == irrigador_id:
            irrigador['status'] = novo_status
            irrigador_encontrado = True
            break
    
    if irrigador_encontrado:
        salvar_dados(dados)
        return jsonify({"sucesso": f"Status do irrigador {irrigador_id} atualizado para {novo_status}"})
    else:
        return jsonify({"erro": f"Irrigador {irrigador_id} não encontrado"}), 404

@app.route('/api/sensores/ambiente', methods=['GET'])
def get_sensores_ambiente():
  dados = carregar_dados()
  return jsonify(dados['sensores_ambiente'])


# --- Ponto de Partida para Rodar o Servidor ---
if __name__ == '__main__':
    # debug=True faz o servidor reiniciar sozinho quando salvamos
    app.run(debug=True, port='5001')