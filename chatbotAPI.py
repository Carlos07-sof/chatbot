from flask import Flask, request, jsonify
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pytz import timezone

app = Flask(__name__)

def obtener_hora_desde_ip(direccion_ip):
    try:
        geolocalizador = Nominatim(user_agent="obtener_hora_desde_ip")
        ubicacion = geolocalizador.geocode(direccion_ip, language='es')

        if ubicacion:
            tf = TimezoneFinder()
            zona_horaria = timezone(tf.timezone_at(lng=ubicacion.longitude, lat=ubicacion.latitude))
            fecha_actual = datetime.now(zona_horaria)
            return fecha_actual.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return "No se pudo obtener la información de ubicación para la dirección IP proporcionada."

    except Exception as e:
        return f"Error al obtener la información: {e}"

@app.route('/obtener_hora', methods=['POST'])
def obtener_hora():
    if 'ip' in request.form:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        # ip_cliente = request.form['ip']

        # Imprimir la dirección IP en la consola
        print(f"Dirección IP del cliente: {client_ip}")

        hora = obtener_hora_desde_ip(client_ip)
        return jsonify({'hora': hora})
    else:
        return jsonify({'error': 'Se requiere la dirección IP en la solicitud POST.'})

@app.route('/endpoint_chatbot', methods=['POST'])
def endpoint_chatbot():
    try:
        data = request.get_json()
        message = data.get('message')
        
        # Imprimir la dirección IP del cliente en la consola
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        print(f"Dirección IP del cliente en el endpoint_chatbot: {client_ip}")

        res = "Respuesta de chatbot"  # Reemplaza esto con la lógica real

        if not res:
            return jsonify({'mensaje': 'Respuesta no encontrada'})
        else:
            return jsonify({'mensaje': res})

    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
