from rdflib import OWL, Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import FOAF, XSD
import pprint
import json

g = Graph()
g.parse("cinema.ttl")

file = open("cinema.json")
json_data = json.load(file)

cinema = Namespace("http://rpcw.di.uminho.pt/2024/cinema/")

for film in json_data:
    g.add((URIRef(f"{cinema}{film["uri"]}"), RDF.type, OWL.NamedIndividual))
    g.add((URIRef(f"{cinema}{film["uri"]}"), RDF.type, cinema.Film))
    g.add((URIRef(f"{cinema}{film["uri"]}"), RDF.type, OWL.NamedIndividual))
    g.add((URIRef(f"{cinema}{film["uri"]}"), cinema.title, cinema.film["name"][0]))
    if "director" in film and film["director"]:
        for director in film["director"]:
            g.add((URIRef(f"{cinema}director"), RDF.type, OWL.NamedIndividual))
            g.add((URIRef(f"{cinema}director"), RDF.type, cinema.Director))
            g.add((URIRef(f"{cinema}{film["uri"]}"), cinema.hasDirector, cinema.director))
    if "writer" in film and film["writer"]:
        for writer in film["writer"]:
            g.add((URIRef(f"{cinema}writer"), RDF.type, OWL.NamedIndividual))
            g.add((URIRef(f"{cinema}writer"), RDF.type, cinema.Writer))
            g.add((URIRef(f"{cinema}{film["uri"]}"), cinema.hasWriter, cinema.writer))
    if "musicComposer" in film and film["musicComposer"]:
        for composer in film["musicComposer"]:
            g.add((URIRef(f"{cinema}composer"), RDF.type, OWL.NamedIndividual))
            g.add((URIRef(f"{cinema}composer"), RDF.type, cinema.MusicComposer))
            g.add((URIRef(f"{cinema}{film["uri"]}"), cinema.hasComposer, cinema.composer))
    if "actors" in film and film["actors"]:
        for actor in film["actors"]:
            g.add((URIRef(f"{cinema}actor"), RDF.type, OWL.NamedIndividual))
            g.add((URIRef(f"{cinema}actor"), RDF.type, cinema.Actor))
            g.add((URIRef(f"{cinema}{film["uri"]}"), cinema.hasActor, cinema.actor))

{
        "name": [
            "Cabaret Balkan"
        ],
        "director": [
            "Goran_Paskaljevi\u0107"
        ],
        "writer": [
            "Goran_Paskaljevi\u0107",
            "Filip_David"
        ],
        "musicComposer": [
            "Zoran_Simjanovi\u0107"
        ],
        "actors": [
            "Bogdan_Dikli\u0107",
            "Sergej_Trifunovi\u0107",
            "Neboj\u0161a_Glogovac",
            "Miki_Manojlovi\u0107",
            "Mirjana_Karanovi\u0107",
            "Bata_\u017divojinovi\u0107",
            "Dragan_Nikoli\u0107"
        ],
        "uri": "Cabaret_Balkan"
}


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