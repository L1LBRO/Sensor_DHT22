# OPC UA, MariaDB, and LCD with Raspberry Pi

This repository contains a Python script that reads data from a DHT22 sensor connected to a Raspberry Pi, stores the data in a MariaDB database, sends the information to an OPC UA server, and finally displays the values on an LCD screen.

## Script Features

### OPC UA Server

Connects to an OPC UA server to update temperature and humidity values.

### MariaDB Database

Connects to a pre-created database to store the readings.

### Data Storage

Saves readings in a table with the following fields:

- `id` (auto-increment)
- `temperature`
- `humidity`
- `reading_timestamp` (timestamp)

### LCD Display

Shows temperature and humidity on an LCD connected to the Raspberry Pi.

## Requirements

### Hardware

- Raspberry Pi with internet connectivity  
- DHT22 sensor  
- LCD display with I2C interface

### Software and Dependencies

- Python 3  
- `opcua` for OPC UA communication  
- `mariadb` for database connectivity  
- `Adafruit_DHT` for reading the DHT22 sensor  
  > Compatibility issues may occur; the recommended approach is to download from the official repository: https://github.com/adafruit/DHT-sensor-library.git  
- `RPLCD` for the LCD screen

## Database Setup

Before running the script, ensure you have a MariaDB database with the following structure:

```sql
CREATE DATABASE sensores;
USE sensores;
CREATE TABLE lecturas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  temperatura FLOAT,
  humedad FLOAT,
  fecha_lectura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
````
To connect successfully, update the database credentials inside the script with your user and password.

## Running the Script

Clone the repository and run the script on your Raspberry Pi:
```bash
git clone https://github.com/L1LBRO/Sensor_DHT22.git
cd Sensor_DHT22
python3 LecturaSensor_EnvioPantalla.py
````

## Usage

Once running, the script reads temperature and humidity every 5 seconds.
Data is sent to the OPC UA server and stored in MariaDB.
Values are displayed on the LCD screen.

## Contributions

If you want to improve this project, feel free to fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License.
