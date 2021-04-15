# Importa las librerias necesarias

import adafruit_dht
import os
import datetime
import time

#Importa el script para enviar correos

from envio_de_correo_v0 import sendEmail

#Setea los mail para enviar y recibir las alarmas por correo. Se tienen que modificar con los mails que se quieren usar como destinatario y remitente para el proyecto.

email_sender = "labi.2019.fiuba@gmail.com"
email_sender_password = "contraparaelLABi"
email_recipient = "fgrcia94@yahoo.com.ar"
subject = "Envío de alarmas - Rack xxx de la FIUBA"

#Setea la ubicación dónde están los archivos del logueo de la UPS (en ups_log_path), el archivo de logueo generado por el script con los valores de la UPS y del sensor (en log_path) y el archivo utilizado para escribir los tiempos en que se enviaron correos (log_emails_path).
log_path = "/var/log/monitoreo_de_racks/dht_and_ups.log"
ups_log_path = "/etc/nut/ups.log"
log_emails_path = "/var/log/monitoreo_de_racks/log_emails_sent.log"

#log_path = "dht_and_ups.log"     #Estos valores son para testear (se tienen que colocar los archivos en la misma carpeta en que corre Python)
#ups_log_path = "ups.log"
#log_emails_path = "log_emails_sent.log"

#Setea el valor máximo de temperatura para comparar y enviar de alarmas.
temperatura_maxima = 100

# Configuración del puerto GPIO al cual esta conectado (GPIO 23)
pin = 23

# Crea el objeto para acceder al sensor. Se debe descomentar la linea dependiendo del tipo de sensor (DHT11 o DHT22)
sensor = adafruit_dht.DHT11(pin)
#sensor = adafruit_dht.DHT22(pin)

# Function to read last N lines of the file through exponential search 
def LastNlines(fname, N): 
	
	# assert statement check a condition 
	assert N >= 0
	
	# declaring variable to implement exponential search 
	pos = N + 1
	
	# list to store last N lines 
	lines = [] 
	
	# opening file using with() method so that file get closed after completing work 
	with open(fname) as f: 
		
		# loop which runs until size of list becomes equal to N 
		while len(lines) <= N: 
			
			# try block 
			try: 
				# moving cursor from left side to pos line from end 
				f.seek(-pos, 2) 
		
			# exception block to handle any run time error 
			except IOError: 
				f.seek(0) 
				break
			
			# finally block to add lines to list after each iteration 
			finally: 
				lines = list(f) 
			
			# increasing value of variable exponentially 
			pos *= 2
			
	# returning the whole list which stores last N lines 
	return lines[-N:] 


#Envío de alarmas por correo electrónico. Hay que pasarle como parámetros el tipo de alarma y el mensaje a enviar en el mail.
#Los emails se mandan una vez cada cierto tiempo, para que no le lleguen muchos mails al destinatario. Es necesario guardar en un archivo la información del tiempo (cantidad de segundos después del epoch) en que fue enviado el último mail de un determinado tipo de alarma, para después poder comparar y saber si ya se puede enviar de nuevo la alarma.
def sendAlarm(type_of_alarm, message):

	#Se fija si ya existe el archivo dónde se guardan los tiempos en que fueron enviadas las últimas alarmas, si no existe lo crea y lo inicializa en cero.
	if(os.path.exists(log_emails_path) == False):
		log_emails = open(log_emails_path,"w")
		log_emails.write("0 0 0")
		log_emails.close()
	if(os.path.getsize(log_emails_path) == 0):
		log_emails = open(log_emails_path,"w")
		log_emails.write("0 0 0")
		log_emails.close()
		
	#Abre el archivo dónde se guardan los tiempos en que fueron enviadas las últimas alarmas.
	log_emails = open(log_emails_path,"r")
	#Se lee los tiempos en que fueron enviadas las últimas alarmas.
	tiempos_mails_enviados = log_emails.readline()
	tiempos_mails_enviados = tiempos_mails_enviados.split(" ", 3)
	log_emails.close()
	tiempo_de_la_ultima_alarma_por_tension_alta_enviada = float(tiempos_mails_enviados[0])
	tiempo_de_la_ultima_alarma_por_tension_baja_enviada = float(tiempos_mails_enviados[1])
	tiempo_de_la_ultima_alarma_por_temperatura_alta_enviada = float(tiempos_mails_enviados[2])
	
	#Tiempo en segundos que tiene que pasar para enviar otra alarma del mismo tipo. Está configurado para que valga 12 hs.
	tiempo_entre_alarmas = 43200
	#Obtiene el tiempo actual en segundos.
	tiempo_actual = time.time()	
	
	if type_of_alarm == "Tension alta":
		#Se fija si pasaron 12 horas desde la última vez que se envió una alarma para enviar otra alarma.
		if (tiempo_actual - tiempo_de_la_ultima_alarma_por_tension_alta_enviada) > tiempo_entre_alarmas:
			#Manda una alarma por mail
			sendEmail(email_sender, email_sender_password, email_recipient, subject, message, log_path)
			tiempo_de_la_ultima_alarma_por_tension_alta_enviada = tiempo_actual
			
	if type_of_alarm == "Tension baja":
		#Se fija si pasaron 12 horas desde la última vez que se envió una alarma para enviar otra alarma.
		if (tiempo_actual - tiempo_de_la_ultima_alarma_por_tension_baja_enviada) > tiempo_entre_alarmas:
			#Manda una alarma por mail
			sendEmail(email_sender, email_sender_password, email_recipient, subject, message, log_path)
			tiempo_de_la_ultima_alarma_por_tension_baja_enviada = tiempo_actual
	
	if type_of_alarm == "Temperatura alta":
		#Se fija si pasaron 12 horas desde la última vez que se envió una alarma para enviar otra alarma.
		if (tiempo_actual - tiempo_de_la_ultima_alarma_por_temperatura_alta_enviada) > tiempo_entre_alarmas:
			#Manda una alarma por mail
			sendEmail(email_sender, email_sender_password, email_recipient, subject, message, log_path)
			tiempo_de_la_ultima_alarma_por_temperatura_alta_enviada = tiempo_actual	

	#Guarda en el archivo los tiempos en que fueron enviadas las últimas alarmas de los distintos tipos, uno a continuación del otro separados por espacio.
	log_emails = open(log_emails_path,"w")
	log_emails.write(str(tiempo_de_la_ultima_alarma_por_tension_alta_enviada) + " " + str(tiempo_de_la_ultima_alarma_por_tension_baja_enviada) + " " + str(tiempo_de_la_ultima_alarma_por_temperatura_alta_enviada))
	log_emails.close()

# Función: Escribe un archivo log en log_path con los datos del sensor y de la UPS, si no existe el archivo lo crea. Luego chequea los datos y si están fuera de los límites envía alarmas por correo electrónico.
def write_log_and_send_alarms(temperatura, humedad):

	#---------Logueo de los datos-----------	
   
	#Esta es una forma menos eficiente de leer la última línea del log de la UPS, recurrir a esta si la otra forma no funciona. Recordar cerrar el archivo.
	#ups_log = open("ups.log","r")
	#last_line_ups_log = ups_log.readlines()[-1]
	#ups_log_data = last_line_ups_log.split(" ", 8)
	#ups_log.close()
	
	#Leo los datos de la UPS
	last_line_ups_log = LastNlines(ups_log_path, 1)	
	ups_log_data = str(last_line_ups_log).split(" ", 8)
	ups_date = ups_log_data[0][2:]
	ups_time = ups_log_data[1]
	ups_battery_charge = ups_log_data[2] 
	ups_voltage = ups_log_data[3]
	ups_load = ups_log_data[4]
	ups_status = ups_log_data[5]
	ups_temperature = ups_log_data[6]
	ups_input_frecuency = ups_log_data[7][:2]

    #Logueo con la información del sensor y la UPS. Cada vez que se ejecuta se crea una nueva línea al final del archivo.
	#El formato es : "fecha en que midió el sensor" + " " + "hora en que midió el sensor" + " " + "temperatura" + " " + "humedad" + " " + "fecha en que midió la UPS" + " " + "hora en que midió la UP" + " " + "Carga de la batería de la UPS" + " " + "Tensión que midió la UPS" +  " " + "Carga conectada a la UPS" + " " + "Estado de la UPS" + " " + "Temperatura de la UPS" + " " + "Frecuencia de la tensión de fase de la UPS." 
	log = open(log_path,"a")
	line_part1 = datetime.datetime.now().strftime("%Y%m%d %H%M%S") + " " + temperatura +  " " + humedad  + " "
	line_part2 = ups_date +  " " +  ups_time + " " + ups_battery_charge + " " + ups_voltage +  " " +  ups_load + " " + ups_status + " " + ups_temperature + " " + ups_input_frecuency + "\n"
	log.write(line_part1 + line_part2)
	log.close()
	
	#---------Chequeo de los valores y envío de alarmas-----------		
	
	#Por el momento está programado el envío de alarmas por tensión alta, por tensión baja y por temperatura alta.
	
	if ups_voltage != "NA":
		ups_voltage_float = float(ups_voltage)#####################################################################################################################################################################################Validar
		#Me fijo si la tensión está por encima de un 10% del valor nominal, si está por encima envío una alarma.
		if ups_voltage_float > (220+220*0.1):
			type_of_alarm = "Tension alta"			
			message = "La tensión está por encima del valor de tolerancia del 10 %. La tensión registrada por la UPS es de " + ups_voltage + " V. Email enviado el " + datetime.datetime.now().strftime("%d/%m/%Y") + " a las " +  datetime.datetime.now().strftime("%H:%M") + " hs."
			sendAlarm(type_of_alarm, message)
		
		#Me fijo si la tensión está por debajo de un 10% del valor nominal, si está por debajo envío una alarma.	
		if ups_voltage_float < (220-220*0.1):
			type_of_alarm = "Tension baja"
			message = "La tensión está por debajo del valor de tolerancia del 10 %. La tensión registrada por la UPS es de " + ups_voltage + " V. Email enviado el " + datetime.datetime.now().strftime("%d/%m/%Y") + " a las " +  datetime.datetime.now().strftime("%H:%M") + " hs."
			sendAlarm(type_of_alarm, message)

	if temperatura != "NA":
		temperatura_float = float(temperatura)
		#Me fijo si la temperatura está por encima del valor máximo seteado, si está por encima envío una alarma.
		if temperatura_float > temperatura_maxima:
			type_of_alarm = "Temperatura alta"
			message = "La temperatura está por encima del valor máximo seteado de " + str(temperatura_maxima) + " °C. " "La temperatura registrada por el sensor es de " + temperatura + " °C. Email enviado el " + datetime.datetime.now().strftime("%d/%m/%Y") + " a las " +  datetime.datetime.now().strftime("%H:%M") + " hs."
			sendAlarm(type_of_alarm, message)
   
#Código para debugueo.      
#temperatura = "120" 
#humedad = "30"
#write_log_and_send_alarms(str(temperatura), str(humedad))


# Funcion principal
def main():
	# Ciclo principal infinito
	while True:

		# Intenta ejecutar las siguientes instrucciones, si falla va a la instruccion except
		try:
			# Obtiene la humedad y la temperatura desde el sensor
			humedad = sensor.humidity
			temperatura = sensor.temperature

			# Corrobora que haya obtenido una lectura
			if humedad is None or temperatura is None:
				humedad = "NA"; temperatura = "NA"

		# Se ejecuta en caso de que falle alguna instruccion dentro del try
		except RuntimeError as error:
			# Imprime en pantalla el error
			print(error.args[0])
			humedad = "NA"; temperatura = "NA"

		try:
			#Loguea los datos de los sensores y la UPS, chequea los valores y si están mal envía alarmas
			write_log_and_send_alarms(str(temperatura), str(humedad))

		except:
			print("Ocurrió un error.")

		# Duerme 10 segundos
		time.sleep(2)

# Llama a la funcion principal
if __name__ == "__main__":
    main()
    
    