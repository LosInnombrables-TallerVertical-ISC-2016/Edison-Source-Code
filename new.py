import time
import pyupm_buzzer as upmBuzzer
import pyupm_grove as grove
import mraa
import pyupm_i2clcd as lcd
import sys
import random


counter = 0
counter = 2
# Create the button object using GPIO pin 0
button = mraa.Gpio(2)
button2 = mraa.Gpio(3)
# Create the buzzer object using GPIO pin 5
buzzer = upmBuzzer.Buzzer(3)
button.dir(mraa.DIR_IN)
button2.dir(mraa.DIR_IN)

ledPin = mraa.Gpio(4)
ledPin.dir(mraa.DIR_OUT)
ledPin.write(0)


chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA, 
          upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO, 
          upmBuzzer.SI];

#Crete the lcd object 
lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)
lcdDisplay.setColor(0,0,0)
entra=False

lcdDisplay.write(str(counter))

# Read the input and print, waiting one second between readings
while 1:
    if(button.read() != 0):
        entra=True
        ledPin.write(1)
        print("Boton 1 presionado")
    
    if(button2.read()!=0 & entra):
        lcdDisplay.setCursor(0, 0)
        counter = counter + 1
        lcdDisplay.write(str(counter))
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        lcdDisplay.setColor(r,g,b)
        print("Boton 2 presionado")
        time.sleep(1.0)
        ledPin.write(0)
        entra=False
    
    

# Delete the buzzer object
del buzzer

# Delete the button object
del button

# Delete the button object
del button2
