# TCG-Scrapers

## Introduction

This repository contains some scrapers that can be used to gather around 140,000 different trading cards from various card games. The main purpose of this was so I could have a dataset to create a GAN (Generative Adversarial Network) and learn more about PyTorch. 

## Contents

- **[Installation](#installation)**
- **[Running](#running)**
- **[References](#references)**

## Installation

**Python Packages**
- bs4
- requests
- selenium
- PIL
- re (should be in the standard library)
- multiprocessing (should be in the standard library)

**Other**
- Mozilla Firefox webdriver

**Note:** For selenium you could use any webdriver, but I personally prefer Firefox, so if you do not have it downloaded you will either need to edit the code to utilize Chrome or some other webdriver, or download Firefox.

## Running

To use any of the scrapers, just run them like you would any normal python program.

For the databases that contain different sizes and qualities of cards it will download the **medium** and **small** cards since this was originally used to gather data rather than high quality images.

**Note:** Some of the scrapers use a considerable amount of RAM (the Magic the Gather scraper used around 8gb when I first used it) and some take a less than ideal amount of time to finish execution as some webpages have to be loaded dynamically.

## References

The following links are for the databases that I scraped.

**The Magic the Gathering link brings you to an API page, and the Weiss Wars brings you to a github containing JSON files**

- **[Card Fight Vanguard Cards](https://vanguardcard.io/packs/)**
- **[Digimon Cards](https://digimoncard.io/packs/)**
- **[Force of Will Cards](https://www.fowtcg.it/en/cardsdb?page=&cardname=&block=ALL&edition=ALL&cardnumber=&ABILITYTEXT=&ATKMIN=0&ATKMAX=2500&DEFMIN=0&DEFMAX=2500&CERCA=cerca#)**
- **[Grand Archive Cards](https://index.gatcg.com/cards?sort=name&page=)**
- **[Hearthstone Cards](https://hearthcard.io/card-database/?&classn=N%2FA&format=Standard&limit=14&offset=0&sort=mana-name)**
- **[Magic the Gathering Cards](https://api.scryfall.com/bulk-data)**
- **[Pokemon Cards](https://pokemoncard.io/packs/)**
- **[Weiss Wars Cards](https://github.com/CCondeluci/WeissSchwarz-ENG-DB/tree/master/DB)**
- **[Yu-Gi-Oh Cards](https://ygoprodeck.com/card-database/?num=100&offset=)**