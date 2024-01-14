from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot import ChatBot

class ChatbotAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.chat = ChatBot()

        self.app.route('/')(self.inicio)
        self.app.route('/chatbot/', methods=['POST'])(self.endpoint_chatbot)
        self.app.errorhandler(404)(self.not_found)
        self.app.errorhandler(405)(self.method_not_allowed)

    def inicio(self):
        return jsonify({"mensaje": "Bienvenido al asistente UNACHAT"})

    def endpoint_chatbot(self):
        try:
            message = request.get_json().get('message')
            response = self.chat.response(message.lower())
            return jsonify({'mensaje': response}) if response else jsonify({'mensaje': 'Respuesta no encontrada'})
        except Exception as e:
            return jsonify({'mensaje': f'Error: {str(e)}'}), 500

    def not_found(self, error):
        return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

    def method_not_allowed(self, error):
        return make_response(jsonify({'error': 'Método no permitido'}), 405)

if __name__ == '__main__':
    chatbot_api = ChatbotAPI()
    chatbot_api.app.run(debug=True)
