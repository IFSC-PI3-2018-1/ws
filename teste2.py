#!/usr/bin/env python
import couchdb
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth
#from flask.ext.httpauth import HTTPBasicAuth
#from flask import couchdb
#from flaskext.couchdbkit import CouchDBKit

couchserver = couchdb.Server("http://localhost:5984/")

def deleta_banco(banco):
    del couchserver[banco]
    return 0

def mostra_bancos():
    print('\n')
    for dbname in couchserver:
        print(dbname)
    print('\n')
    return 0
    
#mostra_bancos()

def cria_banco(banco):
    dbname = banco
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)
    return 0

#cria_banco("fruit")
#mostra_bancos()

#del couchserver["teste123"]

auth = HTTPBasicAuth()
app = Flask(__name__)

categoria = [
    {
    'nid' : 1,
    'modo_escolhido' : 'azul'
    }
]

imagens_enviadas = []
#    {
#    'nid' : 1,
#    'origem' : 'rasp',
#    'conteudo' : '123818713h1cc31hc1hu'
#    },
#    {
#    'nid' : 2,
#    'origem' : 'app',
#    'conteudo' : 'dhuy23y278ndh2uy'
#    }
#]

eventos = []
#    {
#    'nid' : 1,
#    'origem' : 'app',
#    'timestamp' : '123456',
#    'tipo_evento' : 'get_image'
#    },
#    {
#    'nid' : 2,
#    'origem' : 'rasp',
#    'timestamp' : '222222',
#    'tipo_evento' : 'send_image'
#    }
#]
# Como invocar na linha de comando
#
# curl -i http://localhost:5000/livros
#

@app.route('/get_image/<string:cat>', methods=['GET'])#abrir socket, enviando 'cat', receber a imagem, inserir a imagem no banco e retornar o texto da imagem.
def get_image(cat):
         return jsonify({'image':'aaaaaa' })


@app.route('/categoria', methods=['GET'])
def obtem_modos():
     return jsonify({'categoria': ['amarelo','azul','purpura']})


@app.route('/imagens_enviadas', methods=['GET'])
def obtem_imagens():
    return jsonify({'imagens_enviadas': imagens_enviadas})

@app.route('/eventos', methods=['GET'])
def obtem_eventos():
    return jsonify({'eventos': eventos})
# Como invocar na linha de comando
#
# curl -i http://localhost:5000/livros/1
#
@app.route('/imagens_enviadas/<int:nidimagens>', methods=['GET'])
def detalhe_imagens(nidimagens):
    resultado = [resultado for resultado in imagens_enviadas if resultado['nid'] == nidimagens]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'imagens': resultado[0]})

@app.route('/eventos/<int:nideventos>', methods=['GET'])
def detalhe_eventos(nideventos):
    resultado = [resultado for resultado in eventos if resultado['nid'] == nideventos]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'evento': resultado[0]})

# Como invocar na linha de comando
#
# curl -i -X DELETE http://localhost:5000/livros/2
#
@app.route('/categoria/<int:nid_tipo_modos>', methods=['DELETE'])
def excluir_modos(tipo_modos):
        resultado = [resultado for resultado in categoria if resultado['nid'] == tipo_modos]
        if len(resultado) == 0:
                abort(404)
        categoria.remove(resultado[0])
        return jsonify({'resultado': True})

@app.route('/imagens_enviadas/<int:nidimagens>', methods=['DELETE'])
def excluir_imagens(nidimagens):
    resultado = [resultado for resultado in imagens_enviadas if resultado['nid'] == nidimagens]
    if len(resultado) == 0:
        abort(404)
    imagens_enviadas.remove(resultado[0])
    return jsonify({'resultado': True})

@app.route('/eventos/<int:nideventos>', methods=['DELETE'])
def excluir_eventos(nideventos):
    resultado = [resultado for resultado in eventos if resultado['nid'] == nideventos]
    if len(resultado) == 0:
        abort(404)
    eventos.remove(resultado[0])
    return jsonify({'resultado': True})

# Como invocar na linha de comando
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"titulo":"O livro","autor":"Joao"}' http://localhost:5000/livros
#
@app.route('/categoria', methods=['POST'])
def criar_modos():
    if not request.json or not 'modo_escolhido' in request.json:
        abort(400)
    excluir_modos('azul')
    modo = {
        'nid': categoria[-1]['nid'] + 1,
        'modo_escolhido': request.json['modo_escolhido']
    }
    categoria.append(modo)
    return jsonify({'modo': modo}), 201

@app.route('/imagens_enviadas', methods=['POST'])
def criar_imagens():
    if not request.json or not 'origem' in request.json:
        abort(400)
    imagens = {
        'nid': imagens_enviadas[-1]['nid'] + 1,
        'origem': request.json['origem'],
        'conteudo': request.json['conteudo']
    }
    imagens_enviadas.append(imagens)
    return jsonify({'imagens': imagens}), 201

@app.route('/eventos', methods=['POST'])
def criar_eventos():
    if not request.json or not 'origem' in request.json:
        abort(400)
    evento = {
        'nid': eventos[-1]['nid'] + 1,
        'origem': request.json['origem'],
        'timestamp': request.json['timestamp'],
        'tipo_evento': request.json['tipo_evento']
    }
    eventos.append(evento)
    return jsonify({'evento': evento}), 201

# Como invocar na linha de comando
#1
# curl -i -H "Content-Type: application/json" -X PUT -d '{"titulo":"Novo Titulo"}' http://localhost:5000/livros/2
#
@app.route('/imagens_enviadas/<int:nidimagens>', methods=['PUT'])
def atualizar_imagens(nidimagens):
    resultado = [resultado for resultado in imagens_enviadas if resultado['nid'] == nidimagens]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'origem' in request.json and type(request.json['origem']) != unicode:
        abort(400)
    if 'conteudo' in request.json and type(request.json['conteudo']) != unicode:
        abort(400)
    resultado[0]['origem'] = request.json.get('origem', resultado[0]['origem'])
    resultado[0]['conteudo'] = request.json.get('conteudo', resultado[0]['conteudo'])
    return jsonify({'imagens': resultado[0]})

@app.route('/eventos/<int:nideventos>', methods=['PUT'])
def atualizar_eventos(nideventos):
    resultado = [resultado for resultado in eventos if resultado['nid'] == nideventos]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'origem' in request.json and type(request.json['origem']) != unicode:
                abort(400)
    if 'timestamp' in request.json and type(request.json['timestamp']) != unicode:
        abort(400)
    if 'tipo_evento' in request.json and type(request.json['tipo_evento']) != unicode:
        abort(400)
    resultado[0]['origem'] = request.json.get('origem', resultado[0]['origem'])
    resultado[0]['timestamp'] = request.json.get('timestamp', resultado[0]['timestamp'])
    resultado[0]['tipo_evento'] = request.json.get('tipo_evento', resultado[0]['tipo_evento'])
    return jsonify({'evento': resultado[0]})

@app.route('/categoria/<int:nid_categoria>', methods=['PUT'])
def atualizar_categoria(nid_categoria):
    resultado = [resultado for resultado in categoria if resultado['nid'] == nid_categoria]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'modo_escolhido' in request.json and type(request.json['modo_escolhido']) is not str:
        abort(400)
    resultado[0]['modo_escolhido'] = request.json.get('modo_escolhido', resultado[0]['modo_escolhido'])
    return jsonify({'mod': resultado[0]})


#### Autenticacao simples ####
# Como invocar na linha de comando
#
# curl -u aluno:senha123 -i http://localhost:5000/livrosautenticado
#
@app.route('/login', methods=['POST'])
#@auth.login_required
def login():
    return jsonify({'ok': 1})

@app.route('/eventosautenticado', methods=['GET'])
@auth.login_required
def obtem_eventos_autenticado():
    return jsonify({'evento': eventos})

# Autenticacao simples
@auth.get_password
def get_password(username):
    if username == 'aluno':
        return 'senha123'
    return None
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'erro': 'Acesso Negado'}), 403)
##############################
# Para apresentar erro 404 HTTP se tentar acessar um recurso que nao existe
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)
if __name__ == "__main__":
    print("Servidor no ar!")
    app.run(host='0.0.0.0', debug=True)
