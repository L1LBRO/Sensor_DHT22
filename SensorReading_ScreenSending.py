from opcua import Client
import adafruit_dht
import board
import time
import mariadb
from RPLCD.i2c import CharLCD

# Configuración del LCD
lcd = CharLCD('PCF8574', 0x27)  # Usa 0x3F si 0x27 no funciona.

# Configuración del servidor OPC UA
URL = "opc.tcp://localhost:4840/freeopcua/server/"
# Definición de los nodos
TEMP_NODE_ID = "ns=2;i=2"
HUMIDITY_NODE_ID = "ns=2;i=3"

# Configuración de la conexión a MariaDB
DB_CONFIG = {
    "host": "localhost",
    "user": "usersensor",
    "password": "P@ssw0rd!",
    "database": "sensores"
}

# Inicializar el cliente OPC UA
client = Client(URL)

# Inicializar el sensor DHT22
sensor = adafruit_dht.DHT22(board.D4)

def connect_opcua():
    while True:
        try:
            client.connect()
            print("Conectado al servidor OPC UA")
            return
        except Exception as e:
            print(f"Error de conexión en OPC UA: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

def connect_db():
    while True:
        try:
            conn = mariadb.connect(**DB_CONFIG)
            print("Conectado a la base de datos MariaDB")
            return conn
        except mariadb.Error as e:
            print(f"Error de conexión en MariaDB: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

def save_to_db(temperature, humidity, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
        print("Datos guardados en MariaDB")
    except mariadb.Error as e:
        print(f"Error al insertar datos en MariaDB: {e}")

def update_lcd(temperature, humidity):
    """ Escribe la temperatura y humedad en la pantalla LCD """
    lcd.clear()
    lcd.write_string(f"Temp: {temperature:.1f}C")
    lcd.crlf()
    lcd.write_string(f"Humedad: {humidity:.1f}%")

# Conectar a OPC UA y MariaDB
connect_opcua()
conn = connect_db()

temperature_node = client.get_node(TEMP_NODE_ID)
humidity_node = client.get_node(HUMIDITY_NODE_ID)

try:
    while True:
        try:
            # Leer datos del sensor
            temperature = sensor.temperature
            humidity = sensor.humidity

            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature:.1f} C  Humedad: {humidity:.1f}%")

                # Enviar datos a OPC UA
                try:
                    temperature_node.set_value(temperature)
                    humidity_node.set_value(humidity)
                    print("Datos actualizados en el servidor OPC UA")
                except Exception as e:
                    print(f"Error al actualizar OPC UA: {e}")
                    client.disconnect()
                    connect_opcua()

                # Guardar en MariaDB
                save_to_db(temperature, humidity, conn)

                # Actualizar la pantalla LCD
                update_lcd(temperature, humidity)
            else:
                print("Error: valores inválidos del sensor")

        except RuntimeError as e:
            print(f"Error en la lectura del sensor: {e}")

        time.sleep(5)  # Esperar entre lecturas

except KeyboardInterrupt:
    print("Deteniendo el script...")
finally:
    sensor.exit()
    client.disconnect()
    lcd.clear()
    print("Sensor liberado, desconectado de OPC UA y MariaDB cerrada.")
