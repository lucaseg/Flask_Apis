from flask import Flask,jsonify, request

app = Flask(__name__)
stores=[
    {
        'name':'My wonderful store',
        'items':[
            {
                'name':'My item',
                'price':15.99,
            }
        ]
    }
]

# Post /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)


# Get  /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    #if the store name matches, return it else return error
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'messege': 'store not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})


@app.route('/store/<string:name>/item')
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name']== request_data['name']:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify('messege':'is okey')
            
    return jsonify('messege':'error')


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})

    return jsonify({'messege': 'item not found'})

app.run(port=5000)