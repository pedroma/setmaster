from django.conf.urls import patterns, url
from . import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^catalogs$', views.CatalogApiView.as_view()),
    url(r'^catalogs/(?P<id>\d+)$', views.CatalogApiView.as_view()),
    url(r'^cards/$', views.cards_list),
    url(r'^cards/(?P<query>.*)$', views.cards_list),
)
