from flask import Flask, request, jsonify
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pytz import timezone

app = Flask(__name__)

def obtener_hora_desde_ip(direccion_ip):
    try:
        geolocalizador = Nominatim(user_agent="obtener_hora_desde_ip", timeout=10)  # Establece un tiempo de espera específico
        ubicacion = geolocalizador.geocode(direccion_ip, language='es')

        if ubicacion:
            tf = TimezoneFinder()
            zona_horaria = timezone(tf.timezone_at(lng=ubicacion.longitude, lat=ubicacion.latitude))
            fecha_actual = datetime.now(zona_horaria)
            return fecha_actual.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return "No se pudo obtener la información de ubicación para la dirección IP proporcionada."

    except requests.exceptions.Timeout:
        return "El servicio de geolocalización tardó demasiado en responder. Inténtalo de nuevo más tarde."
    except Exception as e:
        return f"Error al obtener la información: {e}"


@app.route('/obtener_hora', methods=['POST'])
def obtener_hora():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    print(f"Dirección IP del cliente: {client_ip}")
    hora = obtener_hora_desde_ip(client_ip)
    return jsonify({'hora': hora})


if __name__ == '__main__':
    app.run(debug=True)
