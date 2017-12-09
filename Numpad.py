

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

MATRIX = 	               [['#',0,'*'],
		 	 [9,8,7],
		 	 [6,5,4],
		 	 [3,2,1]]


ROW = [37,32,36,40]
COL = [35,31,33]


def setup_numpad():
    for j in range(3):
            GPIO.setup(COL[j],GPIO.OUT)
            GPIO.output(COL[j],1)

    for i in range(4):
            GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def read_numpad():
    for j in range(3):
        GPIO.output(COL[j],0)
        for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    while(GPIO.input(ROW[i]) == 0):
                            pass
                    return MATRIX[i][j]
        GPIO.output(COL[j],1)

def destroy_numpad():
    GPIO.cleanup()


#try:
setup_numpad()
while(1):
    number = read_numpad()
    if number is not None and number is not last_number:
        print(number)
    last_number = number
        
#except KeyboardInterrupt:
#    destroy_numpad()
