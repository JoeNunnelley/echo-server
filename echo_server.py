"""
A basic echo server with multi-client select() processing
"""

import select
import socket
import sys
import traceback
import queue


# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def server(log_buffer=sys.stderr):
    """ The server function """
    # set an address for our server
    address = ('127.0.0.1', 10000)
    data_chunk = 16
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    sock.bind(address)
    sock.listen(5)

    inputs = [sock]
    outputs = []

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while inputs:
            try:
                print('waiting for a connection', file=log_buffer)
                # only concerned with readers in this scenario
                readers, _, _ = select.select(inputs,
                                              outputs,
                                              inputs)

                for reader in readers:
                    # add connections to input connection array
                    if reader is sock:
                        conn, addr = sock.accept()
                        print("new connection client: {0}:{1}".format(*addr))
                        conn.setblocking(0)
                        inputs.append(conn)
                    else:
                        try:
                            print('connection - {0}:{1}'.format(*addr),
                                  file=log_buffer)
                            # the inner loop will receive messages sent by
                            # the client in buffers.  When a complete message
                            # has been received, the loop will exit
                            while True:
                                data = reader.recv(data_chunk)
                                print('received "{0}"'.format(data
                                                              .decode('utf8')))
                                if data:
                                    reader.sendall(data)
                                    print('sent "{0}"'.format(data
                                                              .decode('utf8')))
                                else:
                                    print('message complete.\nclosing'
                                          ' connection. {0}:{1}'.format(*addr))
                                    inputs.remove(reader)
                                    reader.close()
                                    break

                        except socket.error as ex:
                            if str(ex) == "[Errno 35] Resource temporarily" \
                                          " unavailable":
                                continue
                            else:
                                traceback.print_exc()
                                sys.exit(1)

            except select.error:
                print("No further clients")
                break

    except KeyboardInterrupt:
        print('quitting echo server', file=log_buffer)
        exit(1)
    finally:
        for reader in inputs:
            print('closing connection {}'.format(reader))
            reader.close()

        print('echo complete, client connections closed',
              file=log_buffer)
# pylint: enable=too-many-nested-blocks
# pylint: enable=too-many-branches
# pylint: enable=too-many-statements


if __name__ == '__main__':
    server()
    sys.exit(0)
