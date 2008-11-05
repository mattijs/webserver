'''Handles incomming requests to the server and sends out the response.'''
import string
import socket
import threading
import Request
import Response

class RequestHandler(threading.Thread):

    def __init__(self, server, (socket, (host, port))):
        threading.Thread.__init__(self)
        
        # The server this handler is working for
        self._server = server
        # The client socket the connection is made from
        self._socket = socket
        # The client host the connection is made from
        self._host= host
        # The client port the connection is made from
        self._port = port
        # The read buffer size
        self._size = 8192
        
        #self.logRequest('Handling connection from ' + self._getFullClientAddress())
        
        
    def run(self):
        requestData = self._socket.recv(self._size)
        
        # create a new request object
        request = Request.Request(requestData)
        
        # create a new response object
        response = Response.Response(self._server, request)
        
        # send the response
        self._socket.send(response.returnResponse())
        
        # close the connection
        self._socket.close()
        
    def logRequest(self, request):
        requestLog = open('logs/request.log', 'a')
        requestLog.write(request + '\n')
        requestLog.close()
        
    
    def _getFullClientAddress(self):
        '''Returns the full address for the client socket.'''
        return self._host + ':' + str(self._port)