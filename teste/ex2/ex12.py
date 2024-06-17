from rdflib import Graph, Namespace, RDF

# Carregar a ontologia existente
g = Graph()
g.parse("med_doentes.ttl", format="turtle")

# Definir o namespace
ns = Namespace("http://www.example.org/disease-ontology#")

# Query SPARQL para diagnosticar a doença de cada paciente
construct_query = """
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

CONSTRUCT {
  ?patient :hasDisease ?disease .
}
WHERE {
  ?patient rdf:type :Patient .
  ?disease rdf:type :Disease .
  
  ?disease :hasSymptom ?symptom .
  
  FILTER NOT EXISTS {
    ?disease :hasSymptom ?diseaseSymptom .
    FILTER NOT EXISTS {
      ?patient :exhibitsSymptom ?diseaseSymptom .
    }
  }
}
"""

# Executar a query CONSTRUCT
construct_results = g.query(construct_query)

# Adicionar os novos triplos à ontologia
for triple in construct_results:
    g.add(triple)

# Salvar a ontologia atualizada com os novos triplos
g.serialize(destination="updated_ontology_with_diagnoses.ttl", format="turtle")
