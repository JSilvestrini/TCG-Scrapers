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

ADDR = "https://www.fowtcg.it/en/cardsdb?page=&cardname=&block=ALL&edition=ALL&cardnumber=&ABILITYTEXT=&ATKMIN=0&ATKMAX=2500&DEFMIN=0&DEFMAX=2500&CERCA=cerca#"
BASE = "https://www.fowtcg.it"
MED = "https://www.fowtcg.it/markdb/"

def clean_name(name : str):
    """
    Cleans a name by removing non-alphanumeric characters.

    Args:
        name: The name to clean.

    Returns:
        The cleaned name with only alphanumeric characters.
    """
    name = name.replace(' ', '_').replace('/', '').replace('-', '_')
    cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return cleaned_name.lower()

def worker_func(card):
    """
    Takes the address of a pack and extracts all cards from the page.

    Args:
        addr: a web address that contains trading cards

    Returns:
        None
    """
    small, normal = card
    name = normal[normal.rfind('/'):]
    name = clean_name(name)
    try:
        nm = requests.get(MED + small[small.rfind('/'):]).content
        nm_name = "fow_" + name + '_md'
        img = Image.open(io.BytesIO(nm))
        img.save(f'{os.getcwd() + "/normal-cards/" + nm_name + ".png"}')

        sm = requests.get(small).content
        sm_name = "fow_" + name + '_sm'
        img = Image.open(io.BytesIO(sm))
        img.save(f'{os.getcwd() + "/small-cards/" + sm_name + ".png"}')
    except:
        print(f"{name} Failed to download")

if __name__ == "__main__":
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        os.mkdir(os.getcwd() + "\\small-cards")
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Card directory already exists")

    small = []
    normal = []

    driver.get(ADDR)
    for i in range(0, 27):
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #table = soup.find('div', {'class':'catalog.catalog-gallery'})
        loc = soup.findAll('a', {'class': 'preview'})

        for j in loc:
            small.append(BASE + j.find('img')['src'])
            normal.append(BASE + j['href'])

        # press next page
        try:
            if i == 0:
                button = driver.find_element(By.CSS_SELECTOR, '.pagination > li:nth-child(28) > a:nth-child(1)')
            else:
                button = driver.find_element(By.CSS_SELECTOR, '.pagination > li:nth-child(29) > a:nth-child(1)')
            button.click()
        except:
            continue

    driver.quit()

    cards = zip(small, normal)

    pool = multiprocessing.Pool()
    pool.map(worker_func, cards)
    pool.close()
    pool.join()