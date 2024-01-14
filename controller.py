from model import Preguntas

class PreguntasController:
    def __init__(self):
        self.modelPreguntas = Preguntas()

    def sendQuestion(self, pregunta):
        try:
            # print(f'STATUS CONTROLLER: {self.modelPreguntas.saveQuestion(content)}')
            self.modelPreguntas.saveQuestion(pregunta)
            return True
        except Exception as e:
            print(f"*ERROR CONTROLLER: {e}*")
            return False
        # finally:
        #     self.modelPreguntas = None

# # Ejemplo de uso
# if __name__ == "__main__":
#     test = PreguntasController()
#     test.sendQuestion('{"etiqueta": "convocatoria","pregunta": "PRE_comvo"}')