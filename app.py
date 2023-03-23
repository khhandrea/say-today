from flask import Flask, jsonify, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

data = []

@api.route('/sayings')
class Sayings(Resource):
    # get random sayings
    def get(self):
        res = {'message': 'Think different', 'data': f'{data}'}
        return jsonify(res)
    
    # post saying
    def post(self):
        payload = request.get_json()
        data.append(payload['saying'])
        res = {'message': f"i got {payload['saying']}!"}
        return jsonify(res)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )