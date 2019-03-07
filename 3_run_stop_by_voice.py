from socket import *
from time import ctime
import time
import RPi.GPIO as GPIO
import motor


HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)

busnum = 1

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

motor.setup(busnum=busnum)
motor.setSpeed(50)
motor.stop()
while True:
    print('Receiving data')
    tcpCliSock,addr = tcpSerSock.accept()
    print('Received data : \n', addr)
    try:
        while True:
            data = ''
            data = tcpCliSock.recv(BUFSIZE)
            print(data)
            if not data:
                break            
            if data == "run":
                for i in range(10):
                    motor.forward()
                    time.sleep(0.001)
            elif data == "stop":
                motor.stop()
            else:
                print("hi")

                
    except KeyboardInterrupt:
        tcpSerSock.close()
