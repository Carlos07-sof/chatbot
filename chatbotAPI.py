from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot import ChatBot

class ChatbotAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.chat = ChatBot()

        @self.app.route('/')
        def inicio():
            return jsonify({"mensaje": "Bienvenido al asistente UNACHAT"})

        @self.app.route('/chatbot/', methods=['POST'])
        def endpoint_chatbot():
            try:
                data = request.get_json()
                message = data.get('message')

                res = self.chat.response(message.lower())

                if not res:
                    return jsonify({'mensaje': 'Respuesta no encontrada'})
                else:
                    return jsonify({'mensaje': res})

            except Exception as e:
                return jsonify({'mensaje': f'Error: {str(e)}'}), 500

        @self.app.errorhandler(404)
        def not_found(error):
            return make_response(jsonify({'error': 'No se encontró el recurso solicitado'}), 404)

        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return make_response(jsonify({'error': 'Método no permitido'}), 405)

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    chatbot_api = ChatbotAPI()
    chatbot_api.run()
