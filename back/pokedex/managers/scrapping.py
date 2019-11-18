# import time
import re
import requests
from bs4 import BeautifulSoup
from playhouse.shortcuts import model_to_dict

from tqdm import tqdm
from lxml import etree, html

from pokedex.models.scrapping import Pokemon, Generation, Symbol

url = 'https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon'
generations_table_xpath = '//*[@id="mw-content-text"]/div/table[1]'
pokemons_table_xpath = '//*[@id="mw-content-text"]/div/table[3]'

# '/html/body/div[3]/div[2]/div[4]/div/table[1]'
symbole_xpath = '//*[@id="mw-content-text"]/div/table[2]'

wikipedia_request = requests.get(url)


def get_table(tabpath):
    tree = html.fromstring(wikipedia_request.content)
    print(tabpath)
    print(tree)
    tables = list(tree.xpath(tabpath))
    print(tables)
    return tables[0]


def get_pokemons():
    pokemons_table = get_table(pokemons_table_xpath)
    pokemons_table_rows = pokemons_table.findall('.//tr')
    pokemons = []
    generations = Generation.select()
    for row in pokemons_table_rows[2:]:
        columns = [col for col in row.findall('td') if (col.get('class') != "table-na")]
        for i, col in enumerate(columns):
            if i % 2 == 0:
                pokemon = {}
                pokemon["numero"] = int(get_text(col))
                pokemon["name"] = get_text(columns[i + 1].findall(".//a")[0])
                pokemon["generation"] = get_pokemon_genaration(pokemon["numero"], generations)
                img = get_image(columns[i + 1])
                pokemon["symbol"] = img if img is not None else get_text(columns[i + 1]).strip(pokemon["name"])
                # pokemon["color"] = get
                pokemons.append(pokemon)

    return pokemons


def load_pokemons_from_wiki():
     """this function load  pokemons from the wikipedia table and
     and create a table in  scrapping schemas
     """
     pokemons = get_pokemons()
     Pokemon.delete().execute()
     for pokemon in pokemons:
         Pokemon.create(numero=pokemon["numero"],name=pokemon["name"],generation=pokemon["generation"],symbol=pokemon["symbol"].strip())



def get_generation(id):
    id = int(id)
    if id <= 151:
        return "Generation I"
    elif id <= 251:
        return "Generation II"
    elif id <= 386:
        return "Generation III"
    elif id <= 483:
        return "Generation IV"
    elif id <= 649:
        return "Generation V"
    elif id <= 721:
        return "Generation VI"
    elif id <= 809:
        return "Generation VII"
    else:
        return "Generation VIII"


def get_image(td):
    img = []
    try:
        img = td.findall('.//img')
    except:
        pass
    if len(img) > 0:
        return clean_text(img[0].get('src'))


def get_text(td):
    text = " "
    try:
        text = td.text_content()
    except:
        pass
    return clean_text(text)


def get_text_or_image(td):
    img = get_image(td)

    if img:
        return img
    return get_text(td)


def clean_text(td):
    if td and td != "":
        clean = td.strip('\n')
        return clean
    return td


def get_generations():
    """get all generations from wikipedia table

    """
    generations_table = get_table(generations_table_xpath)
    generations_table_rows = generations_table.findall('.//tr')
    generations = []
    headers = ["titles", "remakes", "platforms"]
    for i, row in enumerate(generations_table_rows[2:]):
        yeartdtext = get_text(row.find('./td')).strip()
        rowtext = get_text(row)
        generation = {}
        regex = re.compile(r"[0-9]{4}–\w+")
        yearlist = regex.findall(yeartdtext)
        print(yeartdtext)
        print(yearlist)
        names = row.findall('.//th')
        columns = row.findall('td')
        if (len(yearlist) > 0):
            generation["name"] = get_text_or_image(names[0])
            generation["years"] = yearlist[0]
            print(columns)
            start = 1

        else:
            start = 0
            generation["name"] = generations[i - 1]["name"] if ((len(generations) > i - 1) and (i > 0)) else ""
            generation["years"] = generations[i - 1]["years"] if (len(generations) > i - 1 and (i > 0)) else ""
            """get numbers pokemons  total and news
            for a generation in the table row using regex digital
            since we know the column years contains digit we will remove it fromm all the digit within the row
            """
        generation["newpokemons"] = 0
        r2 = re.compile("\d+")
        numbers = r2.findall(get_text(columns[-2]))
        generation["total"] = get_text(columns[-1])
        stop = -1
        if (len(numbers) > 0):
            generation["newpokemons"] = numbers[0]
            stop = -2
        middle = columns[start:stop]
        for it, header in enumerate(headers):
            generation[header] = get_text(middle[it]) if (len(middle) > it) else (generations[i - 1][
                                                                                      header] if (
                    (len(generations) > i - 1) and (i > 0)) else "")

        generations.append(generation)
    return generations


def get_color(td):
    style = td.get('style')
    return style.split(":")[1].strip(';')


def get_symbols():
    symbols_table = get_table(symbole_xpath)
    symbols_rows = symbols_table.findall('.//tr')
    symbols = []

    for row in symbols_rows[1:]:
        columns = row.findall('td')
        print(columns)
        symbol = {}
        th = row.findall('.//th')
        print(row.findall('.//img'))
        symbol["character"] = get_text_or_image(th[0]) if (len(th) > 0) else ""
        symbol["color"] = get_color(th[0]) if (len(th) > 0) else ""
        for i, header in enumerate(["meaning", "description"]):
            symbol[header] = get_text_or_image(columns[i]) if (len(columns) > i) else ""

        symbols.append(symbol)

    return symbols


def get_pokemon_genaration(id, liste):
    generations = sorted([generation for generation in liste if int(generation.total) >= int(id)],
                         key=lambda i: i.total)
    return generations[0].name


def load_symbols_from_wiki():
    symbols = get_symbols()
    Symbol.delete().execute()
    for symbole in symbols:
        Symbol.create(character=symbole["character"], color=symbole["color"], meaning=symbole["meaning"],
                      description=symbole["description"])


def load_generations_from_wiki():
    generations = get_generations()
    Generation.delete().execute()
    for generation in generations:
        Generation.create(name=generation["name"], years=generation["years"], titles=generation["titles"],
                          remakes=generation["remakes"], platforms=generation["platforms"],
                          newpokemons=generation["newpokemons"], total=generation["total"])
def get_pokemons_from_db():
    pokemons= Pokemon.select()
    return [model_to_dict(pokemon) for pokemon  in pokemons]

def get_generations_from_db():
    generations= Generation.select()
    return [model_to_dict(generation) for generation in generations]

def get_symbols_from_db():
    symbols= Symbol.select()
    return [model_to_dict(symbol) for symbol in symbols]
