import requests
import json
import os
import io
import re
from PIL import Image
import multiprocessing
from bs4 import BeautifulSoup

ADDR = "https://github.com/CCondeluci/WeissSchwarz-ENG-DB/tree/master/DB"
RAW = "https://raw.githubusercontent.com/CCondeluci/WeissSchwarz-ENG-DB/refs/heads/master/DB/"

def clean_name(name : str):
    """
    Cleans a name by removing non-alphanumeric characters.

    Args:
        name: The name to clean.

    Returns:
        The cleaned name with only alphanumeric characters.
    """
    name = name.replace(' ', '_').replace('/', '')
    cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return cleaned_name.lower()

def worker_func(card):
    """
    Takes a json object representing a trading card and saves the image.

    Args:
        card: a json object representing a trading card

    Returns:
        None
    """
    try:
        img = card.get('image')
        # place a way to skip certain sets here to prevent unwanted cards
        if img:
            name = card.get('name')
            name = clean_name(name)
            set = clean_name(card.get('set'))

            nm = requests.get(img).content

            name = "wsz_" + set + "_" + name

            img = Image.open(io.BytesIO(nm))
            img.save(f'{os.getcwd() + "/normal-cards/" + name + "_md.png"}')
            return
        else:
            return
    except Exception as e:
        print(f"error processing card {card.get('name')}: {e}")
        return

if __name__ == "__main__":
    try:
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Directory already exist")

    # Get links on page -> Get cards in link -> Put cards into json or a tuple
    main_page = requests.get(ADDR)
    soup = BeautifulSoup(main_page.content, "html.parser")
    file_parents = soup.findAll('a', {'class': 'Link--primary'}) # get the hrefs
    files = []

    for i in file_parents:
        files.append(json.loads(requests.get(RAW + i['title']).content))

    for i in files:
        pool = multiprocessing.Pool()
        pool.map(worker_func, i)
        pool.close()
        pool.join()