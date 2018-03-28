import pyfirmata
import time
import threading 
import smtplib
import pprint
from pymongo import MongoClient
import pymongo
import urllib2
import cookielib
import urllib
import configparser
configuracion = configparser.ConfigParser()

tLock=threading.Lock()

contador1=0
contador2=0
contador3=0
contador4=0

def registro(sensor,maximo,mensaje,fidsensor,ejemplo,coleccion,tabla,contador,en_reposo,contmq,contagua,colecHistorico,contadorHistorico,sensores,relee,ultimahora,conthorassinmov,maximosinmov,reiniciar_datos,movimiento_detectado,bloquear_envio_alerta,diferencia,horadespertar,horaactual):
    print("registro")
    while True:
##        print(sensor, "sensor")
##        print("contagua", contagua)
##        print("maximo", maximo)
        contador=contador+1
        if (type(maximo) is float and fidsensor=='funduino1'):
            tLock.acquire()
            if (sensor.read()>maximo and contagua==1):
                #
                site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=fugadeAgua&Usuario_id_usuario=12"
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
                req = urllib2.Request(site, headers=hdr)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    print (e.code)

                content = page.read()
                print (content)
                time.sleep(1)
                print ('fuga de agua')
                contagua=0
                print ('Encendido')
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                print ("apagado")
                #
                contador=contador+1
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion" )
                        time.sleep(1)
                print ('fuga de agua')
                contagua=0

            elif (sensor.read()<=maximo and contagua==0):
                contador=contador+1
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion" )
                        time.sleep(1)
                print ('libre de agua')
                contagua=1
            tLock.release()
            time.sleep(1)
        if (type(maximo) is float and fidsensor=='mq1'):
            tLock.acquire()
            if (sensor.read()>maximo and contmq==1):
                #
                site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=fugadeGas&Usuario_id_usuario=12"
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
                req = urllib2.Request(site, headers=hdr)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    print (e.code)

                content = page.read()
                print(content)
                time.sleep(1)
                print ('fuga de gas')
                contmq=0
                print ('Encendido')
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                relee.write(float(1.0))
                time.sleep(2)
                relee.write(float(0.0))
                time.sleep(1)
                print ("apagado")
                #
                contador=contador+1
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion") 
                        time.sleep(1)
                print ('fuga de gas')
                contmq=0

            elif (sensor.read()<=maximo and contmq==0):
                contador=contador+1
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion") 
                        time.sleep(1)
                print ('libre de gas')
                contmq=1
            tLock.release()
            time.sleep(1)
    
        elif type(maximo) is bool:
            tLock.acquire()
            if(tabla.digital[sensor].read()==True and en_reposo==True):
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion") 
                        time.sleep(1)
                en_reposo = False
                print ('[' + time.strftime("%T") + '] movimiento\n')
                ultimahora=(time.strftime("%I"))
                conthorassinmov=0
                movimiento_detectado = True
                site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=Movimiento&Usuario_id_usuario=12"
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
                req = urllib2.Request(site, headers=hdr)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    print (e.code)
                content = page.read()
                print(content)
                time.sleep(1)
                print ('Enviada alerta de movimiento')
                
            elif (tabla.digital[sensor].read()==False and en_reposo==False):
                print ('[' + time.strftime("%T") + '] sin movimiento\n')

                ## Cuando la fecha de ejecucion es igual a la de despertar
                if(horaactual == horadespertar):
                    if(reiniciar_datos==1):
                        reiniciar_datos=0
                        movimiento_detectado = False
                        bloquear_envio_alerta = False
                ## Cuando la diferencia es mayor a 2 HORAS
                if(diferencia>=2):
                    
                    if(movimiento_detectado==False and bloquear_envio_alerta==False and reiniciar_datos!=3):
                        reiniciar_datos=1
                        bloquear_envio_alerta=True
                        site= "http://ignacio.awaresystems.cl/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=FaltaMovimiento&Usuario_id_usuario=12"
                        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                               'Accept-Encoding': 'none',
                               'Accept-Language': 'en-US,en;q=0.8',
                               'Connection': 'keep-alive'}
                        req = urllib2.Request(site, headers=hdr)
                        try:
                            page = urllib2.urlopen(req)
                        except urllib2.HTTPError as e:
                            print (e.code)
                        content = page.read()
                        print(content)
                        time.sleep(1)
                        print ('Enviada alerta de falta de movimiento')
                        contmq=0
                        print ('Encendido')
                        relee.write(float(1.0))
                        time.sleep(2)
                        relee.write(float(0.0))
                        time.sleep(1)
                        relee.write(float(1.0))
                        time.sleep(2)
                        relee.write(float(0.0))
                        time.sleep(1)
                        relee.write(float(1.0))
                        time.sleep(2)
                        relee.write(float(0.0))
                        time.sleep(1)
                        relee.write(float(1.0))
                        time.sleep(2)
                        relee.write(float(0.0))
                        time.sleep(1)
                        relee.write(float(1.0))
                        time.sleep(2)
                        relee.write(float(0.0))
                        time.sleep(1)
                        print ("apagado")
                            
                            
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion") 
                        time.sleep(1)
                en_reposo = True
                
            tLock.release()
            time.sleep(0.1)
        time.sleep(0.1)
        
        
def registroHistorico(sensor,fidsensor,ejemplo,tabla,colecHistorico,contadorHistorico,sensores,colecc,listaco,contadorg):
    print("resgistroHistorico")
    if ((int(time.strftime("%M"))%5)==0 and time.strftime("%S")=='00'):
        for i in sensores:
            if (i!="pir1" and i!="corriente1" and sensores[i][1]==0):
                contadorHistorico["historicoid"]=contadorHistorico["historicoid"]+1
                while True:
                    try:
                        colecHistorico.insert(ejemplo)
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion" )
                        time.sleep(1)
                sensores[i][1]=1
            elif (i=="pir1" and i!="corriente1" and sensores[i][1]==0):
                contadorHistorico["historicoid"]=contadorHistorico["historicoid"]+1
                while True:
                    try:
                        break
                    except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
                        print ("error de conexion") 
                        time.sleep(1)
                sensores[i][1]=1
                listaco=[]
    for i in sensores:
        sensores[i][1]=0
    time.sleep(1)
            
            
def ver(relee,contadorconsulta):
    print("while ver")
    while True:        
        if(contadorconsulta==0):
            if time.strftime("%-S")=='50':
                site= "http://ignacio.awaresystems.cl/Saltofinal.php?idfinal=12&intentoo=3" 
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
                req = urllib2.Request(site, headers=hdr)
                try:
                    page = urllib2.urlopen(req)
                except urllib2.HTTPError as e:
                    print (e.code)

                content = page.read()
                print(content)
                #print 'lalala'
                contadorconsulta=1
                if(content!=''):
                    print ('Encendidooo')
                    relee.write(float(1.0))
                    time.sleep(2)
                    relee.write(float(0.0))
                    time.sleep(1)
                    relee.write(float(1.0))
                    time.sleep(2)
                    relee.write(float(0.0))
                    time.sleep(1)
                    relee.write(float(1.0))
                    time.sleep(2)
                    relee.write(float(0.0))
                    time.sleep(1)
                    relee.write(float(1.0))
                    time.sleep(2)
                    relee.write(float(0.0))
                    time.sleep(1)
                    print ("apagadooo")
                    
        if(contadorconsulta==1):
            if time.strftime("%-S")=='1':
                contadorconsulta=0
        time.sleep(0.1)
            #print content
    
        

def main(contador1, contador2, contador3, contador4):
    print("enter main")
    client= MongoClient('mongodb://serviu12:serviu12@ds145389.mlab.com:45389/pruebaaa')
    db=client['pruebaaa']

    contadoringreso=0
    horadespertar=0
    contadorconsulta=0    
    
    if(contadoringreso==0):
        configuracion.read('/home/pi/stayaware.cfg')
        if 'General' in configuracion:
            print("Configuracion leida")
            id = str(configuracion['General']['idAdultoMayor'])
            horadespertar = int(configuracion['General']['horaParaDespertar'])
            print("##########################\n# ID Adulto Mayor: " + id + "\n#  Hora de despertar: " + str(horadespertar) + "\n##########################")
        else:
            print("No existe configuracion... \nComplete en archivo \'stayaware.cfg\'")
            id = str(input("Ingrese ID del adulto mayor: "))
            horadespertar = input("Ingrese Hora de despertar del adulto mayor formato 12 horas: ")
            configuracion['General'] = {'idAdultoMayor' : '1' , 'horaParaDespertar' : '7'}
            with open('/home/pi/stayaware.cfg', 'w') as archivo:
                configuracion.write(archivo)
            print("Configuracion guardada. Abra programa de nuevo.")
            exit()
        contadoringreso=1
##        print("http://awaresystems.cl/ignacio/insertarAlertaAdulto.php?intentoAlerta=1&estadoAlerta=1&tipoAlerta=fugadeGas&Usuario_id_usuario=")


    en_reposo = False
    contmq=0
    contagua=0
    ultimahora=0
    maximosinmov=8
    conthorassinmov=0
    horaactual=int(time.strftime("%I"))
    diferencia=horaactual-horadespertar

    ## Valores:
    ##    3: variable recien inicializada
    ##    0: no reiniciar datos (reiniciar_datos, movimiento_detectado y bloquear_envio_alerta)
    ##    1: reiniciar los datos (reiniciar_datos, movimiento_detectado y bloquear_envio_alerta)
    reiniciar_datos=3

    movimiento_detectado = False
    bloquear_envio_alerta = False
                    
    colecGas = db.Gas
    colecAgua = db.Agua
    colecMov= db.Mov
    print(db.Gas)
    print(db.Agua)
    print(db.Mov)
    colecHistorico=db.historico
    board=pyfirmata.Arduino('/dev/ttyACM1')
    iter=pyfirmata.util.Iterator(board)
    iter.start()
    board.analog[1].mode=pyfirmata.INPUT
    board.analog[1].enable_reporting()
    mq7 = board.get_pin('a:1:i')

    board.analog[5].mode=pyfirmata.INPUT
    board.analog[5].enable_reporting()
    funduino = board.get_pin('a:5:i')

    relee=board.get_pin("d:11:p")

    board.digital[6].mode=pyfirmata.INPUT
    board.digital[6].enable_reporting()
    while True:
        try:
##            contador1=EntregarNuevaId(ObtenerUltimaInsercion(colecGas))+1
##            contador2=EntregarNuevaId(ObtenerUltimaInsercion(colecAgua))+1
##            contador3=EntregarNuevaId(ObtenerUltimaInsercion(colecMov))+1
##            contador4={"historicoid":EntregarNuevaId(ObtenerUltimaInsercion(colecHistorico))+1}
            #
            contador1=contador1 +1
            contador2=contador2 +2
            contador3=contador3 +5
            contador4=contador4 +7 
            print(contador1, contador2, contador3, contador4)
            #
            break
        except pymongo.errors.AutoReconnect or pymongo.errors.ServerSelectionTimeOutError:
            print("error de conexion")
            time.sleep(1)
    
        

    listado={"mq1":[mq7,0],"funduino1":[funduino,0],"pir1":[6,0]}

    ejemplo={"_id":0,"Fidsensor": 0,"medicion": 0,"tipomedicion": 0, "fecha": 0, "hora2": 0}
    
    s1=threading.Thread(target=registro,args=(mq7,0.5,'fuga gas','mq1',ejemplo,colecGas,board,contador1,en_reposo,contmq,contagua,colecHistorico,contador4,listado,relee,ultimahora,conthorassinmov,maximosinmov,reiniciar_datos,movimiento_detectado,bloquear_envio_alerta,diferencia,horadespertar,horaactual))
    s2=threading.Thread(target=registro,args=(funduino,0.4,'agua','funduino1',ejemplo,colecAgua,board,contador2,en_reposo,contmq,contagua,colecHistorico,contador4,listado,relee,ultimahora,conthorassinmov,maximosinmov,reiniciar_datos,movimiento_detectado,bloquear_envio_alerta,diferencia,horadespertar,horaactual))
    s3=threading.Thread(target=registro,args=(6,True,'presencia','pir1',ejemplo,colecMov,board,contador3,en_reposo,contmq,contagua,colecHistorico,contador4,listado,relee,ultimahora,conthorassinmov,maximosinmov,reiniciar_datos,movimiento_detectado,bloquear_envio_alerta,diferencia,horadespertar,horaactual))
##    s4=threading.Thread(target=ver,args=(relee,contadorconsulta))
    s1.start()
    s2.start()
    s3.start()
##    s4.start()

main(contador1, contador2, contador3, contador4)

