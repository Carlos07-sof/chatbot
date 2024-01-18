import nltk
import json
import spacy
import random
import pickle
import threading
import numpy as np
from keras.models import load_model
from genpre import GenerarPregunta
from spacy.cli.download import download as spacy_download

class ChatBot:
    def __init__(self):
        self.generar = GenerarPregunta()

        # Descargar el modelo spaCy para el procesamiento en español si no está presente
        if not spacy.util.is_package('es_core_news_md'):
            spacy_download('es_core_news_md')

        # Cargar el modelo spaCy
        self.nlp = spacy.load('es_core_news_md')

        # Importar archivos generados del entrenamiento
        self.intents_json = json.loads(open('data/intents.json', 'r', encoding='utf-8').read())
        self.words = pickle.load(open('modelos/words.pkl', 'rb'))
        self.classes = pickle.load(open('modelos/classes.pkl', 'rb'))
        self.model = load_model('modelos/chatbot_model.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [token.lemma_ for token in self.nlp(" ".join(sentence_words))]
        print(f'\nlemmas: {sentence_words}')
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)

        if any(value == 1 for value in bow):
            res = self.model.predict(np.array([bow]))[0]
            max_index = np.where(res == np.max(res))[0][0]
            category = self.classes[max_index]
        else:
            category = 'no_respuesta'
            try:
                threading.Thread(target=self.generar.getQuestion, args=(sentence,)).start()
            except Exception as e:
                print(f"*ERROR HILO (chatbot): {e}*")

        print(f'\ncategory: {category}')
        return category

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
    
    def response(self, sentence):
        try:
            ints = self.predict_class(sentence)
            res = self.get_response(ints)
            return res
        except Exception as e:
            print(f"*ERROR (chatbot): {e}*")
            return False
