#@todo: fix python include path
import socket, string
from Server import Server

def main():
    s = Server.Server('config/config.ini')
    s.run()
        

# run the main program
main()
