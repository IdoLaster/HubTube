"""
    Author: Ido Laster
    Description: The main file of the project, that's inits the server
                 wait for requests and response to them.
    Date: 5.5.2017
"""
from threading import Thread
from threading import Lock
from SongRequest import SongRequest
import socket
import sys
import os
import json
sys.path.append(".")
import Constants

global playlist
playlist = []
global lock
lock = Lock()


def handle_request(client_socket, method, resource, full_request, client_ip):
    """
    Handling the client request by checking the method, if the request file
    exists(in case of GET requests) etc.
    @param client_socket: The client Socket instance.
    @param method: The request method (GET/POST).
    @param resource: The name of the requested file/data.
    @param full_request: The entire request.
    @return: None
    """
    if method == "GET ":
        if resource == '':
            # In case the resource in empty we would like to navigate it to
            # The default page.
            resource = Constants.DEFAULT_PAGE
        if resource != Constants.SONG_REQUEST:
            file_type = resource.split("/")[-1].split(".")[-1]
            file_name = resource.split("/")[-1]
            if os.path.isfile(Constants.WEB_ROOT + file_name):
                # If the file exists, we would extract the data out of it
                # And send it with the matching HTTP Headers.
                response_headers = Constants.HTTP_RESPONSES["OK"]
                data = ""
                with open(Constants.WEB_ROOT + file_name, "r") as f:
                    data = f.read()
                if file_type in Constants.HTTP_CONTENT_TYPES.keys():
                    response_headers += Constants.HTTP_CONTENT_TYPES[file_type]
                else:
                    response_headers += Constants.HTTP_CONTENT_TYPES['text']
                response_headers +=\
                    Constants.HTTP_CONTENT_LENGTH.format(str(len(data)))
                response_headers += Constants.NEW_LINE
                client_socket.send(response_headers + data)
            else:
                # Otherwise, we will just send 404.
                client_socket.send(Constants.HTTP_RESPONSES['NOT FOUND'])
        else:
            if client_ip == "127.0.0.1":
                if len(playlist) > 0:
                    # Here we are just getting the first song from the list
                    # putting together the matching headers and sending
                    # it to the
                    # JS Server.
                    lock.acquire()
                    current_song = playlist.pop(0)
                    lock.release()
                    http_headers = Constants.HTTP_RESPONSES['OK']
                    http_headers += Constants.HTTP_CONTENT_TYPES['json']
                    http_headers += Constants.HTTP_CONTENT_LENGTH.format(
                        len(str(current_song.to_json())))
                    http_headers += Constants.NEW_LINE
                    client_socket.send(http_headers +
                                       str(current_song.to_json()))
                else:
                    # If the list is empty, we will send 'Not found'.
                    client_socket.send(Constants.HTTP_RESPONSES['NOT FOUND'])
            else:
                client_socket.send(Constants.HTTP_RESPONSES['NOT FOUND'])

    elif method == "POST ":
        if resource == Constants.SONG_REQUEST:
            # Here we would like to save the song request from the client.
            try:
                data = full_request.split('\r\n\r\n')[-1]
                request_data = json.loads(data)
                song_request = SongRequest(request_data[u'video-url'],
                                           request_data[u'name'])
                if song_request.valid_url():
                    lock.acquire()
                    playlist.append(song_request)
                    lock.release()
                    client_socket.send(Constants.HTTP_RESPONSES['OK'])
                else:
                    client_socket.send(Constants.HTTP_RESPONSES['BAD REQUEST'])
            except Exception as err:
                client_socket.send(Constants.HTTP_RESPONSES['SERVER ERROR'])
                print Constants.ERROR_OCCURRED.format(str(err))


def validate_http_request(request):
    """
    Checking if the request is valid by HTTP standards.
    @param request: The full request of the user.
    @return: boolean that indicates if the request is valid or not,
             Also the resource and the method of the request
    """
    request_parts = request.split("\r\n")[0].split("/")
    resource = "/".join(request_parts[1:-1]).split(" ")[0]
    method = request_parts[0]
    if len(request_parts) < 3:
        return False, '', ''
    if "HTTP" in request_parts[-2]:
        if "1.1" in request_parts[-1]:
            return True, resource, method
    else:
        return False, resource, method


def handle_client(client_socket, client_address):
    """
    Here are doing basic client handing, we get his request and moving it
    forward to handle_client_request.
    @param client_socket: The client socket instance.
    @param client_address: The client (IP,PORT).
    @return: None
    """
    try:
        # Here we are just getting new client and check if his request is good
        # If it is we will move it forward, otherwise we will send back bad
        # Request.
        print Constants.NEW_CLIENT.format(client_address[0], client_address[1])
        client_request = client_socket.recv(Constants.RECV_LENGTH)
        valid_request, resource, method = validate_http_request(client_request)
        if valid_request:
            handle_request(client_socket, method, resource,
                           client_request, client_address[0])
        else:
            client_socket.send(Constants.HTTP_RESPONSES['BAD REQUEST'])
    except socket.timeout as err:
        print Constants.CLIENT_TIMEDOUT
    except socket.error as err:
        print Constants.CLIENT_ERROR_OCCURRED.format(str(err))
    finally:
        client_socket.close()


def main():
    """
    This is the main function, here we just initializing the server
    and creating threads for each new client :)
    @return: None
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((Constants.LISTENING_IP, Constants.PORT))
        server.listen(Constants.Q_LEN)
        print Constants.LISTENING_STARTED.format(str(Constants.PORT))
        while True:
            client_socket, client_address = server.accept()
            thread = Thread(target=handle_client,
                            args=(client_socket, client_address))
            thread.start()
    except socket.error as err:
        print Constants.SERVER_INIT_ERROR.format(str(err))
    except KeyboardInterrupt:
        print Constants.SERVER_TERMINATED
    finally:
        server.close()


if __name__ == '__main__':
    main()
