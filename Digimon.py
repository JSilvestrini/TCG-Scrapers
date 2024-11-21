import requests
import io
import re
from PIL import Image
import multiprocessing
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

ADDR = "https://digimoncard.io/packs/"
BASE = "https://digimoncard.io" # pack/name name name

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

def setify(setname):
    """
    Takes a phrase and returns a string of the first letter of each word.

    Args:
        phrase: The input phrase.

    Returns:
        A string containing the first letter of each word in the phrase.
    """

    words = setname.split()
    acronym = ''.join(word[0] for word in words)
    return acronym

def worker_func(addr):
    """
    Takes the address of a pack and extracts all cards from the page.

    Args:
        addr: a web address that contains trading cards

    Returns:
        None
    """

    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get(addr)

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    imgs = soup.findAll('img', attrs={"class": "lazy"})

    set = soup.find('h2', attrs={'class': 'set-title'})

    if set == None:
        set = 'setless'
    else:
        set = clean_name(setify(set.text))

    if len(imgs) == 0:
        return

    for i in imgs:
        try:
            src = i['src']
            name = i['alt']
            name = clean_name(name)

            nm = requests.get(src).content
            name = "dgmn_" + set + "_" + name
            img = Image.open(io.BytesIO(nm))
            img.save(f'{os.getcwd() + "/normal-cards/" + name + "_md.png"}')

        except:
            print(f"{set}-{i['alt']} Failed to download")
            continue

    driver.quit()

if __name__ == "__main__":
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Card directory already exists")

    pages = []

    driver.get(ADDR)
    for i in range(0, 9):
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find('tbody', {'class':'tablebody'})
        a = table.findAll('a')

        for i in a:
            pages.append(BASE + i['href'])

        # press next page
        button = driver.find_element(By.ID, 'myTable_next')
        try:
            button.click()
        except:
            continue

    driver.quit()

    pool = multiprocessing.Pool()
    pool.map(worker_func, pages)
    pool.close()
    pool.join()