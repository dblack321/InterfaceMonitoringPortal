from django.http import HttpResponse
from django.shortcuts import render

from IMPapp.models import InterfaceAlert

# Create your views here.
def home(request):
    return render(request, "home.html", {"alerts": InterfaceAlert.objects.all()})

def masterData(request):
    return render(request, "masterdata.html")