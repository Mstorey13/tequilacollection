from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Collection, collection_schema, collections_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/collection', methods = ['POST'])
@token_required
def create_collection(current_user_token):
    tequila_name = request.json['tequila_name']
    type = request.json['type']
    abv = request.json['abv']
    region = request.json['region']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    collection = Collection(tequila_name, type, abv, region, user_token = user_token )

    db.session.add(collection)
    db.session.commit()

    response = collection_schema.dump(collection)
    return jsonify(response)

@api.route('/collection', methods = ['GET'])
@token_required
def get_collectopm(current_user_token):
    a_user = current_user_token.token
    collections = Collection.query.filter_by(user_token = a_user).all()
    response = collections_schema.dump(collections)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['GET'])
@token_required
def get_collection_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        collection = Collection.query.get(id)
        response = collection_schema.dump(collection)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/collection/<id>', methods = ['POST', 'PUT'])
@token_required
def update_collection(current_user_token,id):
    collection = Collection.query.get(id) 
    collection.tequila_name = request.json['tequila_name']
    collection.type = request.json['type']
    collection.abv = request.json['abv']
    collection.region = request.json['region']
    collection.user_token = current_user_token.token

    db.session.commit()
    response = collection_schema.dump(collection)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['DELETE'])
@token_required
def delete_collection(current_user_token, id):
    collection = Collection.query.get(id)
    db.session.delete(collection)
    db.session.commit()
    response = collection_schema.dump(collection)
    return jsonify(response)