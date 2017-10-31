import socket
import struct

header_struct = struct.Struct('!I')  # messages up to 2**32 - 1 in length


def recvall(sock: socket.socket, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left'
                           ' in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def get_block(sock):
    data = recvall(sock, header_struct.size)
    (block_length,) = header_struct.unpack(data)
    return recvall(sock, block_length)


def put_block(sock, message):
    block_length = len(message)
    try:
        sock.send(header_struct.pack(block_length))
        sock.send(message)
    except OSError as e:
        print('Couldnt send message {} to {} due to error'.format(message, sock))
