from flask import Flask, jsonify
import pyodbc
import logging
import os

app = Flask(__name__)

# Configuración de conexión a SAP HANA
address = '10.1.0.70'
port = 30015
user = 'SUPRALIVE'
password = 'uGDH6%Yr$K'
database = 'SUPRALIVE'
# Cadena de conexión a SAP HANA
connection_string = f'DRIVER={{HDBODBC}};SERVERNODE={address}:{port};UID={user};PWD={password};DATABASE={database}'

# para manejo de errores
logging.basicConfig(level=logging.INFO)

@app.route('/consultar_sap', methods=['GET'])
def consultar_sap():
    try:
        # Conexión a SAP HANA
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("""SELECT T0."ItemCode" FROM SBO_EC_TENA12_02.OITM T0 WHERE T0."QryGroup5" = 'Y'""")
        result = cursor.fetchall()

        # Crear una lista de resultados
        result_list = []
        for row in result:
            result_list.append({'ItemCode': row[0]})  # accedo al valor de la columna 'ItemCode'
        cursor.close()
        conn.close()

        # Devolver los resultados en formato JSON
        return jsonify(result_list)

    except Exception as e:
        logging.error(f"Error al consultar SAP HANA: {e}")
        return jsonify({"error": "Hubo un problema al realizar la consulta. Intenta de nuevo más tarde."}), 500

if __name__ == '__main__':
    # Puerto Heroku
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto proporcionado por Heroku o 5000 por defecto
    app.run(host='0.0.0.0', port=port, debug=True)
