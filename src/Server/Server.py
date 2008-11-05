'''Creates a new server with the specified configuration.'''
import os.path
import select
import socket
import sys
import threading
import ConfigParser
import RequestHandler

class Server(object):
    
    def __init__(self, configFile):
        print 'Initializing server ...'
        
        print 'Reading configuration from ' + os.path.abspath(configFile)
        config = ConfigParser.ConfigParser()
        config.read(configFile)
        
        self.host = config.get('server', 'host')
        self.port = config.getint('server', 'port')
        self.backlog = config.getint('server', 'backlog')
        self.readSize = 1024
        self.socket = None
        self.threads = []
        # the directory files will be served from
        self.documentRoot = config.get('server', 'documentRoot')
        # files that will be displayed when no filename was given
        self.documentIndex = []
        indexDocumentsString = config.get('server', 'indexOrder')
        indexDocuments = indexDocumentsString.split(',')
        for indexDocument in indexDocuments:
            self.documentIndex.append(indexDocument)
        
        print 'Checking document root ...'
        if not os.path.isdir(self.documentRoot):
            print 'Given document "' + self.documentRoot + '" does not exist'
            exit(1)
        
    def run(self):
        '''Runs the server'''
        self._openSocket()
        input = [self.socket,sys.stdin] 
        running = 1
        
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            
            for s in inputready: 
                if s == self.socket: 
                    # create a new request handler to handle the request
                    handler = RequestHandler.RequestHandler(self, self.socket.accept())
                    handler.start()
                    self.threads.append(handler) 
                elif s == sys.stdin: 
                     # handle standard input
                    servercommand = sys.stdin.readline()
                    if(servercommand == 'quit\n') :
                        print 'Recieved system command, closing server ...'
                        running = 0
                    else :
                        print '''Command ''' + servercommand + ''' not found.''' 
                    
        # close all threads
        self._closeSocket()
        print 'Socket closed.'
        for handler in self.threads:
            handler.join()
        print 'Server shut down'
                    
    def _openSocket(self):
        '''Creates a socket for the server where clients can connect to.'''
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host,self.port))
            self.socket.listen(self.backlog)
            print 'Server started, listening for connections on ' + self.host + ':' + str(self.port) + ' ...'
        except socket.error, (value,message):
            if self.socket:
                self.socket.close()
            print "Could not open socket: " + message
            sys.exit(1) 
            
    def _closeSocket(self):
        '''Closes the servers socket.'''
        if self.socket:
            self.socket.close()
