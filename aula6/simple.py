from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import FOAF, XSD
import pprint

g = Graph()
g.parse("cinema.ttl")

print(len(g))
print(g.serialize())

print("=====================================")

for stmt in g:
    pprint.pprint(stmt)