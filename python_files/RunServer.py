from TTTServer import TTTSocketServer

if __name__ == '__main__':
    server = TTTSocketServer('localhost', 10000)
    server.start()
    server.run_game()