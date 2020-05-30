from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'messege': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'messege': 'The Store is already exists'}

        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json()
        except:
            return {'messege': 'An error occurred while creating the store'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'messege': 'The Store is already exists'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
