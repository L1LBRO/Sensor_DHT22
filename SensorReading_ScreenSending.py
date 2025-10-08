from opcua import Client
import adafruit_dht
import board
import time
import mariadb
from RPLCD.i2c import CharLCD

# LCD configuration
lcd = CharLCD('PCF8574', 0x27)  # Use 0x3F if 0x27 does not work.

# OPC UA server configuration
URL = "opc.tcp://localhost:4840/freeopcua/server/"
# Node definitions
TEMP_NODE_ID = "ns=2;i=2"
HUMIDITY_NODE_ID = "ns=2;i=3"

# MariaDB connection configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "usersensor",
    "password": "P@ssw0rd!",
    "database": "sensores"
}

# Initialize OPC UA client
client = Client(URL)

# Initialize DHT22 sensor
sensor = adafruit_dht.DHT22(board.D4)

def connect_opcua():
    while True:
        try:
            client.connect()
            print("Connected to OPC UA server")
            return
        except Exception as e:
            print(f"OPC UA connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def connect_db():
    while True:
        try:
            conn = mariadb.connect(**DB_CONFIG)
            print("Connected to MariaDB")
            return conn
        except mariadb.Error as e:
            print(f"MariaDB connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def save_to_db(temperature, humidity, conn):
    try:
        cursor = conn.cursor()
        # Note: table/column names kept as in DB schema (lecturas, temperatura, humedad)
        cursor.execute("INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
        print("Data saved to MariaDB")
    except mariadb.Error as e:
        print(f"Error inserting data into MariaDB: {e}")

def update_lcd(temperature, humidity):
    """Write temperature and humidity to the LCD display"""
    lcd.clear()
    lcd.write_string(f"Temp: {temperature:.1f}C")
    lcd.crlf()
    lcd.write_string(f"Humidity: {humidity:.1f}%")

# Connect to OPC UA and MariaDB
connect_opcua()
conn = connect_db()

temperature_node = client.get_node(TEMP_NODE_ID)
humidity_node = client.get_node(HUMIDITY_NODE_ID)

try:
    while True:
        try:
            # Read sensor data
            temperature = sensor.temperature
            humidity = sensor.humidity

            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature:.1f} C  Humidity: {humidity:.1f}%")

                # Send data to OPC UA
                try:
                    temperature_node.set_value(temperature)
                    humidity_node.set_value(humidity)
                    print("Data updated on OPC UA server")
                except Exception as e:
                    print(f"Error updating OPC UA: {e}")
                    client.disconnect()
                    connect_opcua()

                # Save to MariaDB
                save_to_db(temperature, humidity, conn)

                # Update the LCD display
                update_lcd(temperature, humidity)
            else:
                print("Error: invalid sensor values")

        except RuntimeError as e:
            print(f"Sensor read error: {e}")

        time.sleep(5)  # Wait between readings

except KeyboardInterrupt:
    print("Stopping script...")
finally:
    sensor.exit()
    client.disconnect()
    lcd.clear()
    print("Sensor released, disconnected from OPC UA and MariaDB connection closed.")
