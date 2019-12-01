import socket
import sys
import traceback

SERVER = 'localhost'
PORT = 10000

def client(msg, log_buffer=sys.stderr):
    server_address = (SERVER, PORT)
    data_chunk = 16
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.settimeout(2)

    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    sock.connect(server_address)

    # entire message
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf-8'))

        while True:
            chunk = sock.recv(data_chunk)
            received_message += chunk.decode('ascii')
            print('received "{0}" len {1}'.format(chunk.decode('utf8'),
                                                  len(chunk)),
                                          file=log_buffer)

            if not chunk or len(chunk) == 0:
                break

    except socket.timeout:
        print('message end')
    except Exception:
        traceback.print_exc()
        print("Exception {}".format(sys.exc_info()[0]))
        sys.exit(1)
    finally:
        sock.close()
        print('closing socket', file=log_buffer)

    return received_message

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
