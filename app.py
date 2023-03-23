from flask import Flask, jsonify, request
from flask_restx import Api, Resource

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import datetime


app = Flask(__name__)
api = Api(app)

cred = credentials.Certificate("./say-today-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://say-today-default-rtdb.asia-southeast1.firebasedatabase.app/'})


@api.route('/sayings')
class Sayings(Resource):
    # get random sayings
    def get(self):
        dir = db.reference('sayings')
        res = {'message': f'{dir.get()}'}
        return jsonify(res)
    
    # post saying
    def post(self):
        payload = request.get_json()

        dir = db.reference('system')
        next_id = dir.get()['next-id']
        dir.update({'next-id': next_id + 1})

        data = {
            'sayings': payload['saying'],
            'datetime': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            'up': 0,
            'down': 0
        }

        dir = db.reference(f'sayings/{next_id}')
        dir.update(data)
        
        res = {'message': 'message successfully uploaded'}
        return jsonify(res)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )