# OPC UA, MariaDB y LCD con Raspberry Pi

  Este repositorio contiene un script en Python que permite leer datos de un sensor DHT22 conectado a una Raspberry Pi, almacenar los datos en una base de datos MariaDB, enviar la información a un servidor OPC UA y finalmente mostrar los valores en una pantalla LCD.

## Características del Script

  ### Servidor OPC UA: 
  
  Se conecta a un servidor OPC UA para actualizar los valores de temperatura y humedad.

  ### Base de datos MariaDB: 
  
  Se conecta a una base de datos previamente creada para almacenar los valores.

  ### Almacenamiento de datos: 
  
  Guarda las lecturas en una tabla con los siguientes campos:

    id (autoincremental)
    temperatura
    humedad
    fecha_lectura (timestamp)

  ### Pantalla LCD: 
  
  Muestra la temperatura y la humedad en una pantalla LCD conectada a la Raspberry Pi.

  ## Requisitos

  ### Hardware

    Raspberry Pi con conexión a internet
    Sensor DHT22
    Pantalla LCD con interfaz I2C
    
  ### Software y dependencias

    Python 3
    Opcua para la comunicación OPC UA
    Mariadb para la conexión con la base de datos
    Adafruit_dht para la lectura del sensor DHT22 (Pueden surgir problemas de compatibilidad por lo que lo más recomendable es descargarlo desde su repositorio oficial https://github.com/adafruit/DHT-sensor-library.git)
    RPLCD para la pantalla LCD

  ## Configuración de la Base de Datos

  Antes de ejecutar el script, asegúrate de tener creada una base de datos en MariaDB con la siguiente estructura:

    CREATE DATABASE sensores;
    USE sensores;
    CREATE TABLE lecturas (
      id INT AUTO_INCREMENT PRIMARY KEY,
      temperatura FLOAT,
      humedad FLOAT,
      fecha_lectura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

  Para que el script funcione correctamente con la base de datos se deberá cambiar los datos que existen dentro del script para tener el usuario y contraseña del usuario de tu base de datos

  ## Ejecución del Script

   Clona el repositorio y ejecuta el script en tu Raspberry Pi:

    git clone https://github.com/L1LBRO/Sensor_DHT22.git
    cd Sensor_DHT22
    python3 LecturaSensor_EnvioPantalla.py

  ## Uso
    
  Una vez ejecutado, el script leerá la temperatura y humedad del sensor cada 5 segundos.
  Los datos se enviarán al servidor OPC UA y se almacenarán en MariaDB.
  Los valores se mostrarán en la pantalla LCD.

  ## Contribuciones

  Si deseas mejorar este proyecto, siéntete libre de hacer un fork y enviar un pull request con tus mejoras.

  ## Licencia

  Este proyecto está bajo la licencia MIT.
