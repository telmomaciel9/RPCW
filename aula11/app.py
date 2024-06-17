from flask import Flask, render_template, url_for
from datetime import datetime
import requests

def extract_after_slash(s):
    return s.split('/')[-1]

app = Flask(__name__)

data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB
graphDB_endpoint = "http://localhost:7200/repositories/seres_vivos"

@app.route('/')
def index():
    return render_template('index.html', data= {"data": data_iso_formatada})

@app.route('/classes')
def classes():
    sparql_query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?className
WHERE {
  ?class rdf:type owl:Class .
  ?class rdfs:label ?className .
}
"""
    resposta = requests.get(graphDB_endpoint, 
                            params = {'query': sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})

    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']

        return render_template('classes.html', data= dados)
    else:
        return render_template('error.html', data= {"data": data_iso_formatada})
    

if __name__ == '__main__':
    app.run(debug=True)