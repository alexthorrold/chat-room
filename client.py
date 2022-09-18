import socket
import os
import threading
from colored import fg, bg, attr


os.system('clear')

host = '127.0.0.1'
port = 31245

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


def receive():
    while True:
        try:
            message = s.recv(1024).decode('ascii')
            print(message)
        except ConnectionRefusedError:
            print('An error has occured')
            s.close()
            break


def write():
    while True:
        message = input()
        s.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
