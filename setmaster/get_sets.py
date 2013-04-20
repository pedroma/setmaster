import requests
import pymongo
from BeautifulSoup import BeautifulSoup

mongo = pymongo.MongoClient()["magic"]

r_gatherer = requests.get("http://gatherer.wizards.com/Pages/Advanced.aspx")
r_magicinfo = requests.get("http://magiccards.info/search.html")
soup_gatherer = BeautifulSoup(r_gatherer.content)
soup_magicinfo = BeautifulSoup(r_magicinfo.content)
expansions_gatherer = soup_gatherer.find('div', {
                                         'class': 'dynamicAutoCompleteContainer'}).findAll('a')
expansions_magicinfo = soup_magicinfo.find(
    "select", {"id": "edition"}).findAll("option")

for expansion in expansions_magicinfo:
    exp_name = expansion.text
    exp_id = expansion.get("value").split("/")[0]
    if '/' not in exp_name and exp_name != "" and exp_id != "":
        mongo.sets.insert({"gatherer": exp_name, "mtgcardsinfo": exp_id})
