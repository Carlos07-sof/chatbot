from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot import ChatBot

app = Flask(__name__)
CORS(app)
chat = ChatBot()

@app.route('/')
def inicio():
    return jsonify({"mensaje": "Bienvenido al asistente UNACHAT"})

@app.route('/chatbot/', methods=['POST'])
def endpoint_chatbot():
    try:
        message = request.get_json().get('message')
        response = chat.response(message.lower())
        return jsonify({'mensaje': response}) if response else jsonify({'mensaje': 'Respuesta no encontrada'})
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Método no permitido'}), 405)

if __name__ == '__main__':
    app.run(debug=True)
