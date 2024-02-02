from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#GET
@app.route('/', methods = ['GET'])
def inicio():
    return jsonify({"mensaje": "Bienvenido al asistente UNACHAT"}) 
#POST
@app.route('/chatbot/', methods =['POST'])
def chatbot():

    try:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return jsonify({"mensaje": client_ip}) 

    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Método no permitido'}), 405)

if __name__ == '__main__':
    app.run(debug=True)

