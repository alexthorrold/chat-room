import socket
import os
import threading
import json
from colored import fg, bg, attr


host = '127.0.0.1'
port = 31245

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

messages = []


def receive():
    while True:
        try:
            data = s.recv(1024).decode('utf-8')
            json_object = json.loads(data)
            messages.append(json_object)

            os.system('clear')

            for m in messages:
                nickname = m.get('nickname')
                message = m.get('message')
                if nickname != 'server':
                    message = f'{nickname}: {message}'
                print(message)

        except:
            print('An error has occurred')
            s.close()
            break


def write():
    while True:
        message = input('')
        s.send(message.encode('ascii'))
        # print('\r')

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
