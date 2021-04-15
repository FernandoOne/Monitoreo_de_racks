## Programa de Python
Ejecutar el script de la última versión. Colocar el script de envío de correo en la misma carpeta para que lo pueda importar.

## Sensado de temperatura y humedad con DTH11

### Fuentes
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
https://www.internetdelascosas.cl/2017/05/19/raspberry-pi-conectando-un-sensor-de-temperatura-y-humedad-dht11/

### Instalación
Para instalar las librerías se tiene que ejectar en la consola:

```sudo apt-get update

sudo apt-get upgrade

sudo apt-get install python3-pip python3-dev

sudo pip3 install --upgrade setuptools
```

Corroborar que Python 3 sea la versión que corra por default como dice en el la página.
Habilitar I2C y SPI como dice en la página.

Luego ejecutar en la consola:

```pip3 install RPI.GPIO

pip3 install adafruit-blinka

pip3 install adafruit-circuitpython-dht

sudo apt-get install libgpiod2
```

### Verificar conexión del sensor
Conectar el sensor a la Raspberry Pi, varía si el sensor tiene tres pines (versión montada en un PCB) o cuatro pines.

Si están bien instaladas las librerías debería correr el programa.

## Envío de mails

### Fuente
https://code.tutsplus.com/es/tutorials/sending-emails-in-python-with-smtp--cms-29975


