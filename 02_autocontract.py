import pandas as pd
import xml.etree.ElementTree as ET

# Especifica la ruta del archivo .atom que deseas analizar
ruta_archivo = r'C:\Users\itacl\contratacion\licitacionesPerfilesContratanteCompleto_202302\licitacionesPerfilesContratanteCompleto3.atom'

# Define the namespaces as a dictionary
namespaces = {
    'atom': 'http://www.w3.org/2005/Atom',
    'cbc-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2',
    'cac-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2',
    'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2',
    'ns1': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
}

# Parsear el archivo XML
tree = ET.parse(ruta_archivo)
root = tree.getroot()

# Initialize lists to store the extracted information
unique_cpv_list = []
titles = []
place_names = []
presentacion_dates = []
states_of_bid = []
tax_exclusive_amounts = []
winning_party_names = []
tender_tax_exclusive_amounts = []

# Extract information from each <entry> element
for entry in root.findall('.//atom:entry', namespaces=namespaces):
    title = entry.find('atom:title', namespaces=namespaces).text.strip()
    summary = entry.find('atom:summary', namespaces=namespaces).text.strip()

    # Extract information from <cbc:CityName> element for place name
    city_name = entry.find('.//cbc:CityName', namespaces=namespaces)
    place_name = city_name.text.strip() if city_name is not None else "Not Available"

    # Extract information from <cac-place-ext:ContractFolderStatus> element
    contract_status = entry.find('.//cac-place-ext:ContractFolderStatus', namespaces=namespaces)

    if contract_status is not None:
        state_of_bid = contract_status.find('cbc-place-ext:ContractFolderStatusCode', namespaces=namespaces).text.strip()
        folder_element = contract_status.find('cbc:ContractFolderID', namespaces=namespaces)
        folder = folder_element.text.strip() if folder_element is not None else "Not Available"
    else:
        state_of_bid = "Not Available"
        folder = "Not Available"

    # Extract information from <cac:BudgetAmount> element for Tax Exclusive Amount
    budget_amount = entry.find('.//cac:BudgetAmount', namespaces=namespaces)
    if budget_amount is not None:
        tax_exclusive_amount = budget_amount.find('cbc:TaxExclusiveAmount', namespaces=namespaces).text.strip()
    else:
        tax_exclusive_amount = "Not Available"

    # Extract information from <cac-place-ext:TenderResult> element
    tender_result = entry.find('.//cac:TenderResult', namespaces=namespaces)
    if tender_result is not None:
        winning_party_element = tender_result.find('.//cac:WinningParty', namespaces=namespaces)
        if winning_party_element is not None:
            party_name_element = winning_party_element.find('.//cac:PartyName/cbc:Name', namespaces=namespaces)
            winning_party_name = party_name_element.text.strip() if party_name_element is not None else "Not Available"
        else:
            winning_party_name = "Not Available"
    else:
        winning_party_name = "Not Available"

    # Extract information from <cac:AwardedTenderedProject> for tender tax exclusive amount
    awarded_tendered_project = entry.find('.//cac:AwardedTenderedProject', namespaces=namespaces)
    if awarded_tendered_project is not None:
        tender_tax_exclusive_element = awarded_tendered_project.find('.//cbc:TaxExclusiveAmount', namespaces=namespaces)
        tender_tax_exclusive_amount = tender_tax_exclusive_element.text.strip() if tender_tax_exclusive_element is not None else "Not Available"
    else:
        tender_tax_exclusive_amount = "Not Available"

    # Extract information from <cac:TenderSubmissionDeadlinePeriod> for presentation date
    tender_submission_deadline = entry.find('.//cac:TenderSubmissionDeadlinePeriod', namespaces=namespaces)
    if tender_submission_deadline is not None:
        presentacion_date = tender_submission_deadline.find('cbc:EndDate', namespaces=namespaces).text.strip()
    else:
        presentacion_date = "Not Available"

    # Extract information from <cac:RequiredCommodityClassification> for CPV codes
    cpv_elements = entry.findall('.//cac:RequiredCommodityClassification/cbc:ItemClassificationCode', namespaces=namespaces)
    cpv_values = [cpv.text.strip() for cpv in cpv_elements]

    # Remove duplicates from the list of CPV values
    unique_cpv_values = []
    for cpv in cpv_values:
        if cpv not in unique_cpv_values:
            unique_cpv_values.append(cpv)

    # Store the unique CPV values in the list
    unique_cpv_list.append(unique_cpv_values)   

    # Store the extracted information in lists
    titles.append(title)
    place_names.append(place_name)
    states_of_bid.append(state_of_bid)
    presentacion_dates.append(presentacion_date)
    tax_exclusive_amounts.append(tax_exclusive_amount)
    winning_party_names.append(winning_party_name)
    tender_tax_exclusive_amounts.append(tender_tax_exclusive_amount)

# Create a DataFrame with the extracted information
data = {
    'CPV':unique_cpv_list,
    'Titol': titles,
    'Lloc': place_names,
    'Estat': states_of_bid,
    'Data entrega': presentacion_dates,
    'Pressupost base de licitació': tax_exclusive_amounts,
    'Adjudicatari': winning_party_names,
    'Import Adjudicació sense IVA': tender_tax_exclusive_amounts
}
df = pd.DataFrame(data)

# Convert numeric columns to float with 2 decimal places
numeric_columns = ['Pressupost base de licitació', 'Import Adjudicació sense IVA']
df[numeric_columns] = df[numeric_columns].apply(lambda x: pd.to_numeric(x.str.replace(',', ''), errors='coerce'))
df[numeric_columns] = df[numeric_columns].round(2)

# Save the DataFrame to an Excel file
output_file = 'output.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl', float_format='%.2f')

print(f"Data has been successfully saved to {output_file}.")
