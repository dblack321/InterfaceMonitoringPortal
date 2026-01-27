from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from IMPapp.models import InterfaceAlert

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {"alerts": InterfaceAlert.objects.all()})

@login_required
def masterData(request):
    return render(request, "masterdata.html")

@login_required
def error404(request, context):
    return render(request, "404.html", context, status=404)