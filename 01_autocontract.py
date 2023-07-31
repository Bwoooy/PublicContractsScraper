import xml.etree.ElementTree as ET

# Especifica la ruta del archivo .atom que deseas analizar
ruta_archivo = r'C:\Users\itacl\contratacion\licitacionesPerfilesContratanteCompleto_202301\licitacionesPerfilesContratanteCompleto3.atom'

# Parsear el archivo XML
tree = ET.parse(ruta_archivo)
root = tree.getroot()

# Definir el espacio de nombres (namespace) para facilitar las consultas
namespaces = {
    'atom': 'http://www.w3.org/2005/Atom',
    'cbc-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2',
    'cac-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2',
    'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2',
    'ns1': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
}

# Recorrer cada entrada (licitación) en el archivo .atom
for entry in root.findall('.//atom:entry', namespaces):
    # Extraer el título de la licitación
    titulo = entry.find('./atom:title', namespaces).text.strip()

    # Extraer el estado de la licitación
    summary_text = entry.find('./atom:summary', namespaces).text.strip()
    estado = summary_text.split('Estado: ')[1].split(';')[0].strip()

    # Extraer el campo "Importe" si existe
    importe = None
    for part in summary_text.split(';'):
        if 'Importe:' in part:
            importe = part.split('Importe:')[1].strip()
            break
    importe = importe if importe is not None else "Importe no disponible"

    # Extraer el CityName si existe en la ubicación adecuada
    city_name = entry.find('./cac-place-ext:ContractFolderStatus/cac-place-ext:LocatedContractingParty/cac:Party/cac:PostalAddress/cbc:CityName', namespaces)
    city_name = city_name.text.strip() if city_name is not None else "CityName no disponible"

    print("Título de la licitación:", titulo)
    print("Estado de la licitación:", estado)
    print("CityName:", city_name)
    print("Importe:", importe)
    print("-------------------------")
