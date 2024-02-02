from flask import Flask, jsonify
import requests
from datetime import datetime
from timezonefinder import TimezoneFinder
from pytz import timezone

app = Flask(__name__)

def obtener_hora_desde_ip():
    try:
        # Utilizar httpbin para obtener la dirección IP pública
        response = requests.get("https://httpbin.org/ip")
        
        # Analizar la respuesta JSON
        json_data = response.json()
        
        # Obtener la dirección IP desde los datos JSON
        direccion_ip = json_data.get("origin")

        # Obtener las coordenadas geográficas de la dirección IP
        respuesta_geoloc = requests.get(f'https://ipinfo.io/{direccion_ip}')
        datos_geoloc = respuesta_geoloc.json()
        coordenadas = datos_geoloc.get('loc').split(',')

        # Obtener la zona horaria de las coordenadas
        tf = TimezoneFinder()
        zona_horaria_str = tf.timezone_at(lng=float(coordenadas[1]), lat=float(coordenadas[0]))

        # Convertir la cadena de zona horaria a un objeto tzinfo utilizando pytz
        zona_horaria = timezone(zona_horaria_str)

        # Obtener la hora actual en la zona horaria de la dirección IP
        hora_actual = datetime.now(zona_horaria)
        return hora_actual.strftime('%H:%M')
    
    except Exception as e:
        print("Error al obtener la dirección IP pública:", e)
        return None

@app.route('/obtener_hora', methods=['POST'])
def obtener_hora():
    hora = obtener_hora_desde_ip()
    if hora:
        return jsonify({'hora': hora})
    else:
        return jsonify({'error': 'Error al obtener la hora'}), 500

if __name__ == '__main__':
    app.run(debug=True)
