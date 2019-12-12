# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse
from sql_alchemy import database
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLAL   CHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


piadas = [
    {
        'id': '1',
        'pergunta': 'O que aconteceu com pintinho binario que nao tinha 1?',
        'resposta': 'Foi compilar e explodiu!'
    },
    {
        'id': '2',
        'pergunta': 'Eu gosto de iOS e Carlos Drummond?',
        'resposta': 'Carlos Drummond de Android'
    },
    {
        'id': '3',
        'pergunta': 'O que o C++ disse para o C?',
        'resposta': 'Voce nao tem classe!'
    },
    {
        'id': '4',
        'pergunta': 'Quanto programadores são necessários para trocar uma lâmpada?',
        'resposta': 'Nenhum, é problema de hardware.'
    },
    {
        'id': '5',
        'pergunta': 'O que é um terapeuta?',
        'resposta': '1024 gigapeutas.'
    },
    {
        'id': '6',
        'pergunta': 'Como o Nerd faz amigo oculto?',
        'resposta': '.amigo{visibility:hiden}'
    },
    {
        'id': '7',
        'pergunta': 'Seja \"int x = 10; int y = 10; print(x + y);\". Qual o nome do filme?',
        'resposta': 'O código dá 20.'
    }
]

class Piadas(Resource):

    def get(self):
        return {'piadas': [piada.json() for piada in PiadaModel.query.all()]}


class PiadaModel(database.Model):
    __tablename__ = 'piadas'
    id = database.Column(database.String, primary_key=True)
    pergunta = database.Column(database.String())
    resposta = database.Column(database.String())

    def __init__(self, id, pergunta, resposta):
        self.id = id
        self.pergunta = pergunta
        self.resposta = resposta

    def json(self):
        return {
            'id': self.id,
            'pergunta': self.pergunta,
            'resposta': self.resposta
        }

    @classmethod
    def buscar_piada(cls, id):
        piada = cls.query.filter_by(id=id).first()
        if piada:
            return piada
        return None

    def save_piada(self):
        database.session.add(self)
        database.session.commit()

    def update_piada(self, pergunta, resposta):
        self.pergunta = pergunta
        self.resposta = resposta

    def delete_piada(self):
        database.session.delete(self)
        database.session.commit()


class Piada(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('pergunta')
    atributos.add_argument('resposta')

    def buscar_piada(id):
        for piada in piadas:
            if piada['id'] == id:
                return piada
        return False

    def get(self, id):
        piada = PiadaModel.buscar_piada(id)
        if piada:
            return piada.json()
        return {'mensagem': 'piada nao encontrada.'}, 404
      
    def post(self, id):
        if PiadaModel.buscar_piada(id):
            return {
                "mensagem": "Piada id '{}' ja existe.".format(id)
            }, 400  # Bad Request

        dados = Piada.atributos.parse_args()
        piada = PiadaModel(id, **dados)

        try:
            piada.save_piada()
        except:
            return {"mensagem": "Ocorreu um erro ao salvar a piada."}, 500 #Internal Server Error
        return piada.json(), 201

    def put(self, id):
        dados = Piada.atributos.parse_args()
        piada = PiadaModel(id, **dados)

        piada_em_banco = PiadaModel.buscar_piada(id)

        if piada_em_banco:
            piada_em_banco.update_piada(**dados)
            piada_em_banco.save_piada()
            return piada_em_banco.json(), 200
        piada.save_piada()
        return piada, 201

    def delete(self, id):
        piada = PiadaModel.buscar_piada(id)
        if piada:
            piada.delete_piada()
            return {'mensagem': 'Piada apagada.'}
        return {'mensagem': 'Piada não encontrada.'}, 404


@app.before_first_request
def cria_database():
    database.create_all()


api.add_resource(Piadas, '/piadasnerd')
api.add_resource(Piada, '/piadasnerd/<string:id>')


cors = CORS(app, resources={r"/piadasnerd/*":{"origins":"*"}})

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)