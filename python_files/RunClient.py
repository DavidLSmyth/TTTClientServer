from TTTClient import TTTClient
from AIClient import AIBaseClient, OffensiveAI
import argparse
import threading
from music_utils import play_background_music
import configparser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch a client for a TTT game')
    choices = {'manual': TTTClient,'baseai': AIBaseClient, 'offensiveai': OffensiveAI}
    parser.add_argument('client', choices=choices, help='which type of client to launch')
    parser.add_argument('-p', metavar='PORT', type=int, default=10000,
                        help='TCP port (default 10000)')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('../conf/TTT.ini')
    print('Config file port: ', config['DEFAULT']['Port'])

    client = choices[args.client]
    Client = client('127.0.0.1', args.p)
    music_thread = threading.Thread(target=play_background_music)
    music_thread.start()
    Client.run_game()