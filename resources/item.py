from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'messege': 'Item not exist'}, 404

    def post(self, name):
        # Usado para crear un nuevo ITEM
        # 1) nos fijamos si este item a crear ya existe
        if ItemModel.find_by_name(name):
            return {'messege: "An item with the name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        # 2) si no existe lo creamos en la DB
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"messege": "An error ocurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'messege': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
