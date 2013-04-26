# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from catalog.models import Catalog, Item
from mongoengine.queryset import Q
from cards.models import Card
import json
import os


class CatalogApiView(View):

    http_method_names = ["get", "post", "delete", "create"]

    @method_decorator(login_required)
    def get(self, request):
        catalog = Catalog.objects.filter(user=request.user)

        def get_items(items):
            return [{'quantity': i.quantity, 'identifier': i.identifier, 'name': i.name} for i in items]
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
        name = Card.objects.get(multiverse_id=multiverse_id).card_details.name
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
def cards_list(request, query=""):
    cards = Card.objects.filter(Q(card_details__name__icontains=query) | Q(extra_details__name__icontains=query)).limit(20)
    cardlist = []
    for card in cards:
        directory_prefix = "{0}/../api".format(settings.PROJECT_ROOT)
        set = card.set
        multiverse_id = card.multiverse_id
        image_url = "/static/images/{0}/{1}.jpg".format(set, multiverse_id)
        if os.path.exists(directory_prefix + image_url):
            cardlist.append({
                "name": card.card_details.name,
                "multiverse_id": multiverse_id,
                "set": set,
                "image": image_url
            })
    return HttpResponse(json.dumps({"results": cardlist}), content_type="application/json")
