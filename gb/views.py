from django.shortcuts import render, redirect

from settings import dao

# Create your views here.
def home(request):
    '''Home view with a signin and singup form'''
    if request.user.is_authenticated():
        '''If the user is already registered it goes
        to the manager view'''
        return redirect('www.google.com')
    return render(request, 'home_index.html',
                  {'title': 'Welcome'})
