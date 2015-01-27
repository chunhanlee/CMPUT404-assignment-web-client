#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import socket
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    path = ""
    host = ""
    port = 80
    
    def get_host_port(self,url):
        #https://docs.python.org/2/library/urlparse.html
        spliturl = urlparse(url)
        self.host = spliturl.hostname
        
        if (spliturl.path == ""):
            self.path = "/"
        else:
            self.path = spliturl.path

        if (spliturl.port != None):
            self.port = spliturl.port


    def connect(self, host, port):
        # use sockets!
        #https://docs.python.org/2/library/socket.html
        sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets.connect((host,port))
        return sockets

    def get_code(self, data):
        UrlCode = int(data.split()[1])
        return UrlCode

    def get_headers(self,data):
        pack_header = data.split("\r\n\r\n")[0]
        return pack_header

    def get_body(self, data):
        pack_body = data.split("\r\n\r\n")[1]
        return pack_body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        self.get_host_port(url)
        
        conn = self.connect(self.host, self.port)
        
        httpRequest = "GET %s HTTP/1.1\r\n" % self.path +\
                      "Host: %s\r\n" % self.host +\
                      "Accept: */*\r\n\r\n"
        
        conn.sendall(httpRequest)
        data = self.recvall(conn)
        return HTTPRequest(self.get_code(data), self.get_body(data))

    def POST(self, url, args=None):
        self.get_host_port(url)
        
        conn = self.connect(self.host, self.port)
        
        httpRequest = "POST %s HTTP/1.1\r\n" % self.path +\
                      "Content-Type: application/x-www-form-urlencoded"
        
        if (args == None):
            httpRequest + "Content-Length: 0\r\n\r\n"
        else:
            encodeArg = urllib.urlencode(args)
            lenarg = str(len(encodeArg))
            httpRequest + "Content-Length: %s\r\n\r\n" % lengarg +\
                          encodeArg
        
        conn.sendall(httpRequest)
        data = self.recvall(conn)
        return HTTPRequest(self.get_code(data),self.get_body(data) )

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
