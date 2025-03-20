# Read_Gasket_Jobs
A Gui to read through xml files for keywords and present the contents of the key-value pairs.


import re,os
from typing import Dict, List, Union


class Quote:
    QUANTITY: str = 'Quantity'
    PRICE: str = 'Price'


class Colors:
    WHITE = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'


class Regex:
    regex_quantity = r'<Quantity (.+) Quantity/>'
    regex_price = r'<Price (.+) Price/>'

    def xtract_with_regex(self, line: str, regex: str) -> Union[str, None]:
        rg = re.compile(regex, re.IGNORECASE | re.DOTALL)
        match = rg.search(line)
        # print(f' {line}\n {match}')
        try:
            return match.group(1)
        except AttributeError or IndexError:
            return

class Qdata:
    xml_quote: Dict = {}
    quote_quantity: Dict = {
        "Quote": 1,
        "Quantity": 0,
        "Rejected Rows": 0,
    }
    quote_quantity_price: Dict = {
        "Quote": 1,
        "Quantity": 0,
        "Price": 0,
    }

path_to_job: str = 'anp_informat_logs'
subfiles = []
for dirpath, subdirs, files in os.walk(path_to_job):
    for x in files:
        if x.startswith("JOB") -a x.endswith(".xml"):
            subfiles.append(os.path.join(dirpath, x))



def parse_tdxml(file_path):
    try:
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        matches = re.findall(r'<Quantity>(.*?)</Quantity>', content, re.IGNORECASE)
        
        if matches:
            print("Found Quantity values:")
            for match in matches:
                print(match)
        else:
            print("No Quantity values found")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = "example.xml"  # Change this to your XML file path
parse_xml_for_quantity(file_path)


