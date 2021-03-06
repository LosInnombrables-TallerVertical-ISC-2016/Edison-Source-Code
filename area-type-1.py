import time
import pyupm_buzzer as upmBuzzer
import pyupm_grove as grove
import mraa
import pyupm_i2clcd as lcd
import sys
import random

import json
import urllib
import subprocess

#Area que administra
areaName = "A"

#Direccion del servidor
server='http://10.43.14.124:3000/api'

r = urllib.urlopen(server)

#Leyendo query a server.
jsonStr = r.read()

#Convirtiendo en un objeto JSON
jsonResult = json.loads(jsonStr);

#Numero de areas
size = len(jsonResult)

#Buscar objeto del area a administrar
i=0
while (i<size):
    print(jsonResult[i])
    if(jsonResult[i]["name"] == areaName):
        area = jsonResult[i]
    i=i+1

#Espacios ocupados
occupied = area['generalCapacity'] - area['generalAvailable']
#Capacidad del area
capacity = area['generalCapacity']
overload = 0

# Create the button object using GPIO pin 2
button = mraa.Gpio(2)
# Create the buzzer object using GPIO pin 3
button2 = mraa.Gpio(3)
button.dir(mraa.DIR_IN)
button2.dir(mraa.DIR_IN)
# Create the button object using GPIO pin 6
button3 = mraa.Gpio(6)
# Create the buzzer object using GPIO pin 7
button4 = mraa.Gpio(7)
button3.dir(mraa.DIR_IN)
button4.dir(mraa.DIR_IN)

#Inicializar led 
ledPin = mraa.Gpio(5)
ledPin.dir(mraa.DIR_OUT)

if(occupied<capacity):
    ledPin.write(1)
else:
    ledPin.write(0)


entra=False
sale=False
entra2=False
sale2=False

print("ocupados: "+str(occupied)+" de "+str(capacity))

# Read the input and print, waiting one second between readings
while 1:
    #Primera entrada o salida
    if(entra):
        if(button2.read()!=0):
            if(occupied + 1 <= capacity):
                occupied = occupied + 1
                subprocess.check_call(['curl', '-X', 'PUT', '-H', "Cache-Control: no-cache",
                    '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "name="+areaName+"&generalAvailable=-1", server])
            else:
                overload = overload + 1

            print("Boton 2 presionado, entro")
            print("ocupados: "+str(occupied)+" de "+str(capacity))
            entra=False
            sale=False
            time.sleep(0.5)
            #subprocess.check_call('curl -X PUT -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" -d "name=Area 1&generalAvailable=-1" '+server)
    else:
        if(button2.read() != 0):
            sale=True
            
            print("Boton 2 presionado")
            time.sleep(0.5)

    if(sale):
        if(button.read()!=0):
            

            if(occupied - 1 >= 0):
                if(overload == 0):
                    occupied = occupied - 1
                    subprocess.check_call(['curl', '-X', 'PUT', '-H', "Cache-Control: no-cache",
                        '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "name="+areaName+"&generalAvailable=1", server])
                else:
                    overload = overload - 1

            

            print("Boton 1 presionado, salio")
            
            entra=False
            sale=False
            time.sleep(0.5)
    else:
        if(button.read() != 0):
            entra=True
            print("Boton 1 presionado")
            

            time.sleep(0.5)
            
            
    #segunda entrada o salida
    if(entra2):
        if(button4.read()!=0):
            if(occupied + 1 <= capacity):
                occupied = occupied + 1
                subprocess.check_call(['curl', '-X', 'PUT', '-H', "Cache-Control: no-cache",
                    '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "name="+areaName+"&generalAvailable=-1", server])
            else:
                overload = overload + 1

            print("Boton 2 presionado, entro")
            print("ocupados: "+str(occupied)+" de "+str(capacity))
            entra2=False
            sale2=False
            time.sleep(0.5)
            #subprocess.check_call('curl -X PUT -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" -d "name=Area 1&generalAvailable=-1" '+server)
    else:
        if(button4.read() != 0):
            sale2=True
            
            print("Boton 2 presionado")
            time.sleep(0.5)

    if(sale2):
        if(button3.read()!=0):
            

            if(occupied - 1 >= 0):
                if(overload == 0):
                    occupied = occupied - 1
                    subprocess.check_call(['curl', '-X', 'PUT', '-H', "Cache-Control: no-cache",
                        '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "name="+areaName+"&generalAvailable=1", server])
                else:
                    overload = overload - 1

            

            print("Boton 1 presionado, salio")
            
            entra2=False
            sale2=False
            time.sleep(0.5)
    else:
        if(button3.read() != 0):
            entra2=True
            print("Boton 1 presionado")
            time.sleep(0.5)
    
    
    #Led indicador de capacidad llena o no
    if(occupied<capacity):
        ledPin.write(1)
    else:
        ledPin.write(0)

    

# Delete the button object
del button

# Delete the button object
del button2

del ledPin
