from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from models.usuario import UserModel


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="the field 'login' cannot be blank")
argumentos.add_argument('senha', type=str, required=True, help="the field 'senha' cannot be blank")

class User(Resource):
    # endpoint: /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404 # status code not found

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'user deleted'}, 200
        else:
            return {'message': 'user not found'}, 404


class UserRegister(Resource):
    # endpoint: /cadastro
    def post(self):
        dados = UserRegister.argumentos.parse_args()
        user = UserModel(**dados)
        # verificando se user já existe no banco
        if UserModel.find_by_login(dados['login']):
            return {'message': f'the user {dados["login"]} already exists'}, 500
        try:
            user.save_user()
        except:
            return {'message': 'internal error'}, 500
        return {'message': f'user created! {user.json()}'}, 201


class UserLogin(Resource):
    # endpoint: /login
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        try:
            # verificando se user e senha batem com o banco, se sim cria token
            if user and safe_str_cmp(user.senha, dados['senha']):
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {'message': 'username or password is incorrect'}, 401 # nao autorizado
        except:
            return {'message': 'internal error'}, 500