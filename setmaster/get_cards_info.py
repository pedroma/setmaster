#!/home/pma/.virtualenvs/setmaster/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from PIL import Image
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
import urllib
import requests
import os
import logging
import re

# setup logging in INFO level, increase to DEBUG for more information
LOG_FILE = "cards.log"
logger = logging.getLogger("setmaster")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, mode='w')
handler.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))
logger.addHandler(handler)

mongo = MongoClient()["magic"]

# timeout=False so we don't get pymongo.errors.OperationFailure: cursor id '693802459042815642' not valid at server
cards = mongo.cards.find(timeout=False)


def get_and_save_image(url, expansion_dir, card_mid):
    if not os.path.exists("{0}/{1}.jpg".format(expansion_dir, card_mid)):
        request = requests.get(url)
        try:
            i = Image.open(StringIO(request.content))
            if not os.path.exists(expansion_dir):
                os.mkdir(expansion_dir)
            i.save(u"{0}/{1}.jpg".format(
                expansion_dir, card_mid), "JPEG", quality=80, optimize=True, progressive=True)
        except:
            # this might be because the card image does not exist:
            # example: ERROR http://magiccards.info/scans/en/ug/92.jpg
            # Goblin token card 92

            # another possibility is that this is a flip card so the name would be {number}a and number{b}
            # example: http://magiccards.info/scans/en/bok/31a.jpg
            logger.error("{0} [{1}] [{2}]".format(
                url, card_name.encode('utf8'), number))

for card in cards:
    card_set = card["front"]["set"]
    query = {"gatherer": re.compile(r"^{0}$".format(
        card_set), re.IGNORECASE)}
    expansion = mongo.sets.find_one(query)
    if expansion is None:
        # this might be a MastersEdition which has MTGO
        query = {"gatherer": re.compile(r"^MTGO {0}$".format(
            card_set), re.IGNORECASE)}
        expansion = mongo.sets.find_one(query)
    number = card["front"]["number"]
    card_name = card["front"]["name"]
    card_mid = card["front"]["multiverse_id"]
    expansion_dir = "static_media/images/{0}".format(card_set)
    logger.debug("Processing [{0}] from [{1}] {2}".format(
        card_name.encode('utf8'), card_set, number))
    try:
        url = "http://magiccards.info/scans/en/{0}/{1}.jpg".format(
            expansion["mtgcardsinfo"], number)
    except:
        logging.error("^{0}$".format(card_set))
        break
    if number != "None":
        get_and_save_image(url, expansion_dir, card_mid)
    else:
        # if number is "None" go to the card page in magiccards.info and
        # find the img tag with the image we want.
        # If I want I can also store magiccards's number for this
        # card (don't think I need it for now)
        # http://magiccards.info/query?q=Wanderlust+e%3Aal%2Fen&v=card&s=cname
        url = "http://magiccards.info/query?q={0}+e%3A{1}&v=card&s=cname".format(
            urllib.quote(card_name.encode('utf8')), expansion["mtgcardsinfo"])
        req = requests.get(url)
        soup = BeautifulSoup(req.content)
        try:
            image_url = soup.find('img', alt=re.compile(card_name, re.IGNORECASE)).get("src")
        except AttributeError:
            logger.error("Failed parsing {0}: {1}".format(card_name.encode('utf8'), url))
            break
        get_and_save_image(image_url, expansion_dir, card_mid)
        logger.debug("{0} [{1}] [{2}]".format(
            url, card_name.encode('utf8'), number))
