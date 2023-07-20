from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'alpha hotel',
        'estrelas': 4.5,
        'diaria': 420.1,
        'cidade': 'Rio Janeiro'
    },
    {
        'hotel_id': 'beta',
        'nome': 'beta hotel',
        'estrelas': 3.5,
        'diaria': 200.5,
        'cidade': 'Santa catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'charlie hotel',
        'estrelas': 4,
        'diaria': 352.1,
        'cidade': 'Santa catarina'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


api.add_resource(Hoteis, '/hoteis')

if __name__ == '__main__':
    app.run(debug=True)
