# Create your views here.
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    if request.user.is_authenticated():
        return render(request, "index_auth.html")
    else:
        return render(request, "index_anon.html")

class PartialsView(View):

    @method_decorator(login_required)
    def get(self, request, template_name):
        return render(request, "partials/{0}".format(template_name))
