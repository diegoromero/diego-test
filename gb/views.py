import logging

from mongoengine import NotUniqueError, ValidationError
from gb.models import User
from django.contrib.auth import login, logout, authenticate

from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import simplejson

from settings import dao
from gb.forms import SectionForm, ItemForm, ItemInsert

logger = logging.getLogger('orders.views')

# Create your views here.
def home(request):
    '''Home view with a signin and singup form'''
    if request.user.is_authenticated():
        '''If the user is already registered it goes
        to the manager view'''
        return redirect('orders.views.manager_items')
    return render(request, 'home_index.html',
                  {'title': 'Welcome',
                   'template': 'home.html'})

def signin(request):
    '''Sign In view'''
    if request.user.is_authenticated():
        '''If the user is already registered it goes
        to the manager screen'''
        return redirect('orders.views.manager_items')
    if request.method == 'POST':
        username = request.POST['session[username]']
        password = request.POST['session[password]']
        try:
            '''Tries to log in, if succeds it redirects to the
            manager view'''
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('orders.views.manager_items')
            #return HttpResponseRedirect('/manager/items')
        except AttributeError:
            '''If it cant log in it gives a error message'''
            error = True
            error_value = 'Wrong username or password'
    else:
        error = False
        error_value = ''
        username = ''
    return render(request, 'home_index.html',
                  {'title': 'Sign In',
                   'template': 'signin.html',
                   'username': username,
                   'error': error,
                   'error_value': error_value})

def signup(request):
    if request.user.is_authenticated():
        '''If the user is already registered it goes
        to the manager screen'''
        return redirect('orders.views.manager_items')
    if request.method == 'POST':
        username = request.POST['user[name]']
        email = request.POST['user[email]']
        password = request.POST['user[user_password]']
        try:
            '''Tries to create a new client, if succeeds it logs in
            and redirects to the manager view'''
            User.create_user(username=username, email=email, password=password)
            #dao.create_client(username)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('orders.views.manager_items')
        except NotUniqueError, Argument:
            if 'username' in str(Argument):
                '''If the username is already registered it gives a
                error message'''
                error = {'username': True, 'email': False}
                error_value = 'Username already registered'
            elif 'email' in str(Argument):
                '''If the email is already registered it gives a
                error message'''
                error = {'username': False, 'email': True}
                error_value = 'Email already registered'
        except ValidationError:
            '''If the email submited doesnt have a valid form
            it gives a error message'''
            error = {'username': False, 'email': True}
            error_value = 'Not a valid email'
    else:
        error = {'username': False, 'email': False}
        error_value = username = email = ''
    return render(request, 'home_index.html',
                  {'title': 'Sign Up',
                   'template': 'signup.html',
                   'username': username,
                   'email': email,
                   'error': error,
                   'error_value': error_value})

def signout(request):
    '''Sign out view, it logs out and redirects to
    the home view'''
    logout(request)
    return redirect('orders.views.home')

def manager_items(request):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part
    if not request.user.is_authenticated():
        '''If the user is not logged in is redirected to the home view'''
        return redirect('orders.views.home')
    client_id = request.user.username
    items = dao.get_client_items(client_id)
    item_form = ItemForm()
    if request.method == 'POST':
        if request.is_ajax():
            if 'create_item' in request.POST:
                #This case handles the add items submit form
                item_form = ItemForm(request.POST)
                if item_form.is_valid():
                    #If the form is valid it enters here
                    cd = item_form.cleaned_data
                    name = cd['name']
                    price = cd['price']
                    description = cd['description']
                    dao.add_item(client_id, name, price, description)
            elif 'delete_item_id' in request.POST:
                #This case handles the delete item submit form
                item_id = request.POST['delete_item_id']
                dao.del_item(client_id, item_id)
            elif 'edit_item' in request.POST:
                #This case handles the updated items
                item_id = request.POST['item_id']
                name = request.POST['name']
                price = float(request.POST['price'])
                description = request.POST['description']
                dao.update_item(item_id, name = name, price = price, description = description)               
    return render(request, 'desktop_index.html',
                  {'items': items,
                   'item_form': item_form,
                   'template': 'manager_items.html',
                   'title': 'Manager'})

def manager_menus(request):
    #TODO: some refactoring,
    #      make the form validations work with the javascript part,
    #      make a clean decoupled design and python view code that is independent of
    #      the DB or JS code.
    if not request.user.is_authenticated():
        '''If the user is not logged in is redirected to the home view'''
        return redirect('orders.views.home')
    client_id = request.user.username
    try:
        menus = dao.get_client_menus(client_id)
    except TypeError:
        menus = []
    item_form = ItemForm()
    items = dao.get_client_items(client_id)
    if request.method == 'POST':
        if request.is_ajax():
            if 'add_menu' in request.POST:
                "Adds new menu to the db"
                dao.add_menu(request.POST['menu_title'], client_id)
            elif 'save_menu' in request.POST:
                "Saves the selected menu to the db"
                menu = jstree2mongo(request.POST)
                dao.update_menu_title(menu['id'], menu['title'])
                dao.update_menu_structure(menu['id'], menu['structure'])
            elif 'active_menu' in request.POST:
                "Sets the selected menu as active"
                menu_id = jstree2mongo(request.POST)['id']
                dao.update_active_menu(client_id, menu_id)
            elif 'item_form' in request.POST:
                item_form = ItemForm(request.POST)
                if item_form.is_valid():
                    cd = item_form.cleaned_data
                    name = cd['name']
                    price = cd['price']
                    description = cd['description']
                    if 'create_item' in request.POST:
                        dao.add_item(client_id, name, price, description)
                    elif 'edit_item' in request.POST:
                        item_id = request.POST['item_id']
                        dao.update_item(item_id, name = name, price = price, description = description)
    return render(request, 'desktop_index.html',
                  {'menus': menus, 'items': items,
                   'item_form': item_form,
                   'json_menus': mongo2jstree_list(menus),
                   'template': 'manager_menus.html',
                   'title': 'Manager'})


####################
# Helper functions #
####################

def mongo2jstree(menu):
    '''Changes the structure of the menu that uses mongo
    to a way jstree can read it
    P.S: This function can go to infinite depth'''
    tree = {'data': []}
    tree['data'].append({'data': menu['title'], 'attr': {'id': str(menu['_id']), 'rel': 'root'}, 'state': 'open', 'children': []})
    explore_mongo(menu, tree = tree)
    return simplejson.dumps(tree)

def mongo2jstree_list(menus):
    '''handles multiple menus with the function above ( mongo2jstree() )'''
    js_menus = []
    for menu in menus:
        js_menus.append(mongo2jstree(menu))
    return js_menus 

def explore_mongo(data, name='', level = 0, path=[], tree = {'data': []}):
    '''Explores the menu in mongo with recursion'''
    if 'structure' in data:
        for child in data['structure']:
            explore_mongo(data['structure'][child], name=child, tree = tree)
    elif type(data) is dict:
        level += 1
        ##### SECTIONS #####
        path.insert(level-1, name)
        path = path[:level]
        eval(path_2_list(path, level)).insert(0, {'data': name, 'attr': {'rel': 'section'},'state': 'open','children':[]})
        for child in data:
            explore_mongo(data[child], name=child, level=level, path=path, tree=tree)
    elif type(data) is list:
        level += 1
        ##### SUBSECTIONS ######
        path.insert(level-1, name)
        path = path[:level]
        eval(path_2_list(path, level)).insert(0, {'data': name, 'attr': {'rel': 'subsection'}, 'state': 'open','children':[]})
        level += 1
        for child in reversed(data):
            ##### ITEMS #####
            item = dao.get_item(child)
            eval(path_2_list(path, level)).insert(0, {'data': item['name'], 'attr': {'id': child, 'rel': 'item', 'name': item['name'], 'price': item['price'], 'description': item['description']}})


def path_2_list(path, level):
    '''Help enters the path(string) in the structure(list)''' 
    string = "tree['data'][0]['children']"
    for branch in path[:level-1]:
        string += "[0]['children']"
    return string
  
def jstree2mongo(tree):
    '''Changes the structure of the menu that uses jstree
    to the original way that mongo uses.
    P.S: This function can go to infinite depth'''
    body = simplejson.loads(tree['tree'])
    structure = {}
    explore_jstree(body[0], structure = structure)
    return {unicode('structure'): structure, unicode('title'): body[0]['data'], unicode('id'): body[0]['attr']['id']}

def dictizeString(string, dictionary, item_id = unicode(), subsection = unicode(), section = unicode()):
    '''Help enters the path(string) in the structure(dictionary)''' 
    while string.startswith('/'):
        string = string[1:]
    parts = string.split('/', 1)
    if len(parts) > 1:
        branch = dictionary.setdefault(parts[0], {})
        dictizeString(parts[1], branch, item_id = item_id, subsection = subsection, section = section)
    else:
        if item_id:
            if dictionary.has_key(parts[0]):
                 dictionary[parts[0]].append(item_id)
            else:
                 dictionary[parts[0]] = [item_id]
        if subsection:
            if not dictionary.has_key(parts[0]):
                 dictionary[parts[0]] = []
        if section:
            if not dictionary.has_key(parts[0]):
                 dictionary[parts[0]] = {}
                               
def explore_jstree(data, path = '', structure = {}):
    '''Explores the menu in jstree with recursion'''
    if data['attr']['rel'] == 'root':
        if 'children' in data:
            for child in data['children']:
                explore_jstree(child, structure = structure)
            
    elif data['attr']['rel'] == 'section': 
        path += '/' + data['data']
        dictizeString(path, structure, section = data['data'])
        if 'children' in data:
            for child in data['children']:
                explore_jstree(child, path = path, structure = structure)
                
    elif data['attr']['rel'] == 'subsection':
        path += '/' + data['data']
        dictizeString(path, structure, subsection = data['data'])
        if 'children' in data:
            for child in data['children']:
                explore_jstree(child, path = path, structure = structure)
                
    elif data['attr']['rel'] == 'item':
        dictizeString(path, structure, item_id = data['attr']['id'])
