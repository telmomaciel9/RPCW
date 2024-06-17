import json

f = open('corridas.json')
bd = json.load(f)
f.close()

ttl = ""

for corredor in bd:
    registo = f""" 
###  http://rpcw.di.uminho.pt/2024/corridas#{corredor['número']}
<http://rpcw.di.uminho.pt/2024/corridas#{corredor['número']}> rdf:type owl:NamedIndividual ,
                                                      :Corredor ;
                                             :temHobby :{corredor['hobby']} ;
                                             :temTshirt :{corredor['tshirt']} ;
                                             :vive :{corredor['estado'].replace(" ", "_")} ;
                                             :idade "{corredor['idade']}"^^xsd:int ;
                                             :nome "{corredor['nome']}" ;
                                             :número "{corredor['número']}" .

###  http://rpcw.di.uminho.pt/2024/corridas#{corredor['estado'].replace(" ", "_")}
:{corredor['estado'].replace(" ", "_")} rdf:type owl:NamedIndividual ,
                :Estado .


###  http://rpcw.di.uminho.pt/2024/corridas#{corredor['hobby']}
:{corredor['hobby']} rdf:type owl:NamedIndividual ,
              :Hobby .


###  http://rpcw.di.uminho.pt/2024/corridas#{corredor['tshirt']}
:{corredor['tshirt']} rdf:type owl:NamedIndividual ,
                     :Tshirt .
                                             """
    
    ttl += registo

print(ttl)