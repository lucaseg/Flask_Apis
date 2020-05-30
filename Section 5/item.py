from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    def find_by_bame(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return None

    @jwt_required()
    def get(self, name):
        item = self.find_by_bame(name)
        if item:
            return item
        else:
            return {'messege': 'Item not exist'}, 404

    def post(self, name):
        # Usado para crear un nuevo ITEM
        # 1) nos fijamos si este item a crear ya existe
        if self.find_by_bame(name):
            return {'messege: "An item with the name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        # 2) si no existe lo creamos en la DB
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"messege": "An error ocurred inserting the item"}, 500

        return item, 201

    def delete(self, name):
        global items
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name =?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'messege': 'Item Deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_bame(name)
        update_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(update_item)
            except:
                return {'messege': 'An error has been ocurred'}, 500
        else:
            try:
                self.update(update_item)
            except:
                return {'messege': 'An error has been ocurred'}, 500
        return item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query, (item['name'], item['price']))

        items = []
        for row in result:
            items.append({
                {"name": row[0], "price": row[1]}
            })
        connection.commit()
        connection.close()

        return {'items':items}