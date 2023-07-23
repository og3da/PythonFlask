"""
na aula 35.Refatorando, nós criamos o pacote "Resources" e incluimos esse arquivo "hotel.py"
com a Classe "Hoteis" que é um recurso, usado em app.py
"""
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

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
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'hotel not found'}, 404 # status code not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id "{hotel_id}" already exists.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        hotel_objeto.save_hotel()
        return hotel_objeto.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        else:
            hoteis.append(novo_hotel)
            return novo_hotel, 201

    def delete(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hoteis.remove(hotel)
            return {'message': 'hotel deleted'}, 200
        else:
            return {'message': 'hotel not found'}, 404
