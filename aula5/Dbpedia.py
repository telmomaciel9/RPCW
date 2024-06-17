import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"



#SELECT DISTINCT ?desporto ?label ?abstract
#WHERE {
#    ?desporto a dbo:Sport ;
#              rdfs:label ?label ;
#              dbo:abstract ?abstract .
#    FILTER (LANG(?label) = 'en' && LANG(?abstract) = 'en') .
#}

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}



f =open("desportos_inicial.json")
desportos = json.load(f)
f.close()

atletas = []

for desporto in desportos:
    # Define the SPARQL query
    sparql_query = f"""
    PREFIX dbo:  <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT DISTINCT ?s ?nome ?dataNasc ?localLabel ?dataObito
    WHERE {{
        ?s dbp:sport <{desporto['uri']}> .
        optional {{ ?s dbp:birthDate ?dataNasc }}
        optional {{ ?s dbp:deathDate ?dataObito }}
        optional {{
            ?s dbp:birthPlace ?localNasc .
            ?localNasc rdfs:label ?localLabel .
            filter(lang(?localLabel) = 'en')
        }}
        ?s foaf:name ?nome .
    }}
    """

    # Define the parameters
    params = {
        "query": sparql_query,
        "format": "json"
    }

    # Send the SPARQL query using requests
    response = requests.get(sparql_endpoint, params=params, headers=headers)


    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        # Print the results
        desporto['atletas']= []

        for result in results["results"]["bindings"]:
            atleta= {}
            atleta["uri"] = result["s"]["value"]
            atleta["nome"] = result["nome"]["value"]
            if "dataNasc" in result:
                atleta["dataNasc"] = result["dataNasc"]["value"]
            if "localLabel" in result:
                atleta["localLabel"] = result["localLabel"]["value"]
            if "dataObito" in result:
                atleta["dataObito"] = result["dataObito"]["value"]

            desporto['atletas'].append(atleta)

    else:
        print("Error:", response.status_code)
        print(response.text)

# Save the results to a JSON file
f = open("desportos.json", "w", encoding="utf-8")
json.dump(desportos, f, indent=4)
f.close()