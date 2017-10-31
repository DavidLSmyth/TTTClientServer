import unittest
import socket
import threading
import sys
sys.path.append('../python_files')
from python_files.util import recvall, get_block, put_block


class TestUtils(unittest.TestCase):

    def runServer(self, blocks):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 10000))
        self.sock.listen(1)
        self.sc, sockname = self.sock.accept()
        print('Accepted connection from', sockname)
        self.sc.shutdown(socket.SHUT_WR)
        while True:
            block = get_block(self.sc)
            if not block:
                break
            else:
                blocks.append(block)
        self.sc.close()
        self.sock.close()

    def runClient(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 10000))
        sock.shutdown(socket.SHUT_RD)
        put_block(sock, b'Beautiful is better than ugly.')
        put_block(sock, b'Explicit is better than implicit.')
        put_block(sock, b'Simple is better than complex.')
        put_block(sock, b'')
        sock.close()


    def test_get_block(self):
        blocks = []
        t1 = threading.Thread(target=self.runServer, args=(blocks,))
        t2 = threading.Thread(target=self.runClient)
        t2.start()
        t1.start()
        t1.join()
        t2.join()
        self.assertEqual(blocks, [b'Beautiful is better than ugly.',
                                  b'Explicit is better than implicit.',
                                  b'Simple is better than complex.'
                                  ])