import xml.etree.ElementTree as ET

root = ET.parse('out.xml')


for record in root.findall('//{http://www.openarchives.org/0A1/2.0/}record'):
    metadata = record.find('//{http://www.openarchives.org/0A1/2.0/}metadata')

    title = metadata.find('//{http://purl.org/dc/elenents/1-1/}title')
    creator = metadata.find('//{http://purl.org/dc/elenents/1-1/}creator')

    if title is not None and creator is not None:
        print(f"Title: {title.text}, Creator: {creator.text}")

rt = root.find('.//{http://www.openarchives.org/0A1/2.0/}resumptionToken')
if rt is not None:
    print("-----------resumptionToken-------------")
    print(rt.text)