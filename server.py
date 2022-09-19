import socket
import threading
import json
from colored import fg, bg, attr


class Client:
    def __init__(self, client, nickname):
        self.client = client
        self.nickname = client.nickname


clients = []


def broadcast(message, nickname='server'):
    for client in clients:
        d = {'nickname': nickname, 'message': message}
        # json_string = f'{{"nickname": "{nickname}", "message": "{message}"}}'
        json_string = json.dumps(d)
        client.send(json_string.encode('utf-8'))


def whisper(client, message):
    d = {'nickname': 'server', 'message': message}
    json_string = json.dumps(d)
    client.send(json_string.encode('utf-8'))

# json.dump({'nickname': client.nickname, message: message})


def serve_client(c):
    while True:
        try:
            # client = next(cl for cl in clients if cl.client == c)
            message = c.recv(1024).decode('ascii')
            broadcast(message)
        except:
            clients.remove(c)
            c.close()
            broadcast('Someone has left the room')
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
        whisper(c, 'Enter nickname:')
        nickname = c.recv(1024).decode('ascii')
        clients.append(c)
        broadcast(f'{nickname} has joined the room')
        thread = threading.Thread(target=serve_client, args=(c,))
        thread.start()


main()
