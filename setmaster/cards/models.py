from mongoengine.document import Document, EmbeddedDocument
from mongoengine import fields

CARD_TYPE_CHOICES = (
    "normal",
    "flip",
    "split",
    "double"
)

class CardDetail(EmbeddedDocument):
    pt = fields.StringField()
    colors = fields.ListField(fields.StringField(), required=False, default=list)
    number = fields.StringField(required=False)
    cmc = fields.IntField(required=False, default=0)
    flavor = fields.ListField(fields.StringField(), required=False, default=list)
    rules_text = fields.ListField(fields.StringField(), required=False, default=list)
    type = fields.StringField(required=True)
    mana = fields.ListField(fields.StringField(), default=list)
    name = fields.StringField(required=True)
    mtgcardinfo_img = fields.StringField()
    gath_img = fields.StringField(required=True)

class Card(Document):
    multiverse_id = fields.IntField(required=True, primary_key=True)
    set = fields.StringField(required=True)
    type = fields.StringField(choices=CARD_TYPE_CHOICES, max_length=10, required=True, default="normal")
    artist = fields.StringField()
    rarity = fields.StringField()
    othersets = fields.ListField(fields.StringField(), default=[])
    card_details = fields.EmbeddedDocumentField(CardDetail)
    extra_details = fields.EmbeddedDocumentField(CardDetail)

    meta = {'collection': 'cards'}
