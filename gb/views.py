from django.shortcuts import render

from settings import dao
from gb.models import User

# Create your views here.
def home(request):
    if request.method == 'POST':
        User.create_user(username=username, email=email, password=password)
    return render(request, 'home_index.html',
                  {'title': 'Welcome'})
