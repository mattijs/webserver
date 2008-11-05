'''The response object.'''
import os, sys, string
import datetime

class Response(object):
    
    def __init__(self, server, request):
        self._server = server
        self._request = request
        
        self._statusLine = {}
        self._responseHeaders = {}
        self._responseBody = None
        
        # fill the response object
        self._buildResponse()
    
    def _buildResponse(self):
        # check file and build body
        self._buildResponseBody()
        # add corresponding headers
        self._buildResponseHeader()
    
    def _buildResponseHeader(self):
        # calculate the date
        date = datetime.datetime.now()
        formattedDate = date.strftime('%a, %d %b %Y %H:%M:%S %Z')
        self._addResponseHeader('Date', str(formattedDate))
        self._addResponseHeader('Server', 'Monkey Server/0.1')
        self._addResponseHeader('Connection', 'close')
    
    def _setStatusLine(self, statusCode, reasonPhrase):
        self._statusLine['HTTP-Version'] = 'HTTP/1.1'
        self._statusLine['Status-Code'] = str(statusCode)
        self._statusLine['Reason-Phrase'] = reasonPhrase
    
    def _buildResponseBody(self):
        self._responseBody = ''
        # full path for the requested file/directory
        requestFileFullPath = self._server.documentRoot + self._request.getRequestedFile()
        # check if the request contained a directory or a file
        if os.path.basename(requestFileFullPath) == '':
            # check if the directory exists
            if not os.path.isdir(requestFileFullPath):
                self._setStatusLine('404', 'Not Found')
                return
            # check if one of the index files exists
            indexDocuments = self._server.documentIndex
            indexFound = False
            for doc in indexDocuments:
                if os.path.isfile(requestFileFullPath + doc):
                    requestFileFullPath += doc
                    indexFound = True
                    break
            
            if not indexFound:
                # no index file found
                self._setStatusLine('404', 'Not Found')
                return
        elif not os.path.isfile(requestFileFullPath) :
            self._setStatusLine('404', 'Not Found')
            return
        
        # the requested file was ok, read it's contents
        rfhandler = open(requestFileFullPath)
        self._responseBody += rfhandler.read()
        rfhandler.close()
        # add a content type to the header
        self._addResponseHeader('Content-Type', 'text/html')
        
        # build the status line
        self._setStatusLine('200', 'OK')
    
    def _getFullFilePath(self, requestedFile):
        # check if the request was for a file or a directory
        if os.path.isdir(requestedFile):
            pass

    def _addResponseHeader(self, name, value):
        self._responseHeaders[name] = value
    
    def returnResponse(self):
        # build the status line
        statusLine = self._statusLine
        responseStatusLine = string.join([statusLine['HTTP-Version'], statusLine['Status-Code'], statusLine['Reason-Phrase']], ' ') + '\r\n' 

        # build the response headers
        responseHeader = ''
        for header, value in self._responseHeaders.items():
            responseHeader += header + ': ' + value + '\r\n'
        
        # combine the data in one string
        responseString = responseStatusLine
        responseString += responseHeader
        # add an extra CRLF before the body
        responseString += '\r\n'
        responseString += self._responseBody
        
        # return the response
        return responseString
