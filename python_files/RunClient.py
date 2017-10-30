from TTTClient import TTTClient

if __name__ == '__main__':
    Client = TTTClient('127.0.0.1', 8080)
    Client.run_game()