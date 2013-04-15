from django.core.management.base import BaseCommand
from BeautifulSoup import BeautifulSoup
from gatherer.models import Set
import requests, re


class Command(BaseCommand):
    help = "Access gatherer to update the expansions list"

    def handle(self, *app_labels, **options):
        r_gatherer = requests.get("http://gatherer.wizards.com/Pages/Advanced.aspx")
        r_magicinfo = requests.get("http://magiccards.info/search.html")
        soup_gatherer = BeautifulSoup(r_gatherer.content)
        soup_magicinfo = BeautifulSoup(r_magicinfo.content)
        expansions = soup_gatherer.find('div', {'class': 'dynamicAutoCompleteContainer'}).findAll('a')
        expansions_magicinfo = soup_magicinfo.find("select", {"id": "edition"})
        for expansion in expansions:
            try:
                expansion_id = expansions_magicinfo.find("option", text=re.compile(expansion.text, re.IGNORECASE)).parent.get("value")
                set, created = Set.objects.get_or_create(title__iexact=expansion.text, defaults={"magiccard_info_id": expansion_id, "title": expansion.text})
                if not created:
                    set.magiccard_info_id = expansion_id
                    set.save()
            except Exception:
                print expansion.text
