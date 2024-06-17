import csv, json
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, OWL, XSD

# Namespaces
ns = Namespace("http://www.example.org/disease-ontology#")

# Inicializar o grafo RDF
g = Graph()
g.bind("ex", ns)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

#Exercicio 1, 2 e 3

# Carregar a ontologia existente
g.parse("medical.ttl", format="turtle")

# Função para criar URIs de doenças e sintomas
def create_disease_uri(disease_name):
    return ns[disease_name.replace(" ", "_")]

def create_symptom_uri(symptom_name):
    return ns[symptom_name.replace(" ", "_")]

# Ler o CSV e processar as doenças e sintomas
with open('Disease_Syntoms.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease_name = row['Disease']
        disease_uri = create_disease_uri(disease_name)

        # Verificar se a doença já existe
        if (disease_uri, RDF.type, ns.Disease) not in g:
            # Criar instância da doença
            g.add((disease_uri, RDF.type, ns.Disease))

        # Lista de sintomas para associar à doença
        symptoms = []
        for i in range(1, 18):
            symptom_name = row[f'Symptom_{i}'].strip()
            if symptom_name:
                symptom_uri = create_symptom_uri(symptom_name)

                # Verificar se o sintoma já existe
                if (symptom_uri, RDF.type, ns.Symptom) not in g:
                    # Criar instância do sintoma
                    g.add((symptom_uri, RDF.type, ns.Symptom))

                # Associar o sintoma à doença
                g.add((disease_uri, ns.hasSymptom, symptom_uri))
                #symptoms.append(symptom_uri)

        # Adicionar a lista de sintomas como propriedade da doença
        if symptoms:
            g.add((disease_uri, ns.hasSymptom, Literal(", ".join([str(s) for s in symptoms]))))

# Salvar a ontologia atualizada
g.serialize(destination="updated_ontology.ttl", format="turtle")


#Exercicio 4

# Carregar a ontologia existente
g.parse("updated_ontology.ttl", format="turtle")

# Adicionar a nova propriedade :hasDescription
g.add((ns.hasDescription, RDF.type, OWL.DatatypeProperty))
g.add((ns.hasDescription, RDFS.domain, ns.Disease))
g.add((ns.hasDescription, RDFS.range, XSD.string))

# Função para criar URIs de doenças
def create_disease_uri(disease_name):
    return ns[disease_name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")]

# Ler o CSV e processar as descrições das doenças
with open('Disease_Description.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease_name = row['Disease']
        description = row['Description']
        disease_uri = create_disease_uri(disease_name)

        # Adicionar a descrição à instância da doença
        if (disease_uri, RDF.type, ns.Disease) in g:
            g.add((disease_uri, ns.hasDescription, Literal(description, datatype=XSD.string)))

# Salvar a ontologia atualizada
g.serialize(destination="updated_ontology_with_descriptions.ttl", format="turtle")


#Exercicio 6 e 7

# Carregar a ontologia existente
g.parse("updated_ontology_with_descriptions.ttl", format="turtle")

# Função para criar URIs de doenças e tratamentos
def create_uri(name):
    return ns[name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")]

# Ler o CSV e processar os tratamentos das doenças
with open('Disease_Treatment.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease_name = row['Disease']
        disease_uri = create_uri(disease_name)

        # Adicionar tratamentos
        for i in range(1, 5):
            treatment_name = row[f'Precaution_{i}'].strip()
            if treatment_name:
                treatment_uri = create_uri(treatment_name)
                
                # Se a instância de tratamento não existir, adicioná-la
                if (treatment_uri, RDF.type, ns.Treatment) not in g:
                    g.add((treatment_uri, RDF.type, ns.Treatment))
                    g.add((treatment_uri, RDFS.label, Literal(treatment_name)))

                # Associar o tratamento à doença
                g.add((disease_uri, ns.hasTreatment, treatment_uri))

# Salvar a ontologia atualizada
g.serialize(destination="updated_ontology_with_treatments.ttl", format="turtle")


# Carregar a ontologia existente
g.parse("updated_ontology_with_treatments.ttl", format="turtle")

# Função para criar URIs de doentes
def create_patient_uri(patient_id):
    return ns["Patient_" + str(patient_id)]

# Função para limpar strings e criar URIs de sintomas
def create_symptom_uri(symptom_name):
    cleaned_name = symptom_name.replace(" ", "_")  # Substituir espaços por underscores
    return ns[cleaned_name]

# Carregar os dados do arquivo JSON
with open('pg54246.json') as json_file:
    data = json.load(json_file)
    patient_id_counter = 1
    for patient_data in data:
        patient_name = patient_data['nome']
        patient_symptoms = patient_data['sintomas']
        
        # Criar URI para o doente
        patient_uri = create_patient_uri(patient_id_counter)
        
        # Adicionar instância de doente
        g.add((patient_uri, RDF.type, ns.Patient))
        g.add((patient_uri, ns.name, Literal(patient_name)))
        
        # Associar os sintomas ao doente
        for symptom in patient_symptoms:
            symptom_uri = create_symptom_uri(symptom)
            g.add((patient_uri, ns.exhibitsSymptom, symptom_uri))
        
        # Incrementar o contador de IDs de doentes
        patient_id_counter += 1

# Salvar a ontologia atualizada com os doentes e sintomas associados
g.serialize(destination="updated_ontology_with_patients_and_ids.ttl", format="turtle")
