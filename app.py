from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from random import randrange
import datetime

cred = credentials.Certificate("./say-today-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://say-today-default-rtdb.asia-southeast1.firebasedatabase.app/'})

app = Flask(__name__)
api = Api(app, version='1.0', title='say today API', description='Endpoint API of say today', doc='/api-docs')
sayings = api.namespace('sayings', description='get or post sayings')

model = api.model('Model', {
    'saying': fields.String
})

@api.route('/sayings')
class Sayings(Resource):
    # get random sayings
    def get(self):
        res = {}

        dir = db.reference('system/next-id')
        next_id = dir.get()

        if next_id == 1:
            res['message'] = 'There is no saying...'
        else:
            selected_id = randrange(1, next_id)
            dir = db.reference(f'sayings/{selected_id}')
            res['message'] = f"{dir.get()['message']}"
        
        return jsonify(res)
    
    # post saying
    @api.expect(model)
    def post(self):
        payload = request.get_json()

        dir = db.reference('system')
        next_id = dir.get()['next-id']
        dir.update({'next-id': next_id + 1})

        data = {
            'message': payload['saying'],
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