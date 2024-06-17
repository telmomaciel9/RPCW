from flask import Flask, render_template, url_for
import requests
from datetime import datetime

app = Flask(__name__)

# data do sistema em formato ANSI ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

# GraphDB endpoint details
graphdb_endpoint = "http://localhost:7200/repositories/tperiodica"

@app.route('/')
def index():
    return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/elements')
def elements():
    # Send SPARQL query to GraphDB
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?n ?nome ?simb where { 
	?s a tp:Element .
    ?s tp:name ?nome.
    ?s tp:symbol ?simb.
    ?s tp:atomicNumber ?n. 
}  
order by ?n
"""
    payload = {"query": sparql_query}

    response = requests.get(graphdb_endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('elements.html', data=data)
    else:
        return render_template('empty.html', data=data)


@app.route('/elements/<int:na>')
def element(na):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{ 
	?s a tp:Element .
    ?s tp:name ?nome.
    ?s tp:symbol ?simb.
    ?s tp:atomicNumber {na}. 
}}  
order by ?n
"""
    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('element.html', data = {
            "data": data_iso_formatada,
            "na": na,
            "nome": data[0]["nome"]["value"],
            "simb": data[0]["simb"]["value"]
        })
    else:
        return render_template('empty.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

