'''Class handles client connections to the server.'''
import string, socket
import threading

class Client(threading.Thread):

    def __init__(self, (socket, (host, port))):
        threading.Thread.__init__(self) 
        self.socket = socket
        self.host = host
        self.port = port
        self.size = 1024
        
        print 'Handling connection from ' + self._getFullHost()
        
    def run(self):
        motd = open('config/motd', 'r')
        self.socket.send(motd.read())
        motd.close()
        
        self.socket.send('''> ''')
        
        running = 1
        while running:
            data = self.socket.recv(self.size)
            if data:
                self.socket.send(self._cleanData(data))
                self.socket.send('\n> ')
            else:
                self.socket.close()
                print 'Connection for ' + self._getFullHost() + ' closed'
                running = 0 
        
    def _cleanData(self, data):
         clean = string.strip(data)
         clean = string.strip(clean, '\r')
         clean = string.strip(clean, '\n')
         clean = string.strip(clean, '\'')
    
         return clean

    def _getFullHost(self):
        return self.host + ':' + str(self.port)