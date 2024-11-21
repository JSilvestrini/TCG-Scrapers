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

ADDR = "https://hearthcard.io/card-database/?&classn=N%2FA&format=Standard&limit=14&offset=0&sort=mana-name"

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
    Takes the zipped card and creates an image.

    Args:
        card: a zipped name and image source

    Returns:
        None
    """
    name, src = card
    name = clean_name(name)

    nm = requests.get(src).content
    name = "htsn_" + name
    img = Image.open(io.BytesIO(nm))
    img.save(f'{os.getcwd() + "/normal-cards/" + name + "_md.png"}')

if __name__ == "__main__":
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        os.mkdir(os.getcwd() + "\\normal-cards")
    except:
        print("Card directory already exists")

    driver.get(ADDR)
    imgs = []
    names = []
    for page in range(0, 139):
        time.sleep(.3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find('div', {'class':'api-results'})
        container = table.findAll('div', attrs = {'class': 'api-card'})

        for i in container:
            names.append(i['data-name'])
            imgs.append(i.find('img')['src'])

        # press next page
        button = driver.find_element(By.CLASS_NAME, 'fas.fa-chevron-square-right.paging-right-button')

        try:
            button.click()
        except:
            continue

    pool = multiprocessing.Pool()
    pool.map(worker_func, zip(names, imgs))
    pool.close()
    pool.join()

    driver.quit()