from django.db import models
from django.utils.translation import ugettext_lazy as _


class Set(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    magiccard_info_id = models.CharField(_("Magic Cards Info ID"), help_text=_("Id used for each expansion in magiccards.info"), max_length=255, null=True, blank=True)


class Card(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    title_pt = models.CharField(_("Name in Portuguese"), max_length=255, null=True, blank=True)
    title_es = models.CharField(_("Name in Spanish"), max_length=255, null=True, blank=True)
    title_ct = models.CharField(_("Name in Chinese Traditional"), max_length=255, null=True, blank=True)
    title_cs = models.CharField(_("Name in Chinese Simplified"), max_length=255, null=True, blank=True)
    title_fr = models.CharField(_("Name in French"), max_length=255, null=True, blank=True)
    title_jp = models.CharField(_("Name in Japanese"), max_length=255, null=True, blank=True)
    title_ru = models.CharField(_("Name in Russian"), max_length=255, null=True, blank=True)
    title_it = models.CharField(_("Name in Italian"), max_length=255, null=True, blank=True)
    title_de = models.CharField(_("Name in German"), max_length=255, null=True, blank=True)
    title_kr = models.CharField(_("Name in Korean"), max_length=255, null=True, blank=True)
    title_br = models.CharField(_("Name in Portuguese (Brazil)"), max_length=255, null=True, blank=True)
    multiverseId_pt = models.IntegerField(_("Portuguese Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_es = models.IntegerField(_("Spanish Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_ct = models.IntegerField(_("Chinese Traditional Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_cs = models.IntegerField(_("Chinese Simplified Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_fr = models.IntegerField(_("French Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_jp = models.IntegerField(_("Japanese Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_ru = models.IntegerField(_("Russian Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_it = models.IntegerField(_("Italian Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_de = models.IntegerField(_("German Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_kr = models.IntegerField(_("Korean Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId_br = models.IntegerField(_("Portuguese (Brazil) Multiverse Identifier"), default=0, null=True, blank=True)
    multiverseId = models.IntegerField(_("Multiverse Identifier"), unique=True)
    cost = models.CharField(_("Cost"), max_length=255)
    cmc = models.IntegerField(_("Converted Mana Cost"))
    language = models.CharField(_("Language"), max_length=255)
    text = models.TextField(_("Rules text"), null=True, blank=True)
    flavor = models.TextField(_("Flavor text"), null=True, blank=True)
    strength = models.CharField(_("Creature strength"), help_text=_("Create strength if empty is its not applicable, '*' for special values, '3/1' for creatures and a single integer for Planeswalkers"), max_length=20)
    type = models.CharField(_("Card type"), max_length=255, default="")
    set = models.ForeignKey(Set, verbose_name=_("Set"))
    printings = models.ManyToManyField("Card", verbose_name=_("Printings"), help_text=_("Other printings of this card"), null=True, blank=True)
    collector_number = models.CharField(_("Collector number"), help_text=_("The number of this card inside a Set"), max_length=255, null=True, blank=True)
    rarity = models.CharField(_("Rarity"), max_length=255, null=True, blank=True)
    artist = models.CharField(_("Artist"), max_length=255, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ("frontend.card_detail", (self.multiverseId,))


class SubCard(models.Model):
    title = models.CharField(_("Title"), max_length=255, null=True, blank=True)
    title_pt = models.CharField(_("Name in Portuguese"), max_length=255, null=True, blank=True)
    title_es = models.CharField(_("Name in Spanish"), max_length=255, null=True, blank=True)
    title_ct = models.CharField(_("Name in Chinese Traditional"), max_length=255, null=True, blank=True)
    title_cs = models.CharField(_("Name in Chinese Simplified"), max_length=255, null=True, blank=True)
    title_fr = models.CharField(_("Name in French"), max_length=255, null=True, blank=True)
    title_jp = models.CharField(_("Name in Japanese"), max_length=255, null=True, blank=True)
    title_ru = models.CharField(_("Name in Russian"), max_length=255, null=True, blank=True)
    title_it = models.CharField(_("Name in Italian"), max_length=255, null=True, blank=True)
    title_de = models.CharField(_("Name in German"), max_length=255, null=True, blank=True)
    text = models.TextField(_("Rules text"), null=True, blank=True)
    flavor = models.TextField(_("Flavor text"), null=True, blank=True)
    strength = models.CharField(_("Creature strength"), help_text=_("Create strength is empty if its not applicable, '*' for special values, '3/1' for creatures and a single integer for Planeswalkers"), max_length=20)
    type = models.CharField(_("Card type"), max_length=255, default="")
    collector_number = models.CharField(_("Collector number"), help_text=_("The number of this card inside a Set"), max_length=255, null=True, blank=True)
    card = models.OneToOneField("Card", verbose_name=_("Card in case of card flip and/or transforms"), null=True)
