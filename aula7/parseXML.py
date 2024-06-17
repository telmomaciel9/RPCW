import xml.etree.ElementTree as ET

tree = ET.parse('agenda.xml')
root = tree.getroot()

# for child in root:
#    print(child.tag, child.attrib)

# for entrada in root.iter('entrada'):
#    nome = entrada[0]
#    print(nome.text, entrada.attrib)

# for entrada in root.iter('entrada'):
#    print('------------------------')
#    for campo in entrada:
#        print(campo.tag, campo.text)

# for entrada in root.findall('entrada'):
#    print('------------------------')
#    for campo in entrada:
#        print(campo.tag, campo.text)

# for n in root.findall('.//nome'):
#     print('------------------------')
#     print(n.text)

for numero in root.iter('telefone'):
    print(numero.text)