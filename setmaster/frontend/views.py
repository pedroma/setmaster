# Create your views here.
from django.shortcuts import render

def home(request):
    if request.user.is_authenticated():
        return render(request, "index_auth.html")
    else:
        return render(request, "index_anon.html")
