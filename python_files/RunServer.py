from TTTServer import TTTSocketServer

if __name__ == '__main__':
    server = TTTSocketServer('localhost', 8080)
    server.start()