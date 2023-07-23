"""
na aula 35.Refatorando, nós criamos o pacote "Resources" e incluimos esse arquivo "hotel.py"
com a Classe "Hoteis" que é um recurso, usado em app.py
"""
from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM hoteis


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="the field 'nome' cannot be blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="the field 'estrelas' cannot be blank")
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade', type=str)

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'hotel not found'}, 404 # status code not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id "{hotel_id}" already exists.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        try:
            hotel_objeto.save_hotel()
        except:
            return {'message': 'internal error'}, 500
        return hotel_objeto.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            try:
                hotel_encontrado.update_hotel(**dados)
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'internal error'}, 500
            return hotel_encontrado.json(), 200
        else:
            hotel_objeto = HotelModel(hotel_id, **dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'internal error'}, 500
            return hotel_objeto.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'hotel deleted'}, 200
        else:
            return {'message': 'hotel not found'}, 404
