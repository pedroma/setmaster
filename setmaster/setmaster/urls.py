from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^api/', include("api.urls")),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/login/', auth_login,
        {'template_name': 'registration/login.html',
         'authentication_form': AuthenticationForm,
         },
        name='auth_login'),
    (r'^accounts/', include(
     'smregistration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include("frontend.urls")),
)
