# XML Merging + Scraping for Multiple XML Files

import os
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

# ------------------------------
# STEP 1: Set your folder path
# ------------------------------
folder_path = r"E:\senepati_sir_batch\10_11_25\xml file"

# ------------------------------
# STEP 2: Define cleaning functions
# ------------------------------
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = re.sub('  ', ' ', text)
    return text

# ------------------------------
# STEP 3: Merge all XML files
# ------------------------------
merged_root = ET.Element("merged_data")

for file in os.listdir(folder_path):
    if file.endswith(".xml"):
        file_path = os.path.join(folder_path, file)
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Convert XML content to string
        xml_str = ET.tostring(root, encoding='utf8').decode('utf8')

        # Clean (denoise) XML text
        clean_text = denoise_text(xml_str)

        # Create new XML element for each file’s content
        file_element = ET.SubElement(merged_root, "file", name=file)
        file_element.text = clean_text

# ------------------------------
# STEP 4: Save merged XML
# ------------------------------
merged_tree = ET.ElementTree(merged_root)
output_path = os.path.join(folder_path, "merged.pdf")
merged_tree.write(r"E:\senepati_sir_batch\10_11_25\merged.pdf", encoding="utf-8", xml_declaration=True)

print(f"All XML files merged successfully into: {output_path}")


# 