from django.conf.urls import patterns, url
from . import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^partials/(?P<template_name>.*)', views.PartialsView.as_view()),
)
