##=== COLABORACION DE PROYECTO ELECTROCONTROLATE DE SEBASTIAN CARRENO

import serial
import time
import MySQLdb
import datetime
import threading
from pymongo import MongoClient
import pymongo

tLock=threading.Lock()

def EntregarNuevaId(UltimaInsercionMDB):
    return UltimaInsercionMDB['_id']+1

def ObtenerUltimaInsercion(MDBColeccion):
    if (len(list(MDBColeccion.find()))==0):
        MDBColeccion.insert({'_id':0})
    return list(MDBColeccion.find().sort('_id',1))[-1]

##=== Subir Historial Condensacion a Mongo ===========================================
def SubeHistorialCondensacion(idsensor, temperatura, humedad, ventana):
	db = MySQLdb.connect("localhost","root","123","mysql" )
    	cursor = db.cursor()
    	sql = "SELECT idusuario, nombre FROM `USUARIO`"
    	try:
		client= MongoClient('mongodb://admin:efficienth2017@ds113841.mlab.com:13841/efficientmdb')
    		mdb=client['efficientmdb']

            	cursor.execute(sql)
            	results = cursor.fetchall()
            	for row in results:
                	idusuario = row[0]
                	nombre = row[1]
            	db.commit()

		horaActual = datetime.datetime.now() ##obtengo la hora
		fecha = time.strftime("%d/%m/%y") ##obtengo la fecha
		strHora = ""
		if horaActual.hour < 10:
			strHora = "0" + str(horaActual.hour)
		else:
			strHora = str(horaActual.hour)
		hora = strHora + ":00:00"
		coleccionHistCond = mdb.HistoricoCondensacion

		if coleccionHistCond.find({"id_sensor":idsensor, "id_usuario":idusuario, "hora":hora, "fecha": fecha}).count() > 0:	#Si existe
			coleccionHistCond.update({"id_sensor":idsensor, "id_usuario":idusuario, "hora":hora, "fecha":fecha},{"$set": {"nombre":nombre, "temperatura":temperatura, "humedad":humedad}}, upsert = False, multi = True)
		else:
			contadorHist = EntregarNuevaId(ObtenerUltimaInsercion(coleccionHistCond))
			datosHist={"_id":0,"id_usuario": 0,"nombre": 0,"id_sensor": 0, "temperatura": 0, "humedad": 0, "ventilacion": 0, "hora":0, "fecha":0}
			datosHist['_id'] = contadorHist
	            	datosHist['id_usuario'] = idusuario
	           	datosHist['nombre'] = nombre
	            	datosHist['id_sensor'] = idsensor
	            	datosHist['temperatura'] = temperatura
	            	datosHist['humedad'] = humedad
	            	datosHist['ventilacion'] = ventana
			datosHist['hora'] = hora
			datosHist['fecha'] = fecha
			convert2unicode(datosHist)
	            	coleccionHistCond.insert(datosHist)
	except Exception as e:
         	print(e);
		print "Error 27"
		db.rollback()

	# disconnect from server
	db.close()


##=== Realiza update de la Condensacion en la nube ===============================

def ModificarCondensacion(idsensor, temperatura, humedad, ventana):
	db = MySQLdb.connect("localhost","root","123","mysql" )
    	cursor = db.cursor()
    	sql = "SELECT idusuario, nombre FROM `USUARIO`"
    	try:
    		client= MongoClient('mongodb://admin:efficienth2017@ds113841.mlab.com:13841/efficientmdb')
    		mdb=client['efficientmdb']
            	cursor.execute(sql)
            	results = cursor.fetchall()
            	for row in results:
                	idusuario = row[0]
                	nombre = row[1]
            	db.commit()
        	coleccionCondMod = mdb.Condensacion
      	 	coleccionCondMod.update({"id_sensor":idsensor, "id_usuario":idusuario},{"$set": {"temperatura":temperatura, "humedad":humedad, "ventilacion":ventana}}, upsert = False, multi = True)
    	except Exception as e:
         	print(e);
		print "Error 26"

##=== Almacena la info de Condensacion en la nube =================================

def RegistroCond(opcion, datos, coleccion, idusuario, nombre, idsensor, contador, temperatura, humedad, ventana):
        if (opcion == 'cond'):
            tLock.acquire()
            datos['_id'] = contador
            datos['id_usuario'] = idusuario
            datos['nombre'] = nombre
            datos['id_sensor'] = idsensor
            datos['temperatura'] = temperatura
            datos['humedad'] = humedad
            datos['ventilacion'] = ventana
            while True:
                try:
		    convert2unicode(datos)
                    coleccion.insert(datos)
                    break
                except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                    print "error de conexion mongodb (condensacion)"
            tLock.release()

##=== Subir Condensacion a Mongo ===========================================
def SubirCondensacion(idsensor, temperatura, humedad, ventana):
	db = MySQLdb.connect("localhost","root","123","mysql" )
    	cursor = db.cursor()
    	sql = "SELECT idusuario, nombre, NOW()- INTERVAL 1 HOUR FROM `USUARIO`"
    	try:
    		client= MongoClient('mongodb://admin:efficienth2017@ds113841.mlab.com:13841/efficientmdb')
    		mdb=client['efficientmdb']
            	cursor.execute(sql)
            	results = cursor.fetchall()
            	for row in results:
                	idusuario = row[0]
                	nombre = row[1]
                	fecha = row[2]
            	db.commit()
            	datosCond={"_id":0,"id_usuario": 0,"nombre": 0,"id_sensor": 0, "temperatura": 0, "humedad": 0, "ventilacion": 0}

        	coleccionCond = mdb.Condensacion
        	contadorCond = EntregarNuevaId(ObtenerUltimaInsercion(coleccionCond))
		sube=threading.Thread(target=RegistroCond,args=('cond', datosCond, coleccionCond, idusuario, nombre, idsensor, contadorCond, temperatura, humedad, ventana))
   		sube.start()

	except Exception as e:
         	print(e);
		print "Error 25"

##=== Realiza el update de la tabla condensacion ===============
def UpdateCondensacion(idsensor, temperatura, humedad, ventana):
   	db = MySQLdb.connect("localhost","root","123","mysql" )
	cursor = db.cursor()
	sql = "UPDATE `CONDENSACION` set `temperatura` = " + str(temperatura) + ", `humedad` = " + str(humedad) + ",`ventana` = " + str(ventana) + " WHERE idsensor = " + str(idsensor)
	try:
		cursor.execute(sql)
		db.commit()
		ModificarCondensacion(idsensor, temperatura, humedad, ventana)
	except Exception as e:
                print(e);
		print "Error 24"
		db.rollback()

	# disconnect from server
	db.close()

##=== Realiza la insercion en la tabla condensacion ===============
def InsertCondensacion(idsensor, temperatura, humedad, ventana):
    	db = MySQLdb.connect("localhost","root","123","mysql" )
	cursor = db.cursor()
	sql = "INSERT INTO `CONDENSACION` (`idsensor`, `temperatura`, `humedad`,`ventana`) VALUES (" + str(idsensor) + ", " + str(temperatura) + ", " + str(humedad) + ", " + str(ventana) + ")"
	try:
		cursor.execute(sql)
		db.commit()
		SubirCondensacion(idsensor, temperatura, humedad, ventana)
	except Exception as e:
                print(e);
		print "Error 23"
		db.rollback()

	# disconnect from server
	db.close()

##=== Agrega datos de condensacion a la tabla =====================
def AgregarCondensacion(idsensor, temperatura, humedad, ventana):
    	#print str(idsensor)
	db = MySQLdb.connect("localhost","root","123","mysql" )
	cursor = db.cursor()
	sql = "SELECT * FROM `CONDENSACION` WHERE idsensor = " + str(idsensor)
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
        	contador = 0
		for row in results:
			contador = 1
		db.commit()
        	if contador == 1:
            		UpdateCondensacion(idsensor, temperatura, humedad, ventana)
        	else:
            		InsertCondensacion(idsensor, temperatura, humedad, ventana)
		horaActual = datetime.datetime.now() ##obtengo la hora
		if horaActual.minute == 0 and horaActual.second < 13: ## si son los primeros 13 segundos de cada hora
			SubeHistorialCondensacion(idsensor, temperatura, humedad, ventana)
	except Exception as e:
                print(e);
		print "Error 22"
		db.rollback()

	# disconnect from server
	db.close()

##=== Transforma a unicode ========================================

def convert2unicode(mydict):
	for k, v in mydict.iteritems():
        	if isinstance(v, str):
            		mydict[k] = unicode(v, errors = 'replace')
        	elif isinstance(v, dict):
            		convert2unicode(v)

##==== Metodo de Inicializacion de programa ===================================================================

def IniciarPrograma():
	arduino=serial.Serial('/dev/ttyACM0',baudrate=9600, timeout = 3.0)
	arduino.close()
	arduino.open()
	txt=''
	cadena=''
	while True:
		time.sleep(0.1)
		while arduino.inWaiting() > 0:
			txt = arduino.read(1)
			if txt == ',':
        	                x = cadena.split(':')
                		## Sensor 1
        	                print ("temperatura",x[0],"humedad",x[1],"ventana/puerta",x[2])
                		AgregarCondensacion(1, x[0], x[1],x[2])
                		x = ''
				cadena = ''
				txt = ''
			else:
				cadena+=txt
	arduino.close()

IniciarPrograma()

"""
##======= Hago un ciclo infinito buscando el numero del puerto en el que esta arduino ====================================

def BuscandoPuerto(buscarPuerto):
	time.sleep(0.4)
	try:
		print buscarPuerto
		if(buscarPuerto == 20):
			sys.exit(0)
		arduino=serial.Serial(('/dev/ttyACM'+str(buscarPuerto)),baudrate=9600, timeout = 3.0)
		IniciarPrograma(arduino)
	except:
		print "fallo en"
		BuscandoPuerto(buscarPuerto+1)


###====== Aqui parte el codigo ===========================================================================================
buscarPuerto = 0
BuscandoPuerto(buscarPuerto)
"""
