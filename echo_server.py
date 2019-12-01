"""
A basic echo server
"""

import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    """ The server function """
    # set an address for our server
    address = ('127.0.0.1', 10000)
    data_chunk = 16
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    sock.bind(address)
    sock.listen(1)
    # pylint: disable=too-many-nested-blocks
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    data = conn.recv(data_chunk)
                    print('received "{0}"'.format(data.decode('utf8')))
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    if len(data) < data_chunk:
                        break
            except socket.error:
                traceback.print_exc()
                sys.exit(1)
            finally:
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        conn.close()
        print('quitting echo server', file=log_buffer)
        exit(1)
    # pylint: enable=too-many-nested-blocks

if __name__ == '__main__':
    server()
    sys.exit(0)
