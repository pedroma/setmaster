# Create your views here.
from django.http import HttpResponse
import json
import pymongo
import os
import re

mongo = pymongo.MongoClient()["magic"]

def cards_list(request, query=None):
    if query is not None:
        cards = mongo.cards.find({"front.name": re.compile(r"{0}".format(query), re.IGNORECASE)})
        if len(query) < 5:
            cards.limit(20)
    else:
        cards = mongo.cards.find()
    cards.limit(20)
    cardlist = []
    for card in cards:
        directory_prefix = "/home/pma/workspace/setmaster/setmaster/api"
        if card["front"].get("set") is None:
            set = card["front"]["partA"]["set"]
        else:
            set = card["front"]["set"]
        if card["front"].get("multiverse_id") is None:
            multiverse_id = card["front"]["partA"]["multiverse_id"]
        else:
            multiverse_id = card["front"]["multiverse_id"]
        image_url = "/static/images/{0}/{1}.png".format(set, multiverse_id)
        print directory_prefix+image_url
        if os.path.exists(directory_prefix+image_url):
            cardlist.append({
                "name": card["front"]["name"],
                "multiverse_id": card["front"]["multiverse_id"],
                "set": card["front"]["set"],
                "image": image_url
            })
    return HttpResponse(json.dumps({"results": cardlist}), content_type="application/json")
