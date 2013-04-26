from mongonaut.sites import MongoAdmin
from .models import Card, CardDetail

class CardAdmin(MongoAdmin):
    search_fields = ('multiverse_id',)

    # provide following fields for view in the DocumentListView
    list_fields = ('card_details.name')

Card.mongoadmin = CardAdmin()

CardDetail.mongoadmin = MongoAdmin()
