from django.shortcuts import render
import requests

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def books(request):
    title = request.POST['title']
    response = requests.get('https://frappe.io/api/method/frappe-library?page=2&title=' + title)
    print(title)
