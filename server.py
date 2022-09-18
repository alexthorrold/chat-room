import socket
import threading
import json
from colored import fg, bg, attr


clients = []


def broadcast(message):
    for client in clients:
        client.send(message)


def serve_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(index)
            client.close()
            break


def main():
    host = '127.0.0.1'
    port = 31245

    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((host, port))
    ss.listen(5)
    print(f'%s Listening on port {port} %s' % (fg('yellow'), attr(0)))

    while True:
        c, address = ss.accept()
        print('Connected to:', address)
        c.send('Enter nickname:'.encode('ascii'))
        nickname = c.recv(1024).decode('ascii')
        clients.append(c)
        broadcast(f'{nickname} has joined the room'.encode('ascii'))
        thread = threading.Thread(target=serve_client, args=(c,))
        thread.start()


main()
