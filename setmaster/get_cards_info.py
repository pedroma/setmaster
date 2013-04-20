#!/home/pma/.virtualenvs/setmaster/bin/python
from pymongo import MongoClient
from PIL import Image
from StringIO import StringIO
import requests
import os
import logging
import re

LOG_FILE = "cards.log"

logger = logging.getLogger("setmaster")
handler = logging.FileHandler(filename=LOG_FILE, mode='w')
handler.setFormatter(logging.Formatter('[%(levelname)s] - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

mongo = MongoClient()["magic"]

cards = mongo.cards.find()

# There are some cards where the number is "None" because they don't
# really have a number (old cards)

for card in cards:
    query = {"gatherer": re.compile(r"^{0}$".format(
        card["front"]["set"]), re.IGNORECASE)}
    expansion = mongo.sets.find_one(query)
    number = card["front"]["number"]
    logger.debug("Processing [{0}] from [{1}] {2}".format(card[
                 "front"]["name"].encode('utf8'), card["front"]["set"], number))
    url = "http://magiccards.info/scans/en/{0}/{1}.jpg".format(
        expansion["mtgcardsinfo"], number)
    if number != "None":
        expansion_dir = "static_media/images/{0}".format(card["front"]["set"])
        # only download what is not downloaded
        if not os.path.exists("{0}/{1}.png".format(expansion_dir, card["front"]["multiverse_id"])):
            req = requests.get(url)
            try:
                i = Image.open(StringIO(req.content))
                if not os.path.exists(expansion_dir):
                    os.mkdir(expansion_dir)
                i.save(u"{0}/{1}.jpg".format(expansion_dir, card["front"][
                       "multiverse_id"]), "JPEG", quality=80, optimize=True, progressive=True)
            except:
                # this might be because the card image does not exist:
                # example: ERROR http://magiccards.info/scans/en/ug/92.jpg
                # Goblin token card 92

                # another possibility is that this is a flip card so the name would be {number}a and number{b}
                # example: http://magiccards.info/scans/en/bok/31a.jpg
                logger.error("{0} [{1}] [{2}]".format(url, card[
                             "front"]["name"].encode('utf8'), number))
    else:
        # if number is "None" I should try and go to magiccardsinfo and somehow
        # guess its number I can try to do a search:
        # http://magiccards.info/query?q=Wanderlust+e%3Aal%2Fen&v=card&s=cname
        # and from that search get the card image url and definitely store the magiccard.info
        # number toghether with the card info
        logger.warn("{0} [{1}] [{2}]".format(url, card[
                    "front"]["name"].encode('utf8'), number))
