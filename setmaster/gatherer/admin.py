from django.contrib import admin
from gatherer.models import Set, Card, SubCard

class CardAdmin(admin.ModelAdmin):
    list_display = ("title", "collector_number","set")
    list_display_links = ("title", "collector_number")
    list_filter = ('set',)

admin.site.register(Set)
admin.site.register(Card,CardAdmin)
admin.site.register(SubCard)
