'''The request object.'''
import string
import re
import pprint

class Request(object):
    
    # The supported methods
    # @type _supportedMethod: tuple
    _supportedMethod = (
            'OPTIONS', 
            'GET', 
            'HEAD', 
            'POST', 
            'PUT', 
            'DELETE', 
            'TRACE', 
            'CONNECT')
    _supportedHeaders = (
            'Accept', 
            'Accept-Charset', 
            'Accept-Encoding', 
            'Accept-Language', 
            'Authorization', 
            'Expect', 
            'From', 
            'Host', 
            'If-Match', 
            'If-Modified-Since', 
            'If-None-Match', 
            'If-Range', 
            'If-Unmodified-Since', 
            'Max-Forwards', 
            'Proxy-Authorization', 
            'Range', 
            'Referer', 
            'TE', 
            'User-Agent')
    
    _requestLine = {}
    _requestHeaders = {}
    _requestBody = None
    
    def __init__(self, requestData):
        self.requestData = requestData
        
        # parse the request
        self._parseRequest()
        
    def _parseRequest(self):
        data = self.requestData
        
        lines = data.splitlines()
        ln = 1
        for line in lines:
            self._parseRequestLine(ln, line.strip())
            ln = ln + 1
        
    def _parseRequestLine(self, lineNumber, line):
        r1 = re.compile('(GET|POST)\s(/[^\s]*)\s([^/]*)/(.*)')
        if r1.match(line):
            # it's the request line
            m = r1.match(line)
            self._requestLine['method'] = m.group(1)
            self._requestLine['file'] = m.group(2)
            self._requestLine['protocol'] = m.group(3)
            self._requestLine['protocol_version'] = m.group(4)
        elif line.find(':') != -1 :
            # it's a request header
            colonIndex = line.find(':')
            self._requestHeaders[line[:int(colonIndex)-1].strip()] = line[int(colonIndex)+1:].strip()
        else :
            # it's the request body
            self._requestBody = line.strip()

    def _validateRequest(self):
        pass
    
    def getRequestedFile(self):
        return self._requestLine['file']
    
    def isInvalid(self):
        return False
    
    def toString(self):
        requestString = ''
        # add the request-line
        requestString = requestString + self._requestLine['method'] + self._requestLine['file'] + self._requestLine['protocol'] + self._requestLine['protocol_version'] + '\n'
        # add the headers
        for header, value in self._requestHeaders.items():
            requestString = requestString + header + ': ' + value + '\n'
        # add the body
        requestString = requestString + 'Body:\n ' + self._requestBody + '\n'
        
        # return the string
        return requestString