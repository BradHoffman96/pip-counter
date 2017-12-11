import time
import smbus
from multiprocessing import Queue


ADDR = 0x20
DIRA = 0x00
DIRB = 0x01
PORTA = 0x12
PORTB = 0x13
numbers = [[0b0111110,0b1000001,0b1000001,0b0111110],[0b1000001,0b1000001,0b1111111,0b0000001],[0b1001111,0b1001001,0b1001001,0b1111001],[0b1000001,0b1001001,0b1001001,0b1111111],[0b1111000,0b0001000,0b0001000,0b1111111],[0b1111001,0b1001001,0b1001001,0b1000111],[0b1111111,0b1001001,0b1001001,0b1001111],[0b1000000,0b1000000,0b1000000,0b1111111],[0b1111111,0b1001001,0b1001001,0b1111111],[0b1111000,0b1001000,0b1001000,0b1111111]]

bus = smbus.SMBus(1)

def initDisplay():
    bus.write_byte_data(ADDR,DIRA,0x00);
    bus.write_byte_data(ADDR,DIRB,0x00);

def turnOffLeds():
    bus.write_byte_data(ADDR,PORTA,0x00);
    bus.write_byte_data(ADDR,PORTB,0x00);


def turnOnLeds():
    bus.write_byte_data(ADDR,PORTA,0xFF);
    bus.write_byte_data(ADDR,PORTB,0x00);

def setLed(row,col):
    bus.write_byte_data(ADDR,PORTA,0x80>>col);
    bus.write_byte_data(ADDR,PORTB,~(1<<row));

def setColumn(row,data):
    bus.write_byte_data(ADDR,PORTB,0xFF);
    bus.write_byte_data(ADDR,PORTA,data);
    bus.write_byte_data(ADDR,PORTB,~(1<<row));

def setRow(column, data):
    bus.write_byte_data(ADDR,PORTA,0x00);
    bus.write_byte_data(ADDR,PORTB,~data);
    bus.write_byte_data(ADDR,PORTA,0x80>>column);


def display_number(data):
    bcd = []
    try:
        if(len(data) is 1):
            bcd.append(0)
            bcd.append(int(data[0]))
        else:
            bcd.append(int(data[0]))
            bcd.append(int(data[1]))
    except:
        return
    for i in range(0,2):
        for j in range(0,4):
            setColumn(j+4*i, numbers[bcd[1-i]][3-j]<< (i))
            time.sleep(0.001)

def sub_process(q):
    initDisplay()
    number = '3'
    while(1):
        if q.qsize() > 0:
            number = q.get()
        display_number(number)    
    


#Main program
if __name__ == '__main__':
    initDisplay()
    turnOnLeds()
    time.sleep(1)
    turnOffLeds()
    time.sleep(1)
        
    while(1):
        for i in range(0,100):
            for j in range(0,50):
                display_number(str(i))
            turnOffLeds()










    
