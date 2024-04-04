from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'index.html')

def login(request):
    template_name = 'my_login.html'

    return render(request, template_name)
