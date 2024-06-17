from rdflib import OWL, Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import FOAF, XSD
import pprint
import json

g = Graph()
g.parse("cinema.ttl")

file = open("cinema.json")
json_data = json.load(file)
print(json_data)

cinema = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")

g.add((URIRef(f"{cinema}Twilight"), RDF.type, OWL.NamedIndividual))
g.add((URIRef(f"{cinema}Twilight"), RDF.type, cinema.Film))
g.add((URIRef(f"{cinema}CatherineHardwicke"), RDF.type, OWL.NamedIndividual))
g.add((URIRef(f"{cinema}CatherineHardwicke"), RDF.type, cinema.Director))
g.add((URIRef(f"{cinema}Twilight"), cinema.hasDirector, cinema.CatherineHardwicke))


#print(len(g))
#print(g.serialize())

#print("=====================================")

#for stmt in g:
#    pprint.pprint(stmt)