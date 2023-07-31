import xml.etree.ElementTree as ET

# Aquí especifica la ruta del archivo .atom que deseas analizar
ruta_archivo = r'C:\Users\itacl\contratacion\licitacionesPerfilesContratanteCompleto_202301\licitacionesPerfilesContratanteCompleto3.atom'

# Parsear el archivo XML
tree = ET.parse(ruta_archivo)
root = tree.getroot()

# Mostrar la estructura del archivo XML
#print("Estructura del archivo XML:")
#print(ET.dump(root))

# Acceder a algunos datos específicos
print("\nAlgunos datos específicos:")
for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
    id_licitacion = entry.find('{http://www.w3.org/2005/Atom}id').text
    titulo = entry.find('{http://www.w3.org/2005/Atom}title').text
    resumen = entry.find('{http://www.w3.org/2005/Atom}summary').text
    print(f"ID Licitación: {id_licitacion}")
    print(f"Título: {titulo}")
    print(f"Resumen: {resumen}")
    print("-" * 50)
