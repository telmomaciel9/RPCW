import requests

endpoint_url = 'https://repositorium.sdum.uminho.pt/oai/oai'

params = { 'verb': 'ListRecords', 'metadataPrefix': 'oai_dc', 'set': 'com_1822_21291' }

r = requests.get(endpoint_url, params=params)

f = open('repositorium.xml', 'wb')
f.write(r.content)
f.close()

