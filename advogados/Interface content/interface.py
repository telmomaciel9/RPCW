from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# data do sistema em formato ANSI ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

# Página principal
#
@app.get('/')
def pag_principal():
    return render_template('index.html', data = {"data": data_iso_formatada})

# Tabela com os advogados
#
@app.get('/advogados')
def pag_advogados():
    resposta = requests.get('http://127.0.0.1:5000/advogados')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('advogados.html', data=data)
    else:
        return render_template('empty.html', data=data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)