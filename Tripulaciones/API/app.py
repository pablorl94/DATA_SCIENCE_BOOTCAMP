
"""


██████╗  ██████╗ ██╗   ██╗████████╗███████╗           ██╗ █████╗  
██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝          ███║██╔══██╗ 
██████╔╝██║   ██║██║   ██║   ██║   █████╗      █████╗╚██║╚██████║ 
██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝      ╚════╝ ██║ ╚═══██║ 
██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗           ██║ █████╔╝ 
╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝           ╚═╝ ╚════╝  
                                
                         █████╗ ██████╗ ██╗
                        ██╔══██╗██╔══██╗██║
                        ███████║██████╔╝██║
                        ██╔══██║██╔═══╝ ██║
                        ██║  ██║██║     ██║
                        ╚═╝  ╚═╝╚═╝     ╚═╝
                                                                 

 API de la aplicación "ROUTE -19"

 Enlace a la API:   https://route19api.herokuapp.com/

"""

# -----------------------------------------------------------------------------

# Importaciones

import json
from routes import main
from flask import Flask, jsonify, send_file
from flask_cors import CORS


# Creación de la aplicación y admisión del intercambio cruzado de recursos

app = Flask(__name__)
CORS(app)


# -----------------------------------------------------------------------------

# Función para leer los archivos de datos en el directorio de la API

def read_file(filename):
    with open(filename, "r") as file:
        return json.loads(file.read())


# Función para parsear la información proporcionada en una petición GET

def parse(input_info):
    parameters = input_info.split("&")
    parsed_info = {parameter.split("=")[0]: parameter.split("=")[1] \
                   for parameter in parameters}
    origin_info = parsed_info["origin"].split(",")
    origin = (float(origin_info[0]), float(origin_info[1]))

    destination_info = parsed_info["destination"].split(",")
    destination = (float(destination_info[0]), float(destination_info[1]))

    coordinates = (origin, destination)

    return coordinates


# -----------------------------------------------------------------------------

# La interfaz principal de la API

@app.route("/")
def get_main_interface():
    return send_file("./logo/logo.jpg")


# Para la parte de MAPA:

# Devuelve los lugares peligrosos

@app.route("/map/danger", methods = ["GET"])
def get_danger_map():

    try:
        resource = read_file("./maps/map_danger")
    except:
        resource = None

    if resource:
        return jsonify(resource)
    else:
        return jsonify({"message": "Resource coul not be loaded."})


# Devuelve los lugares a proteger

@app.route("/map/safe", methods = ["GET"])
def get_safe_map():

    try:
        resource = read_file("./maps/map_safe")
    except:
        resource = None

    if resource:
        return jsonify(resource)
    else:
        return jsonify({"message": "Resource coul not be loaded."})


# Para la parte de RUTAS:

# Devuelve los lugares peligrosos

@app.route("/routes/danger", methods = ["GET"])
def get_danger_routes():

    try:
        resource = read_file("./routes/routes_danger")
    except:
        resource = None

    if resource:
        return jsonify(resource)
    else:
        return jsonify({"message": "Resource coul not be loaded."})


# Devuelve los lugares a proteger

@app.route("/routes/safe", methods = ["GET"])
def get_safe_routes():

    try:
        resource = read_file("./routes/routes_safe")
    except:
        resource = None

    if resource:
        return jsonify(resource)
    else:
        return jsonify({"message": "Resource coul not be loaded."})


# Probar con este ejemplo:
# http://127.0.0.1:5000/routes/origin=-3.714517,40.433050&destination=-3.709389,40.435584

@app.route("/routes/<string:parameters>", methods = ["GET"])
def get_route(parameters):
    
    coordinates = parse(parameters)

    try:
        resource = main(coordinates)
    except:
        resource = None

    if resource:
        return jsonify(resource)
    else:
        return jsonify({"message": "Resource coul not be loaded."})


# -----------------------------------------------------------------------------

# Ejecución de la API como script

if __name__ == "__main__":
    app.run(debug = True, port = 5000)




