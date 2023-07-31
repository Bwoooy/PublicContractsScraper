import pandas as pd
import xml.etree.ElementTree as ET
import zipfile

# Path to your .atom archive and XML file within it
atom_archive_path = 'path/to/your/archive.atom'
xml_file_inside_archive = 'entry.xml'

# Function to extract XML data from the .atom archive
def extract_xml_from_atom(atom_path, xml_file):
    with zipfile.ZipFile(atom_path) as z:
        with z.open(xml_file) as f:
            return f.read()

# Read XML data from the .atom archive
xml_data = extract_xml_from_atom(atom_archive_path, xml_file_inside_archive)

# Parse the XML data
root = ET.fromstring(xml_data)

# Initialize lists to store the extracted information
titles = []
place_names = []
states_of_bid = []
tax_exclusive_amounts = []
winning_party_names = []
tender_tax_exclusive_amounts = []

# Extract information from each <entry> element
for entry in root.findall('.//entry', namespaces=root.nsmap):
    title = entry.find('title').text.strip()
    summary = entry.find('summary').text.strip()

    # Extract information from <cac-place-ext:ContractFolderStatus> element
    contract_status = entry.find('.//cac-place-ext:ContractFolderStatus', namespaces=root.nsmap)
    if contract_status is not None:
        state_of_bid = contract_status.find('cbc-place-ext:ContractFolderStatusCode', namespaces=contract_status.nsmap).text.strip()
        tax_exclusive_amount = contract_status.find('cbc-place-ext:ContractFolderID', namespaces=contract_status.nsmap).text.strip()
    else:
        state_of_bid = "Not Available"
        tax_exclusive_amount = "Not Available"

    # Extract information from <cac-place-ext:TenderResult> element
    tender_result = entry.find('.//cac-place-ext:TenderResult', namespaces=root.nsmap)
    if tender_result is not None:
        winning_party_name = tender_result.find('.//cac:WinningParty/cbc:Name', namespaces=root.nsmap).text.strip()
        tender_tax_exclusive_amount = tender_result.find('cbc-place-ext:TaxExclusiveAmount', namespaces=root.nsmap).text.strip()
    else:
        winning_party_name = "Not Available"
        tender_tax_exclusive_amount = "Not Available"

    # Extract the place name from the summary
    place_name = summary.split(';')[-1].strip()

    # Store the extracted information in lists
    titles.append(title)
    place_names.append(place_name)
    states_of_bid.append(state_of_bid)
    tax_exclusive_amounts.append(tax_exclusive_amount)
    winning_party_names.append(winning_party_name)
    tender_tax_exclusive_amounts.append(tender_tax_exclusive_amount)

# Create a DataFrame with the extracted information
data = {
    'Title': titles,
    'Place Name': place_names,
    'State of Bid': states_of_bid,
    'Tax Exclusive Amount': tax_exclusive_amounts,
    'Winning Party Name': winning_party_names,
    'Tender Tax Exclusive Amount': tender_tax_exclusive_amounts
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = 'output.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Data has been successfully saved to {output_file}.")
