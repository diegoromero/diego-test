from django.shortcuts import render

from settings import dao
from gb.models import User

# Create your views here.
def home(request):
    User.create_user(username='c0', email='c@0.com', password='c0')
    return render(request, 'home_index.html',
                  {'title': 'Welcome'})
