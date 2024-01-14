from connection import PostgreSQLConnection

class Preguntas:
    def __init__(self):
        self.conn = PostgreSQLConnection()
        self.cnx = self.conn.connect()
        self.clos = self.conn.close()

    def saveQuestion(self, pregunta):
        # self.cnx = self.cnx.connect()
        query = f"CALL procesarPregunta('{pregunta}');"
        try:
            with self.cnx.cursor() as cursor:
                if pregunta:
                    cursor.execute(query)
                    self.cnx.commit()
                    return True
                else:
                    print('*NO HAY DATOS*')
            
            self.free()
        except Exception as e:
            print(f"*ERROR AL EJECUTAR LA CONSULTA: {e}*")
            return False

    def free(self):
        self.clos.close()
        self.clos = None
        self.cnx = None
        self.conn = None
