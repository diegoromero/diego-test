from django.shortcuts import render, redirect
from django.utils import simplejson
from django.conf import settings

from settings import dao
from models import Document
from forms import DocumentForm

# Create your views here.
def home(request):
    '''Home view with a signin and singup form'''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
    else:
        form = DocumentForm()
    menus = dao.get_client_menus('c0')
    return render(request, 'home_index.html',
                  {'title': 'Welcome',
                   'form': form,
                   'menus': menus,
                   'json_menus': mongo2jstree_list(menus)})

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
