import socket
import pickle
import threading
import sys
from loguru import logger


connections = {}


def listen(conn, addr):
    try:
        logger.info(f'New connection: {addr}')
        while True:
            data = conn.recv(1024)
            msg = pickle.loads(data)
            if data:
                resend(msg, addr)
                logger.info(f'{msg["username"]}: {msg["text"]}')
    except (ConnectionResetError, EOFError):
        logger.info(f'{addr} has disconnected')
        conn.close()
        del connections[addr]
        logger.debug(f'Total connections: {len(connections)}')


def resend(msg, source_addr):
    for a, c in connections.items():
        if a != source_addr:
            c.sendall(pickle.dumps(msg))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 55555))
        sock.listen()
        logger.info('Server is running, please, press ctrl+c to stop')

        while True:
            conn, addr = sock.accept()
            connections[addr] = conn
            logger.debug(f'Total connections: {len(connections)}')
            listener = threading.Thread(target=listen, args=(conn, addr))
            listener.daemon = True
            listener.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\b\bBye!')
        sys.exit(0)
