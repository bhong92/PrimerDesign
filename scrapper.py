import requests
import random
from bs4 import BeautifulSoup
import json

elements = ['Helium',
            'Lithium',
            'Beryllium',
            'Boron',
            'Carbon',
            'Nitrogen',
            'Oxygen',
            'Fluorine',
            'Neon',
            'Sodium',
            'Magnesium',
            'Aluminum',
            'Silicon',
            'Phosphorus',
            'Sulfur',
            'Chlorine',
            'Argon',
            'Potassium',
            'Calcium',
            'Scandium',
            'Titanium',
            'Vanadium',
            'Chromium',
            'Manganese',
            'Iron',
            'Cobalt',
            'Nickel',
            'Copper',
            'Zinc',
            'Gallium',
            'Germanium',
            'Arsenic',
            'Selenium',
            'Bromine',
            'Krypton',
            'Rubidium',
            'Strontium',
            'Yttrium',
            'Zirconium',
            'Niobium',
            'Molybdenum',
            'Technetium',
            'Ruthenium',
            'Rhodium',
            'Palladium',
            'Silver',
            'Cadmium',
            'Indium',
            'Tin',
            'Antimony',
            'Tellurium',
            'Iodine',
            'Xenon',
            'Cesium',
            'Barium',
            'Lanthanum',
            'Cerium',
            'Praseodymium',
            'Neodymium',
            'Promethium',
            'Samarium',
            'Europium',
            'Gadolinium',
            'Terbium',
            'Dysprosium',
            'Holmium',
            'Erbium',
            'Thulium',
            'Ytterbium',
            'Lutetium',
            'Hafnium',
            'Tantalum',
            'Tungsten',
            'Rhenium',
            'Osmium',
            'Iridium',
            'Platinum',
            'Gold',
            'Mercury',
            'Thallium',
            'Lead',
            'Bismuth',
            'Polonium',
            'Astatine',
            'Radon',
            'Francium',
            'Radium',
            'Actinium',
            'Thorium',
            'Protactinium',
            'Uranium',
            'Neptunium',
            'Plutonium',
            'Americium',
            'Curium',
            'Berkelium',
            'Californium',
            'Einsteinium',
            'Fermium',
            'Mendelevium',
            'Nobelium',
            'Lawrencium',
            'Rutherfordium',
            'Dubnium',
            'Seaborgium',
            'Bohrium',
            'Hassium',
            'Meitnerium']


def findElement(element):
    url = "https://en.wikipedia.org/wiki/" + element
    response = requests.get(
        url=url
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    allTxt = soup.get_text()
    cTxt = allTxt.find('Contents') - 1
    rTxt = allTxt.find('reference') + 11

    if cTxt != -2 & rTxt != -1:
        return allTxt[rTxt:cTxt]


i = random.choice(elements)
def getJSON(e):
    info = findElement(e)
    element = {e: info}

    jsonFile = json.dumps(element, ensure_ascii=False)
    print(jsonFile)

    with open('example.json', 'w', encoding="utf-8") as outfile:
        outfile.write(jsonFile)

# url = "https://en.wikipedia.org/wiki/" + 'hydrogen'
# response = requests.get(
#     url=url
# )
# soup = BeautifulSoup(response.content, 'html.parser')
#
# allTxt = soup.get_text(strip=True)
# c = 0
# print(allTxt)
# info = allTxt[10:14]
# string = ''
# for i in info:
#     string += str(i)
# string = string.replace('<p>','')
# string = string.replace('</p>','')
# string = string.replace('<b>','')
# string = string.replace('</b>','')
# string = string.replace('<i>','')
# string = string.replace('</i>','')
#
# b = string.find('<')
# e = string.find('>')+1
#
# while b != -1:
#     remove = string[b:e]
#     string = string.replace(remove, '')
#     b = string.find('<')
#     e = string.find('>')+1
#
# print(string)