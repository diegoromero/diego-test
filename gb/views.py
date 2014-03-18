from django.shortcuts import render

from settings import dao
from gb.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        '''If the user is already registered it goes
        to the manager view'''
        return redirect('www.google.com')
    User.create_user(username='c0', email='c@0.com', password='c0')
    return render(request, 'home_index.html',
                  {'title': 'Welcome'})
