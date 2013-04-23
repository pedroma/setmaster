# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from catalog.models import Catalog, Item
import json
import pymongo
import os
import re

mongo = pymongo.MongoClient()["magic"]


class CatalogApiView(View):

    http_method_names = ["get", "post", "delete", "create"]

    @method_decorator(login_required)
    def get(self, request):
        catalog = Catalog.objects.filter(user=request.user)

        def get_items(items):
            return [{'quantity': i.quantity, 'identifier': i.identifier, 'name': i.name} for i in itecat.itemsms]
        catalogs = [
            {'id': cat.id, 'name': cat.name, 'items': cat.items.count(),
             'total_quantity': sum(cat.items.values_list('quantity', flat=True))} for cat in catalog
        ]
        return HttpResponse(json.dumps({"catalogs": catalogs}), content_type="application/json")

    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        catalog = Catalog(user=request.user, name=data.get("name"))
        catalog.save()
        return HttpResponse(json.dumps({"success": True}), content_type="application/json")

    @method_decorator(login_required)
    def create(self, request, id, multiverse_id):
        name = mongo.cards.find_one({"front.multiverse_id": int(multiverse_id)})["front"]["name"]
        catalog = Catalog.objects.get(id=id)
        if catalog.items.filter(identifier=multiverse_id).count() == 0:
            item = Item(name=name, quantity=1, identifier=multiverse_id)
            item.save()
            catalog.items.add(item)
        else:
            item = catalog.items.get(identifier=multiverse_id)
            item.quantity = item.quantity + 1
            item.save()
        return HttpResponse(json.dumps({"success": True}), content_type="application/json")

    @method_decorator(login_required)
    def delete(self, request, id):
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponse(json.dumps({"success": True}), content_type="application/json")


@login_required
def cards_list(request, query=None):
    if query is not None:
        cards = mongo.cards.find({"front.name": re.compile(
            r"{0}".format(query), re.IGNORECASE)})
        if len(query) < 5:
            cards.limit(10)
    else:
        cards = mongo.cards.find()
        cards.limit(10)
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
