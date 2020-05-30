from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import autenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key='lucas'
api = Api(app)

jwt = JWT(app, autenticate, identity) # /auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/user-register')

app.run(port=5000, debug =True )