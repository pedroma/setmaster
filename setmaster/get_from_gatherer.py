# -*- coding: utf-8 -*-
import os
import requests
import logging
from mongoengine import connect
from pymongo import MongoClient
from bs4 import BeautifulSoup
from cards.models import Card, CardDetail

connect("magic")

# setup logging in INFO level, increase to DEBUG for more information
LOG_FILE = "cards.log"
log = logging.getLogger("setmaster")
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, mode='w')
handler.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))
log.addHandler(handler)

GATHERER_URL = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid={0}"
GATHERER_IMG_URL = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={0}&type=card"
GATHERER_BASE = "http://gatherer.wizards.com/{0}"
MTGCARD_INFO_IMG = "http://magiccards.info/scans/en/{0}/{1}.jpg"
CARDS = MongoClient()["magic"].cards
SETS = MongoClient()["magic"].sets
MANA_SYMBOLS = MongoClient()["magic"].symbols
COLORS = ("White", "Blue", "Red", "Black", "Green")

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def getElementValue(soup, element, selector=" .value", component=0):
    params = '[id$="cardComponent{2}"] [id$="{0}"]{1}'.format(element, selector, component)
    matches = soup.select(params)
    if matches:
        return matches[0].text.strip()
    else:
        return None

def getElementList(soup, element, selector=" .cardtextbox", component=0):
    params = '[id$="cardComponent{2}"] [id$="{0}"]{1}'.format(element, selector, component)
    matches = soup.select(params)
    result = []
    for match in matches:
        result.append(match.text)
    return result

def getOtherSets(soup):
    params = '[id$="cardComponent0"] [id$="otherSetsValue"] img'
    matches = soup.select(params)
    result = []
    for match in matches:
        title = match.get("title")
        src = match.get("src")
        clean_title = title[0:title.index("(")].strip()
        result.append(clean_title)
        src = src.replace("size=small", "size=large")
        src = src.lstrip("../..")
        SETS.update({
            "gatherer": clean_title
        }, {
            "$set": {"image": GATHERER_BASE.format(src)}
        })
    return result

def getManaAndColors(soup):
    params = '[id$="cardComponent0"] [id$="manaRow"] .value img'
    matches = soup.select(params)
    colors = []
    mana = []
    for match in matches:
        alt = match.get("alt")
        src = match.get("src")
        if alt in COLORS and alt not in colors:
            colors.append(alt)
        mana.append(alt)
        src = src.replace("size=medium", "size=large")
        src = src.lstrip("/")
        MANA_SYMBOLS.update({
            "title": alt
        }, {
            "$set": {"image": GATHERER_BASE.format(src)}
        }, True)
    return mana, colors

def parse_file(filename):
    setname = filename[0:-4]  # take out the last for chars (.txt)
    f = open("ids/{0}".format(filename), "r")
    expansion = SETS.find_one({"gatherer": setname})
    for id in f.readlines():
        multiverse_id = id.rstrip()  # clean \n and other garbage
        if Card.objects.filter(multiverse_id=multiverse_id).count():
            continue
        req = requests.get(GATHERER_URL.format(multiverse_id))
        soup = BeautifulSoup(req.content)
        card_type = getElementValue(soup, "typeRow")
        extra_content = {}
        # cards with "//"  in their name are split cards
        name = getElementValue(soup, "nameRow")
        multiverse_id = multiverse_id
        number = getElementValue(soup, "numberRow")
        rarity = getElementValue(soup, "rarityRow", " .value span")
        artist = getElementValue(soup, "artistRow", " .value a")
        power_toughness = getElementValue(soup, "ptRow")

        cmc = getElementValue(soup, "cmcRow")

        othersets = getOtherSets(soup)
        mana, colors = getManaAndColors(soup)
        flavor = getElementList(soup, "FlavorText")
        text = getElementList(soup, "textRow")

        # based on card type, get extra content if needed
        physical_card_type = "normal"  # one of double, split, flip, normal
        if " // " in name:
            physical_card_type = "split"
            name, second_name = name.split(" // ")
            extra_content = {
                "name": second_name
            }
            # follow new url and get details for second part of card
        if len(soup.select('[id$="subtitleDisplay]')) > 1:
            # special card here. Either double or flip
            transform = flip = False
            for t in text:
                if "transform" in t:
                    transform = True
                if "flip" in t:
                    flip = True
            if transform and flip:
                # problem, should write card info manually
                log.warn("Card has transform and flip. Edit manually: {0}".format(multiverse_id))
                continue
            if transform:
                physical_card_type = "double"
            if flip:
                physical_card_type = "flip"

            if physical_card_type in ("flip", "double"):
                snd_number = getElementValue(soup, "numberRow", component=1)
                extra_content = {
                    "name": getElementValue(soup, "nameRow", component=1),
                    "number": snd_number,
                    "pt": getElementValue(soup, "ptRow", component=1),
                    "flavor": getElementList(soup, "FlavorText", component=1),
                    "rules_text": getElementList(soup, "textRow", component=1),
                    "type": getElementValue(soup, "typeRow", component=1),
                    "mtgcardinfo_img": MTGCARD_INFO_IMG.format(expansion["mtgcardsinfo"], snd_number),
                    "gath_img": GATHERER_IMG_URL.format(multiverse_id),
                }

        detail = {
            "mtgcardinfo_img": MTGCARD_INFO_IMG.format(expansion["mtgcardsinfo"], number),
            "gath_img": GATHERER_IMG_URL.format(multiverse_id),
            "pt": power_toughness,
            "colors": colors,
            "number": number,
            "cmc": safe_cast(cmc, int, 0),
            "flavor": flavor,
            "rules_text": text,
            "type": card_type,
            "mana": mana,
            "name": name
        }
        card_detail = CardDetail(**detail)
        card = {
            "set": setname,
            "type": physical_card_type,
            "multiverse_id": int(multiverse_id),
            "artist": artist,
            "rarity": rarity,
            "othersets": othersets,
            "card_details": card_detail,
        }
        if extra_content:
            card.update({"extra_details": CardDetail(**extra_content)})

        card = Card(**card)
        card.save()

        print "Inserted", name

files = os.listdir("ids/")
from joblib import Parallel, delayed
Parallel(n_jobs=8)(delayed(parse_file)(filename) for filename in files)
