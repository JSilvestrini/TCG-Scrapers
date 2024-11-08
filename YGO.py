from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import os
import time
import io

# The address used to get the card ID and small art
ADDRESS = "https://ygoprodeck.com/card-database/?num=100&offset="
# Location of fullsized cards
CARD_LOCATION = "https://images.ygoprodeck.com/images/cards/"
# Used to check if the card is loaded or not
CARD_BACK = "https://images.ygoprodeck.com/images/assets/CardBack.jpg"
# Hardcoded page limit, used to check if on last page
OFFSET_MAX = 135

if __name__ == "__main__":

    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        os.mkdir(os.getcwd() + "\\YGO_Full")
        os.mkdir(os.getcwd() + "\\YGO_Small")
    except:
        print("Card directory already exists")

    for page in range(0, OFFSET_MAX):
        print(f"[{page}/{OFFSET_MAX}] Pages Downloaded")
        curr_addr = ADDRESS + str(page * 100)
        driver.get(curr_addr)

        names = []

        while (len(names) < 100 and page < OFFSET_MAX - 1) or (page == OFFSET_MAX - 1 and len(names) < 19):
            time.sleep(0.1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            parent = soup.find(id="api-area-results")
            names = parent.findAll('a')

        imgs = parent.findAll('img', attrs={"class": "lazy"})


        for i in range(0, len(imgs)):
            img_src = imgs[i]['src']
            if img_src == CARD_BACK:
                img_src = imgs[i]['data-src']
            img_id = img_src[img_src.rfind('/') + 1:]
            img_name = names[i]['href'][names[i]['href'].rfind('/') + 1:names[i]['href'].rfind('-')]

            data = requests.get(img_src).content
            img = Image.open(io.BytesIO(data))
            img.save(f'{os.getcwd() + "/YGO_Small/" + img_name + "-small.jpg"}')

            data = requests.get(CARD_LOCATION + f"{img_id}").content
            img = Image.open(io.BytesIO(data))
            img.save(f'{os.getcwd() + "/YGO_Full/" + img_name + "-full.jpg"}')

    driver.quit()