from django.core.management.base import BaseCommand, CommandError
from gatherer.models import Set, Card, SubCard
from optparse import make_option
from BeautifulSoup import BeautifulSoup
import requests, re,os
from PIL import Image
from StringIO import StringIO
from urlparse import urlparse

LANGUAGES = ["28","pt-PT","es-ES","zh-TW","zn-CN","31","ja-JP","ru-RU","it-IT","de-DE"]
#28 english
#31 french
#zh-TW - Chinese traditional
#zn-CN - Chinese simplified

class Command(BaseCommand):
    args = "<expansion>"
    help = "Fetches information and images from the Magic Gatherer"

    option_list = BaseCommand.option_list + (
        make_option("-e","--expansion",
            action='store',
            dest='expansion',
            default=None,
            help='Fetch only this expansion'),
        make_option("-f","--from",
            action='store',
            dest='from',
            default=None,
            help='Fetch only from this expansion on (alphabetic order)'),
        make_option("-o","--output",
            action='store',
            dest='output_folder',
            default="",
            help='Set the output folder for the images.'),
        )

    def handle(self, *args, **options):
        output_folder = options["output_folder"]
        if output_folder[-1] != '/':
            output_folder = "%s/"%output_folder
        if options["expansion"] is not None:
            expansions = Set.objects.filter(title=options["expansion"])
            self.stdout.write("Fetching cards only for %s\n"%expansions[0].title)
        elif options["from"]:
            exps = Set.objects.all()
            expansions = []
            for exp in exps:
                if exp.title >= options["from"]:
                    expansions.append(exp)
        else:
            expansions = Set.objects.all()
        if not expansions:
            raise CommandError("Expansion %s was not found. Does it really exist?" % options["expansion"])

        #OK. Got the expansions list
        for expansion in expansions:
            url = "http://gatherer.wizards.com/Pages/Search/Default.aspx?output=compact&sort=cn+&action=advanced&set=[\"%s\"]"%expansion.title
            r = requests.get(url,cookies={'CardDatabaseSettings':'0=1&1=28&2=0&14=1&3=13&4=0&5=1&6=15&7=0&8=1&9=1&10=19&11=7&12=8&15=1&16=0&13='})
            soup = BeautifulSoup(r.content)
            cards = soup.findAll('tr',{'class':re.compile(r'\bcardItem\b')})
            self.stdout.write("Fetching %s cards in %s\n"%(len(cards),expansion.title))
            for card in cards:
                mana = card.find('td', {'class':'mana top'}).findAll('img')
                mana_cost = []
                name_link = card.find('td', {'class':'name top'}).find('a')
                name = name_link.text.encode('utf-8')
                id = dict(map(lambda x: x.split("="),urlparse(name_link.get('href')).query.split("&")))['multiverseid']
                for img in mana:
                    image = img.get('src')
                    alt = img.get('alt',"")
                    if not os.path.exists("%saux_images/%s.png"%(output_folder,alt)) and image is not None:
                        #get image
                        url_image = "http://gatherer.wizards.com/%s&size=large" % image
                        url_image = url_image.replace("size=small&", "")
                        req_img = requests.get(url_image)
                        try:
                            i = Image.open(StringIO(req_img.content))
                        except:
                            req_img = requests.get(url_image.replace("size=large","size=medium"))
                            i = Image.open(StringIO(req_img.content))
                        i.save("%saux_images/%s.png"%(output_folder,alt),"PNG")
                    mana_cost.append(alt)
                if not os.path.exists("%simages/%s/%s.png"%(output_folder,expansion.title,id)):
                    self.stdout.write("Fetching image for card %s\n" % name)
                    req_img = requests.get("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card"%id)
                    i = Image.open(StringIO(req_img.content))
                    if not os.path.exists("%simages/%s"%(output_folder,expansion.title)):
                        os.mkdir("%simages/%s"%(output_folder,expansion.title))
                    i.save("%simages/%s/%s.png"%(output_folder,expansion.title,id))
                type = card.find('td',{'class':'type top'}).text.encode('utf-8')
                power,defense = [v.text for v in card.findAll('td',{'class':'numerical top'})]
                if not power and not defense:
                    strength = ""
                elif not power:
                    strength = defense
                else:
                    strength = "%s/%s"%(power,defense)
                cmc = 0
                for i in mana_cost:
                    try:
                        cmc = cmc + int(i)
                    except:
                        if i != "X":
                            cmc = cmc + 1
                try:
                    card_obj, created = Card.objects.get_or_create(multiverseId=id,defaults={"title":name.decode('utf8'),"type":type,"strength":strength,"cost":mana_cost,"cmc":cmc,"set":expansion})
                except Exception as inst:
                    self.stdout.write("Problem creating card http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s\n\t %s\n"%(id,inst))
                    break

                # NOW got to the specific page for this card and retrieve the rest of the info
                try:
                    url = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s"%id
                    r = requests.get(url)
                except:
                    self.stdout.write("Error fetching %s\n"%url)
                    url = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%s"%id
                    r = requests.get(url)
                soup = BeautifulSoup(r.content)
                if soup.find("div",{'id':"ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_componentWrapper"}) is None or soup.find("div",{'id':"ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl07_componentWrapper"}):
                    # This is a simple card. No flipping and no transformations
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'}).findAll('div',{'class':'cardtextbox'})
                        text = '<br/>'.join([t.renderContents() for t in txt])
                        card_obj.text = text
                    except:
                        # card may not have text
                        pass
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText'}).findAll('div',{'class':'cardtextbox'})
                        text = '<br/>'.join([t.renderContents() for t in txt])
                        card_obj.flavor = text
                    except:
                        # card may not have flavor text
                        pass
                    try:
                        collector_number = soup.find("div",{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_numberRow'}).find('div',{'class':'value'}).text
                        card_obj.collector_number = collector_number
                    except:
                        # it seems that not all cards have a collector number
                        # http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=3134
                        pass
                    try:
                        rarity = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow'}).find('div',{'class':'value'}).text
                        card_obj.rarity = rarity
                    except:
                        self.stdout.write("Problem getting the rarity of %s\n"%url)
                        pass
                    try:
                        artist = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit'}).find('a').text
                        card_obj.artist = artist
                    except:
                        artist = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit'}).text
                        card_obj.artist = artist

                    # discover multiverse related cards
                    try:
                        card_links = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_otherSetsValue'}).findAll('a')
                        for a in card_links:
                            try:
                                card_obj.printings.add(Card.objects.get(multiverseId=a.get('href').split('=')[-1]))
                            except:
                                # card may have not been created yet
                                pass
                    except:
                        # if there is only one printing of this card
                        pass
                    card_obj.save()
                else:
                    # This is a complex card. Either a transformation or a flip
                    # CARD NAME
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_nameRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_nameRow"
                    # TEXT
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_textRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_textRow"
                    # FLAVOR TEXT
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_flavorRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_flavorRow"
                    # COLLECTOR NUMBER
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_numberRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_numberRow"
                    # STRENGTH
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_ptRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_ptRow"
                    # RARITY
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_rarityRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_rarityRow"
                    # ARTIST
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_artistRow"
                    # "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_artistRow"
                    sub_card,created = SubCard.objects.get_or_create(card=card_obj)
                    txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_nameRow'}).find('div',{'class':'value'}).text
                    sub_card.title = txt
                    type = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_typeRow'}).find('div',{'class':'value'}).text
                    sub_card.type = txt
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_textRow'}).findAll('div',{'class':'value'}).text
                        sub_card.title = txt
                    except:
                        # card may not have text
                        pass
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_textRow'}).findAll('div',{'class':'cardtextbox'})
                        text = '<br/>'.join([t.renderContents() for t in txt])
                        sub_card.text = text
                    except:
                        # card may not have text
                        pass
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_flavorRow'}).findAll('div',{'class':'cardtextbox'})
                        text = '<br/>'.join([t.renderContents() for t in txt])
                        card_obj.flavor = text
                    except:
                        # card may not have flavor text
                        pass
                    try:
                        txt = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_flavorRow'}).findAll('div',{'class':'cardtextbox'})
                        text = '<br/>'.join([t.renderContents() for t in txt])
                        sub_card.flavor = text
                    except:
                        # card may not have flavor text
                        pass
                    try:
                        collector_number = soup.find("div",{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_numberRow'}).find('div',{'class':'value'}).text
                        card_obj.collector_number = collector_number
                    except:
                        # it seems that not all cards have a collector number
                        # http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=3134
                        pass
                    try:
                        collector_number = soup.find("div",{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl06_numberRow'}).find('div',{'class':'value'}).text
                        sub_card.collector_number = collector_number
                    except:
                        # it seems that not all cards have a collector number
                        # http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=3134
                        pass
                    try:
                        rarity = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_rarityRow'}).find('div',{'class':'value'}).text
                        card_obj.rarity = rarity
                    except:
                        self.stdout.write("Problem getting the rarity of %s\n"%url)
                        pass
                    try:
                        artist = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl05_artistRow'}).find('a').text
                        card_obj.artist = artist
                    except:
                        artist = soup.find('div',{'id':'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ArtistCredit'}).text
                        card_obj.artist = artist

                    # discover multiverse related cards
                    # until now flip and transform cards are unique to a specific set.
                    sub_card.save()
                    card_obj.sub_card = sub_card
                    card_obj.save()

                    pass

                # lets take care of languages
                url = "http://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=%s"%id
                try:
                    r = requests.get(url)
                except:
                    self.stdout.write(url+"\n")
                    r = requests.get(url)
                soup = BeautifulSoup(r.content)
                for card in soup.findAll('tr',{'class':re.compile(r'\bcardItem\b')}):
                    tds = card.findAll('td')
                    lang = tds[1].text
                    value = tds[0].find('a').text
                    mid = tds[0].find('a').get('href').split("=")[-1]
                    if lang == "German":
                        card_obj.title_de = value
                        card_obj.multiverseId_de = mid
                    elif lang == "Italian":
                        card_obj.title_it = value
                        card_obj.multiverseId_it = mid
                    elif lang == "French":
                        card_obj.title_fr = value
                        card_obj.multiverseId_fr = mid
                    elif lang == "Japanese":
                        card_obj.title_jp = value
                        card_obj.multiverseId_jp = mid
                    elif lang == "Russian":
                        card_obj.title_ru = value
                        card_obj.multiverseId_ru = mid
                    elif lang == "Chinese Simplified":
                        card_obj.title_cs = value
                        card_obj.multiverseId_cs = mid
                    elif lang == "Chinese Traditional":
                        card_obj.title_ct = value
                        card_obj.multiverseId_ct = mid
                    elif lang == "Portuguese":
                        card_obj.title_pt = value
                        card_obj.multiverseId_pt = mid
                    elif lang == "Spanish":
                        card_obj.title_es = value
                        card_obj.multiverseId_es = mid
                    elif lang == "Korean":
                        card_obj.title_kr = value
                        card_obj.multiverseId_kr = mid
                    elif lang == "Portuguese (Brazil)":
                        card_obj.title_br = value
                        card_obj.multiverseId_br = mid
                    else:
                        self.stdout.write("Please add the language %s to the script\n"%lang)
                card_obj.save()
