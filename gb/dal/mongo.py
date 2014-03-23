import pymongo
import mongoengine
_MONGODB_USER = 'heroku'
_MONGODB_PASSWD = '67qXAWeeMw9GcsWbz9pCxC2N5aSZrblkTJrTVFj4csM6IUqF0cepykkVbOhENY1RYJ1Hc5Xu'
_MONGODB_HOST = 'oceanic.mongohq.com'
_MONGODB_NAME = 'app23051257'
_MONGODB_PORT = '10000'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s:%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_PORT, _MONGODB_NAME)

from django.conf.settings import _MONGODB
from bootstrap import menus, items, clients
from orders import OrdersDAO
from mongoengine.django.auth import User
from bson.objectid import ObjectId

class MongoOrdersDAO(OrdersDAO):

    def __init__(self, bootstrap=True):
        self.db = _MONGODB
        if bootstrap:
            # load bootstrap data
            self.db.user.remove()
            User.create_user(username='c0', email='c@0.com', password='c0')
            self.db.menus.remove()
            self.db.menus.insert(menus)
            self.db.items.remove()
            self.db.items.insert(items)
            self.db.clients.remove()
            self.db.clients.insert(clients)

    def get_client_menus_list(self, client_id):
        '''Gets the list of menus from the client'''
        return self.db.clients.find_one({'_id': client_id})['menus']
            
    def get_client_menus(self, client_id):
        '''Gets all the content of all the menus of the client'''
        menus_list = self.get_client_menus_list(client_id)
        menus = []
        for menu in menus_list:
            menus.append(self.db.menus.find_one({'_id': get_mongo_id(menu)}))
            menus[-1]['id'] = str(menus[-1]['_id'])
        return menus

    def get_item(self, item_id):
        '''Get the specified item from the DB'''
        mongo_id = get_mongo_id(item_id)
        item = self.db.items.find_one({'_id':mongo_id})
        item['id'] = item['_id']
        return item

def get_mongo_id(iid):
    try:
        mongo_id = ObjectId(iid)
    except pymongo.errors.InvalidId:
        mongo_id = iid
    return mongo_id
