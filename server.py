import socket
import pickle
import threading
from loguru import logger


connections = {}


def listen(conn, addr):
    try:
        logger.info(f'New connection: {addr}')
        while True:
            data = conn.recv(1024)
            msg = pickle.loads(data)
            if data:
                logger.info(f'{msg["username"]}: {msg["text"]}')
    except (ConnectionResetError, EOFError):
        logger.info(f'{addr} has disconnected')
        conn.close()
        del connections[addr]
        logger.debug(f'Total connections: {len(connections)}')


def resend(msg, conn):
    pass


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
            listener.start()


if __name__ == '__main__':
    main()
