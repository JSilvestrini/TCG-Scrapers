import requests
import io
import re
from PIL import Image
import multiprocessing
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

ADDR = "https://index.gatcg.com/cards?sort=name&page="
BASE = "https://ga-index-public.s3.us-west-2.amazonaws.com/cards"

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

def worker_func(addr):
    """
    Takes the address of a pack and extracts all cards from the page.

    Args:
        addr: a web address that contains trading cards

    Returns:
        None
    """

    name = addr[addr.rfind('/'):]
    name = clean_name(name)
    try:
        nm = requests.get(addr + '.jpg').content
        name = "grarc_" + name
        img = Image.open(io.BytesIO(nm))
        img.save(f'{os.getcwd() + "/normal-cards/" + name + "_md.png"}')
    except:
        print(f"{name} Failed to download")

if __name__ == "__main__":
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Card directory already exists")

    pages = []

    for i in range(0, 37):
        driver.get(ADDR + str(i+1))
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #table = soup.find('div', {'class':'catalog.catalog-gallery'})
        loc = soup.findAll('a', {'class': 'hover__aurora'})

        for i in loc:
            pages.append(BASE + i['href'][i['href'].rfind('/'):])

    driver.quit()

    pool = multiprocessing.Pool()
    pool.map(worker_func, pages)
    pool.close()
    pool.join()