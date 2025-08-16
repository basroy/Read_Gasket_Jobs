import re, os
from tkinter import BooleanVar
from typing import Dict, List, Union

class JobPath:
    filepath = "C:\\Users\\Bashobi\\PycharmProjects\\PythonProject\\GasketUI\\Jobs\\Day_1"
    rootpath = "C:\\Users\\Bashobi\\PycharmProjects\\PythonProject\\GasketUI\\Jobs"

class Quote:
    QUANTITY: str = 'Quantity'
    PRICE: str = 'Price'

class Colors:
    WHITE = '#ffffff'
    RUBY = '#8a175c'
    BISQUE = '#Ffe4c4'
    GREEN = '#018c48'
    GREENMATT='#009688'
    GRAY = '#787f88'
    BLUE = '#23395d'
    CYAN = '#0d6592'
    ICE = '#adb5bd'
    BROWN = '#1f0000'

class VarType:
    TRUE: BooleanVar=True
    FALSE: BooleanVar=False

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
    quote_quantity: Dict = {"Quote": 1, "Quantity": 0, "Rejected Rows": 0, }
    quote_quantity_price: Dict = {"Quote": 1, "Quantity": 0, "Price": 0, }

def prepare_summary():
    pass

