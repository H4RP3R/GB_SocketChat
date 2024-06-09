import socket
import threading
import pickle
import sys
from time import sleep


def listen(sock):
    while True:
        data = sock.recv(1024)
        if data:
            msg = pickle.loads(data)
            display_message(msg)


def write(sock, username):
    while True:
        text = input()
        msg = {'username': username, 'text': text}
        sock.sendall(pickle.dumps(msg))


def display_message(msg):
    print(f'{msg["username"]}: {msg["text"]}')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                sock.connect(('127.0.0.1', 55555))
                break
            except ConnectionRefusedError:
                print('trying to connect ...')
                sleep(5)

        username = input('Enter your name: ').strip()
        print(f'Welcome, {username}!')

        writer = threading.Thread(target=write, args=(sock, username))
        writer.daemon = True
        writer.start()

        listener = threading.Thread(target=listen, args=(sock, ))
        listener.daemon = True
        listener.start()
        listener.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\bBye!')
        sys.exit(0)
