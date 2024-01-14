import json
import spacy
import es_core_news_md
from controller import PreguntasController

class GenerarPregunta:
    def __init__(self):
        self.pregunta = PreguntasController()
        self.nlp = spacy.load('es_core_news_md')
        self.nlp = es_core_news_md.load()

    def procesarPregunta(self, pregunta):
        lemmas = [token.lemma_ for token in pregunta]
        lemmas = ' '.join(lemmas)
        return lemmas

    def procesarEtiqueta(self, pregunta):
        newEtiqueta = []

        for token in pregunta:
            if token.pos_ == 'NOUN':
                newEtiqueta.append(token.lemma_)
            if token.pos_ == 'PROPN':
                newEtiqueta.append(token.lemma_)
        
        etiqueta = "_".join(newEtiqueta)
        return etiqueta
    
    def sendJSON(self, data):
        dataJSON = {"etiqueta": None, "pregunta": None}
        dataJSON['etiqueta'] = self.procesarEtiqueta(data)
        dataJSON['pregunta'] = self.procesarPregunta(data)
        return dataJSON
    
    def build(self,sentence):
        doc = self.nlp(sentence)
        response = self.sendJSON(doc)
        response = json.dumps(response, ensure_ascii = False)
        return response
    
    def getQuestion(self,pregunta):
        try:
            # print(f'STATUS (gen-pre): {self.pregunta.sendQuestion(self.build(pregunta))}')
            self.pregunta.sendQuestion(self.build(pregunta))
            return True
        except Exception as e:
            print(f"*ERROR (gen-pre): {e}*")
            return False
        # finally:
        #     self.pregunta = None

# # Ejemplo de uso
# if __name__ == "__main__":
#     test = GenerarPregunta()

#     # Oración de ejemplo en español
#     # sentence = "como me inscribo a la universidad"
#     # sentence = "cuando son las convocatorias"
#     # sentence = "cuando se abren convocatorias"
#     # sentence = "cuando seran las convocatorias de la escuela"
#     # sentence = "cuando se realizan las convocatorias"
#     # sentence = "cuando terminan las convocatorias"
#     # sentence = "cuando cierran las convocatorias"
#     sentence = "cuando es la fecha del examen de admision y cuando dan los resultados"

#     # print(f'JSON: {test.build(sentence)}')
#     print(test.getQuestion(sentence))
