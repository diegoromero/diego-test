from django.shortcuts import render

from settings import dao

# Create your views here.
def home(request):
    return render(request, 'home_index.html',
                  {'title': 'Welcome'})
