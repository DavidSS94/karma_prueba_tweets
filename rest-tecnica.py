# rest-tecnica.py

import dateutil.parser
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config['MONGO_DBNAME'] = 'MiniMetrics'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/app'

mongo = PyMongo(app)

# Endpoint 1: Regresa: Total Tweets, Total Usuarios Unicos, Menciones Unicas, Total Hastags Unicos
# @app.route('/totales', methods=['POST'])
@app.route('/endpoint_1', methods=['POST'])
def get_all_totals():
    tweets = mongo.db.tweets
    output = []
    searchId = request.json['searchId']
    initialDate = dateutil.parser.parse(request.json['initialDate'])
    finalDate = dateutil.parser.parse(request.json['finalDate'])
    if id_exist(searchId):
        if compare_data(searchId, initialDate, finalDate):
            if compare_dates(initialDate, finalDate):
                totaltweets = tweets.find({
                    'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } ,
                }).count()
                totalusers = tweets.aggregate([
                    { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                    { '$group': { '_id': "$usuario.preferredUsername" }},
                    { '$count': "totalusers" }
                ])
                totalhashtags = tweets.aggregate([
                    { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                    { '$project': { '_id': 0, 'hashtags': 1 } },
                    { '$unwind': '$hashtags'},
                    { '$group': { '_id': '$hashtags', 'conteo': { '$sum': 1 } }},
                    { '$project': { '_id': 0, 'hastag': '$_id', 'conteo': 1 } },
                    { '$count': "totalhastags" },
                ])
                totalmentions = tweets.aggregate([
                    { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                    { '$project': { '_id': 0, 'menciones': 1 } },
                    { '$unwind': '$menciones'},
                    { '$group': { '_id': '$menciones', 'conteo': { '$sum': 1 } }},
                    { '$project': { '_id': 0, 'mencion': '$_id', 'conteo': 1 } },
                    { '$count': "totalmencionesunicas" }
                ])
                # for q in tweets:
                output.append({'totaltweets': totaltweets})
                for q in totalusers:
                    output.append({'totalusers': q['totalusers']})
                for q in totalhashtags:
                    output.append({'totalhastags': q['totalhastags']})
                for q in totalmentions:
                    output.append({'totalmencionesunicas': q['totalmencionesunicas']})
                return jsonify({'result': output})
            else:
                return jsonify({'Error': 'La fecha inicial debe ser menor que la final'})
        else:
            return jsonify({'Error': 'Ingrese todos los datos'})
    else:
        return jsonify({'Error': 'La busqueda solicitada, no existe'})


# Endpoint 2: Usuario con más tweets
# @app.route('/unique_users', methods=['POST'])
@app.route('/endpoint_2', methods=['POST'])
def get_unique_users():
    tweets = mongo.db.tweets
    output = []
    searchId = request.json['searchId']
    initialDate = dateutil.parser.parse(request.json['initialDate'])
    finalDate = dateutil.parser.parse(request.json['finalDate'])
    if id_exist(searchId):
        if compare_data(searchId, initialDate, finalDate):
            if compare_dates(initialDate, finalDate):
                count = tweets.aggregate([
                        { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                        { '$project': { '_id': 0, 'usuario': 1 } },
                        { '$group': { '_id': "$usuario.preferredUsername", 'conteo': { '$sum': 1 }, }},
                        { '$project': { '_id': 0, 'usuario': '$_id', 'conteo': 1 } },
                        { '$sort': { 'conteo': -1} },
                        { '$limit': 1 },
                    ])
                for q in count:
                    output.append({'usuario': q['usuario'], 'conteo': q['conteo']})
                return jsonify({'result': output})
            else:
                return jsonify({'Error': 'La fecha inicial debe ser menor que la final'})
        else:
            return jsonify({'Error': 'Ingrese todos los datos'})
    else:
        return jsonify({'Error': 'La busqueda solicitada, no existe'})

# Endpoint 3: Top 10 Hastags más repetidos
# @app.route('/top_hashtags', methods=['POST'])
@app.route('/endpoint_3', methods=['POST'])
def get_top_hastags():
    tweets = mongo.db.tweets
    output = []
    searchId = request.json['searchId']
    initialDate = dateutil.parser.parse(request.json['initialDate'])
    finalDate = dateutil.parser.parse(request.json['finalDate'])
    if id_exist(searchId):
        if compare_data(searchId, initialDate, finalDate):
            if compare_dates(initialDate, finalDate):
                count = tweets.aggregate([
                    { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                    { '$project': { '_id': 0, 'hashtags': 1 } },
                    { '$unwind': '$hashtags' },
                    { '$group': { '_id': '$hashtags', 'conteo': { '$sum': 1 } }},
                    { '$project': { '_id': 0, 'hashtag': '$_id', 'conteo': 1 } },
                    { '$sort': { 'conteo': -1 } },
                    { '$limit': 10 },
                ])
                for q in count:
                    output.append({'hashtag': q['hashtag'], 'conteo': q['conteo']})
                return jsonify({'result': output})
            else:
                return jsonify({'Error': 'La fecha inicial debe ser menor que la final'})
        else:
            return jsonify({'Error': 'Ingrese todos los datos'})
    else:
        return jsonify({'Error': 'La busqueda solicitada, no existe'})

# Endpoint 4: Tipo de tweet y porcentaje
# @app.route('/tweet_types', methods=['POST'])
@app.route('/endpoint_4', methods=['POST'])
def get_tweets_type():
    tweets = mongo.db.tweets
    output = []
    searchId = request.json['searchId']
    initialDate = dateutil.parser.parse(request.json['initialDate'])
    finalDate = dateutil.parser.parse(request.json['finalDate'])
    total = tweets.count({ 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate }})
    if id_exist(searchId):
        if compare_data(searchId, initialDate, finalDate):
            if compare_dates(initialDate, finalDate):
                count = tweets.aggregate([
                    { '$match': { 'busquedaId': searchId, 'postedTime': { '$gte': initialDate, '$lt': finalDate, } }},
                    { '$group': { '_id': "$verb", 'conteo': { '$sum': 1 }, }},
                    { '$project': { '_id': 0, 'type': { '$cond': { 'if': { '$eq': ["$_id", "post"] }, 'then': "original", 'else': "retweet" } }, "conteo": 1, "percentage": { '$divide': [{ '$multiply': [ 100, '$conteo'  ]}, total ]} }},
                ])
                for q in count:
                    output.append({'type': q['type'], 'conteo': q['conteo'], 'percentage': q['percentage']})
                return jsonify({'result': output})
            else:
                return jsonify({'Error': 'La fecha inicial debe ser menor que la final'})
        else:
            return jsonify({'Error': 'Ingrese todos los datos'})
    else:
        return jsonify({'Error': 'La busqueda solicitada, no existe'})

def id_exist(search):
    busquedas = mongo.db.busquedas
    id = search
    output = []
    resultado = busquedas.find({ '_id': ObjectId(id)}).count()
    # return jsonify({'result': resultado})
    if str(resultado) == '1':
        return True
    else:
        return False


def compare_dates(initial, final):
    if initial < final:
        return True
    return False

def compare_data(id, initialDate, finalDate):
    if id and initialDate and finalDate:
        return True
    else:
        False

if __name__ == '__main__':
    app.run(debug=True)
