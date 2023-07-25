from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required # COM ESSA LIB VAMOS DEFINIR AS REQUISIÇÕES QUE PRECISAM DE LOGIN
from models.hotel import HotelModel
import sqlite3


#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


def normalize_path_params(
        cidade=None,
        estrelas_min= 0,
        estrelas_max = 5,
        diaria_min = 0,
        diaria_max = 10000,
        limit = 50,
        offset = 0, **dados
):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = "SELECT * FROM hoteis \
                    WHERE (estrelas >= ? and estrelas <= ?) \
                    and (diaria >= ? and diaria <= ?) \
                    LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM hoteis \
                    WHERE (estrelas >= ? and estrelas <= ?) \
                    and (diaria >= ? and diaria <= ?) \
                    and cidade = ? LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4]
            })

        return {'hoteis': hoteis}  # SELECT * FROM hoteis


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

    @jwt_required
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

    @jwt_required
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

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'hotel deleted'}, 200
        else:
            return {'message': 'hotel not found'}, 404
