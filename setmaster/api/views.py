# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from catalog.models import Catalog
import json
import pymongo
import os
import re

mongo = pymongo.MongoClient()["magic"]


@login_required
def catalog_list(request):
    catalog = Catalog.objects.filter(user=request.user)

    def get_items(items):
        return [{'quantity': i.quantity, 'identifier': i.identifier, 'name': i.name} for i in items]
    catalogs = [{'name': cat.name, 'items': cat.items.count()} for cat in catalog]
    return HttpResponse(json.dumps({"catalogs": catalogs}), content_type="application/json")


@login_required
def cards_list(request, query=None):
    if query is not None:
        cards = mongo.cards.find({"front.name": re.compile(
            r"{0}".format(query), re.IGNORECASE)})
        if len(query) < 5:
            cards.limit(100)
    else:
        cards = mongo.cards.find()
        cards.limit(100)
    cardlist = []
    for card in cards:
        directory_prefix = "{0}/../api".format(settings.PROJECT_ROOT)
        if card["front"].get("set") is None:
            set = card["front"]["partA"]["set"]
        else:
            set = card["front"]["set"]
        if card["front"].get("multiverse_id") is None:
            multiverse_id = card["front"]["partA"]["multiverse_id"]
        else:
            multiverse_id = card["front"]["multiverse_id"]
        image_url = "/static/images/{0}/{1}.jpg".format(set, multiverse_id)
        if os.path.exists(directory_prefix+image_url):
            cardlist.append({
                "name": card["front"]["name"],
                "multiverse_id": card["front"]["multiverse_id"],
                "set": card["front"]["set"],
                "image": image_url
            })
    return HttpResponse(json.dumps({"results": cardlist}), content_type="application/json")
