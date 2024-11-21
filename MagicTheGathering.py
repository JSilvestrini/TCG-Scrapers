import requests
import json
from PIL import Image
import os
import io
import re
import multiprocessing

JSON_LOC = "https://api.scryfall.com/bulk-data"

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
        img_uri = card.get('image_uris')
        # place a way to skip certain sets here to prevent unwanted cards
        if img_uri:
            name = card.get('name')
            name = clean_name(name)
            set = card.get('set')

            sm = requests.get(img_uri.get('small')).content
            nm = requests.get(img_uri.get('normal')).content

            name = "mtg_" + set + "_" + name

            img = Image.open(io.BytesIO(sm))
            img.save(f'{os.getcwd() + "/small-cards/" + name + "_sm.png"}')

            img = Image.open(io.BytesIO(nm))
            img.save(f'{os.getcwd() + "/normal-cards/" + name + "_md.png"}')
            return
        else:
            return
    except:
        print(f"error processing card {card.get('name')}")
        return

def language(card):
    """
    Checks the language on the card to ensure it is english (could be changed manually for other languages)

    Args:
        card: a json object representing a trading card

    Returns:
        None
    """
    if card.get('lang') == 'en':
        return card
    return None

def filter_none_values(data):
    """
    Removes all NoneType values from data.

    Args:
        data: a json containing card objects

    Returns:
        data without NoneTypes
    """
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [item for item in data if item is not None]
    else:
        return data

if __name__ == "__main__":
    try:
        os.mkdir(os.getcwd() + "\\small-cards")
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Directories already exist")

    data_request = requests.get(JSON_LOC)
    data = json.loads(data_request.content)
    bulk_cards_uri = data["data"][3]["download_uri"]
    bulk_grabber = requests.get(bulk_cards_uri)

    with multiprocessing.Pool() as pool:
        english_json = pool.map(language, bulk_grabber.content)
        english_json = filter_none_values(english_json)

    pool = multiprocessing.Pool()
    pool.map(worker_func, english_json)
    pool.close()
    pool.join()