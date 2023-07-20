"""
na aula 35.Refatorando, nós criamos o pacote "Resources" e incluimos esse arquivo "hotel.py"
com a Classe "Hoteis" que é um recurso, usado em app.py
"""
from flask_restful import Resource, reqparse

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'alpha hotel',
        'estrelas': 4.5,
        'diaria': 420.1,
        'cidade': 'Rio Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'bravo hotel',
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

class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {'message': 'hotel not found'}, 404 # status code not found

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        dados = argumentos.parse_args()

        novo_hotel = {
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade'],
        }

        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        pass
    def delete(self, hotel_id):
        pass