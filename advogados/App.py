from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON 

app = Flask(__name__)

# (R) Listar todos os advogados
#
@app.get('/advogados')
def get_advogados():
    query = """
PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
SELECT ?adv ?n ?i ?a ?b ?c ?cor
WHERE {
?adv a :Advogado ;
:nome ?n ;
:idade ?i ;
:área ?a ;
:bebida ?b ;
:carro ?c ;
:cor ?cor .
}
"""
    resultado = sparql_get_query(query)
    advogados = []
    for linha in resultado['results']['bindings']:
        advogado = {
            "id": linha['adv']['value'].split('#')[-1],
            "nome": linha['n']['value'],
            "idade": linha['i']['value'],
            "área": linha['a']['value'],
            "bebida": linha['b']['value'],
            "carro": linha['c']['value'],
            "cor": linha['cor']['value']
        }
        advogados.append(advogado)
    return jsonify(advogados), 200


@app.get('/advogados/<id>')
def get_advogado(id):
    query = f"""
        PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
        SELECT * WHERE{{
            :{id} ?p ?o .
        }}
"""
    resultado = sparql_get_query(query)
    if resultado['results']['bindings']:
        advogado = {}
        for linha in resultado['results']['bindings']:
            advogado[linha['p']['value'].split('#')[-1]] = linha['o']['value'].split('#')[-1]
        return jsonify(advogado), 200
    else:
        return jsonify({"erro": "Advogado inexistente..."}), 404

# (C)riar um advogado
#
@app.post('/advogados')
def create_advogado():
    dados = request.json
    if not dados:
        return jsonify({"erro": "Não foram enviados dados do advogado a criar..."}), 400
    else:
        triplos = []
        if "nome" in dados:
            triplos.append(f":{dados['id']} :nome \"{dados['nome']}\" .")
        if "idade" in dados:
            triplos.append(f":{dados['id']} :idade \"{dados['idade']}\" .")
        if "área" in dados:
            triplos.append(f":{dados['id']} :área \"{dados['área']}\" .")
        if "cor" in dados:
            triplos.append(f":{dados['id']} :cor \"{dados['cor']}\" .")
        if "carro" in dados:
            triplos.append(f":{dados['id']} :carro \"{dados['carro']}\" .")
        if "bebida" in dados:
            triplos.append(f":{dados['id']} :bebida \"{dados['bebida']}\" .")

        query = f"""
        PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
        INSERT DATA{{
            :{dados['id']} a :Advogado, :Pessoa, owl:NamedIndividual .
            {"\n".join(triplos)}
        }}
        """
        sparql_query(query)
        return jsonify({"mensagem": f"Advogado criado com sucesso: {dados['id']}"})


# (D) Apagar um advogado
#
@app.delete('/advogados/<id>')
def delete_advogado(id):
    query = f"""
    PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
    DELETE{{
        :{id} ?p ?o .
    }}
    WHERE{{
       :{id} ?p ?o . 
    }}
    """
    sparql_query(query)
    return jsonify({"mensagem": f"Advogado removido da base de dados: {id}"})


# (U) Alterar um advogado
#
@app.put('/advogados/<id>')
def update_advogado(id):
    dados = request.json
    if not dados:
        return jsonify({"erro": "Não foram enviados dados do advogado a alterar..."}), 400
    else:
        triplos_apagar = []
        triplos_inserir = []
        if "nome" in dados:
            triplos_apagar.append(f":{dados['id']} :nome ?o .")
            triplos_inserir.append(f":{dados['id']} :nome \"{dados['nome']}\" .")
        if "idade" in dados:
            triplos_apagar.append(f":{dados['id']} :idade ?o .")
            triplos_inserir.append(f":{dados['id']} :idade \"{dados['idade']}\" .")
        if "área" in dados:
            triplos_apagar.append(f":{dados['id']} :área ?o .")
            triplos_inserir.append(f":{dados['id']} :área \"{dados['área']}\" .")
        if "cor" in dados:
            triplos_apagar.append(f":{dados['id']} :cor ?o .")
            triplos_inserir.append(f":{dados['id']} :cor \"{dados['cor']}\" .")
        if "carro" in dados:
            triplos_apagar.append(f":{dados['id']} :carro ?o .")
            triplos_inserir.append(f":{dados['id']} :carro \"{dados['carro']}\" .")
        if "bebida" in dados:
            triplos_apagar.append(f":{dados['id']} :bebida ?o .")
            triplos_inserir.append(f":{dados['id']} :bebida \"{dados['bebida']}\" .")

        query = f"""
        PREFIX : <http://www.di.uminho.pt/prc2021/advogados#>
        DELETE{{
            {"\n".join(triplos_apagar)}
        }}
        INSERT{{
            {"\n".join(triplos_inserir)}
        }}
        WHERE{{
            :{id} ?p ?o . 
        }}
        """
        sparql_query(query)
        return jsonify({"mensagem": f"Advogado alterado com sucesso: {id}"})


# ------- Funções Auxiliares --------------------------
def sparql_get_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/advogados")
    sparql.setMethod('GET')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def sparql_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/advogados/statements")
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == '__main__':
    app.run(debug=True)