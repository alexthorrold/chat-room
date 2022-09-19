import socket
import threading
import json
from colored import fg, bg, attr


class User:
    def __init__(self, client, nickname):
        self.client = client
        self.nickname = nickname


users = []


def broadcast(message, nickname='server'):
    d = {'nickname': nickname, 'message': message}
    json_string = json.dumps(d)

    for user in users:
        user.client.send(json_string.encode('utf-8'))


def whisper(client, message):
    d = {'nickname': 'server', 'message': message}
    json_string = json.dumps(d)
    client.send(json_string.encode('utf-8'))


def serve_client(c):
    while True:
        try:
            message = c.recv(1024).decode('ascii')
            nickname = next(cl for cl in users if cl.client == c).nickname
            broadcast(message, nickname)
        except:
            users.remove(next(cl for cl in users if cl.client == c))
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
        while nickname == 'server':
            whisper(c, 'Invalid nickname')
            whisper(c, 'Enter nickname:')
            nickname = c.recv(1024).decode('ascii')

        client = User(c, nickname)
        users.append(client)
        broadcast(f'{nickname} has joined the room')
        thread = threading.Thread(target=serve_client, args=(c,))
        thread.start()


main()
