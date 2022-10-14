#! /usr/bin/env python

import os

from api import app

#from models.user import User
from api.endpoints import *
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://abdul:abdulrazzaq404@localhost/digisook"
from flask_mongoengine import MongoEngine
#db.create_all()
app.config['MONGODB_SETTINGS'] = {
    'db': 'digisook',
    'host': os.getenv('localhost', 'localhost:27017'),
}
db = MongoEngine()
db.init_app(app)


#db.init_app(app)
#db.create_all()
#from api.endpoints import test














if __name__ == "__main__":
    
    app.run(debug=True)
    
#from api.endpoints import test

