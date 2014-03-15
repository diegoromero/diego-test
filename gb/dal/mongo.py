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

from bootstrap import menus, items, clients

class MongoOrdersDAO(OrdersDAO):

    def __init__(self, bootstrap=True):
        self.client = mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
        self.db = eval('self.client.' + _MONGODB_NAME)
        if bootstrap:
            # load bootstrap data
            self.db.user.remove()
            self.db.menus.remove()
            self.db.menus.insert(menus)
            self.db.items.remove()
            self.db.items.insert(items)
            self.db.clients.remove()
            self.db.clients.insert(clients)
