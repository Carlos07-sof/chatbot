import nltk                             # Biblioteca para procesamiento del lenguaje natural
import json                             # Módulo para manejar archivos JSON
import spacy                            # Biblioteca para procesamiento del lenguaje natural
import random                           # Módulo para generación de números aleatorios
import pickle                           # Módulo para serializar y deserializar objetos
import threading                        # Importar el módulo threading para hacer el hilo
import numpy as np                      # Biblioteca para operaciones numéricas
import es_core_news_md                  # Modelo de spacy para palabras en español
from keras.models import load_model     # Importar un modelo de Keras (biblioteca para aprendizaje profundo)
from genpre import GenerarPregunta

class ChatBot:

    def __init__(self):

        self.generar = GenerarPregunta()
        # Cargar el modelo de spacy para el procesamiento en español
        self.nlp = spacy.load('es_core_news_md')
        self.nlp = es_core_news_md.load()

        # Importar archivos generados del entrenamiento
        self.intents_json = json.loads(open('data/intents.json', 'r', encoding='utf-8').read())
        self.words = pickle.load(open('modelos/words.pkl', 'rb'))
        self.classes = pickle.load(open('modelos/classes.pkl', 'rb'))
        self.model = load_model('modelos/chatbot_model.h5')

    # pasamos las palabras de la oracion a su forma raiz
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [token.lemma_ for token in self.nlp(" ".join(sentence_words))]
        print(f'\nlemmas: {sentence_words}')
        return sentence_words

    # convertimos la informacion a unos y ceros según si estan presentes en los patrones
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        # print(f'\nbag: {bag}')
        return np.array(bag)

    # predecimos la categoria a la que pertenece la oracion
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)

        if any(value == 1 for value in bow):
            res = self.model.predict(np.array([bow]))[0]
            max_index = np.where(res == np.max(res))[0][0]
            category = self.classes[max_index]
        else:
            category = 'no_respuesta'
            try:
                threading.Thread(target = self.generar.getQuestion, args = (sentence,)).start()
            except Exception as e:
                print(f"*ERROR HILO (chatbot): {e}*")
            # finally:
            #     self.generar = None

        print(f'\ncategory: {category}')
        return category

    # obtenemos una respuesta aleatoria
    def get_response(self, tag):
        list_of_intents = self.intents_json['intents']
        result = ""
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i['responses'])
                break
            else:
                result = False
        return result
    
    # respuesta que espera el api
    def response(self, sentence):
        try:
            ints = self.predict_class(sentence)
            res = self.get_response(ints)
            return res
        except Exception as e:
            print(f"*ERROR (chatbot): {e}*")
            return False
        
    
    # test del chatbot
    # def chatTest(self):
    #     print("\n\n¡Bienvenido al Chatbot!")
    #     print("Escribe 'salir' para terminar la conversacion.\n")

    #     while True:
    #         mensaje_usuario = input("usuario: ")

    #         if mensaje_usuario.lower() in ['salir', 'adios']:
    #             print("\n\nHasta luego. ¡Espero que hayas tenido una buena conversacion!\n")
    #             break

    #         ints = self.predict_class(mensaje_usuario)
    #         res = self.get_response(ints)
    #         print(f"\nchatbot: {res}\n")

# Ejemplo de uso
# if __name__ == "__main__":
#     test = ChatBot()
#     test.chatTest()