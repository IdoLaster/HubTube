"""
    Author: Ido Laster
    Description: Constants file for the server.
    Date: 5.5.2017
"""
# Networking related constants:
LISTENING_IP = "0.0.0.0"
PORT = 80
Q_LEN = 10
RECV_LENGTH = 1024
RECV_LENGTH = 1024
CLIENT_TIMEOUT = 2

# HTTP related constants:
WEB_ROOT = "./web_root/"
DEFAULT_PAGE = "gui.html"
HTTP_RESPONSES = {"OK": 'HTTP/1.1 200 OK\r\n',
                  "NOT FOUND": 'HTTP/1.1 404 NOT FOUND\r\n',
                  'BAD REQUEST': "HTTP/1.1 400 BAD REQUEST\r\n",
                  "SERVER ERROR": "HTTP/1.1 500 INTERNAL SERVER ERROR\r\n"}
HTTP_CONTENT_TYPES = {"html": "Content-Type: text/html; charset=utf-8\r\n",
                 "jpg": "Content-Type: image/jpeg\r\n",
                 "css": "Content-Type: text/css\r\n",
                 "js": "Content-Type: text/javascript; charset=UTF-8\r\n",
                 "ico": "Content-Type: image/x-icon\r\n",
                 "json": "Content-Type: application/json\r\n",
                 "text": "Content-Type: text/plain\r\n"}
NEW_LINE = "\r\n"
HTTP_CONTENT_LENGTH = "Content-Length: {}\r\n"
SONG_REQUEST = "request_song"  # << If you want to change the GET of the js server it's this one

# Messages:
SERVER_INIT_ERROR = "Server initialization failed: {}"
LISTENING_STARTED = "Listening started at port: {}"
NEW_CLIENT = "New client connected: {}:{}"
CLIENT_ERROR_OCCURRED = "Client error occurred: "
CLIENT_TIMEDOUT = "Client timed out, closing connection."
ERROR_OCCURRED = "General error occurred: {}"
SERVER_TERMINATED = "Server forced to close by user."
