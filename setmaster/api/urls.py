from django.conf.urls import patterns, include, url
from . import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^catalogs/$', views.catalog_list),
    url(r'^cards/$', views.cards_list),
    url(r'^cards/(?P<query>.*)$', views.cards_list),
)
