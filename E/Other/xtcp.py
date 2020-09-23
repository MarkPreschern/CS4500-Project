#!/usr/bin/python3

# Imports
import argparse
import json
import socket
import time

# Local Imports
from xjson import get_json_vals

# Constants
DEFAULT_PORT = 4567
SERVER_TIMEOUT = 10
CLIENT_TIMEOUT = 1
HOSTNAME = 'localhost'


def initialize_socket(port):
    """
    Return a socket that is capable of TCP communication.

    :return: a socket object that is ready for TCP communication or None if unsuccessful.
    """
    global SERVER_TIMEOUT, CLIENT_TIMEOUT, HOSTNAME

    # Initialize a socket that is capable of TCP communication and has the specified wait time
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SERVER_TIMEOUT)

    try:
        # Bind the socket to a specific host/port and listen for new connections
        sock.bind((HOSTNAME, port))
        sock.listen(1)

        # Attempt to connect after listening
        connection = sock.accept()[0]
        connection.settimeout(CLIENT_TIMEOUT) 

        # Return a new socket that is connected to the host at the specified port
        return connection
    except ConnectionRefusedError:
        print("Error: connection refused.")
    except socket.timeout:
        print("Error: timeout")

    return None


def initialize_arg_parser():
    """
    Initialize a parser that can accept and process command line arguments.

    :return: a parser that accepts the desired arguments (i.e. port)
    """
    parser = argparse.ArgumentParser(
        description="Parse JSON values from an input stream over a TCP connection.")
    parser.add_argument("port", nargs="?", type=int,
                        help="The port used by the script for communication.")

    return parser


def receive_json(sock):
    """
    Receive a string containing well-formed JSON values from the socket.

    :param sock: the socket object from which data will be received.
    :return: a string containing all of the well-formed JSON values received.
    """
    json_data = b''

    # Listen for data and add to the string until all data has been received from the client.
    while True:
        try:
            new_data = sock.recv(1)
            json_data = json_data + new_data

            if new_data == b'':
                break

        except socket.timeout:
            break

    return json_data


def convert_json_vals(vals):
    """
    Convert the provided list of JSON values into JSON objects describing their count/sequence.

    : param vals: a list of well-formed JSON values
    : return: a tuple containing a JSON object and a JSON list both describing sequence/count
    """
    # Create the JSON object / list
    obj1 = {"count": len(vals), "seq": vals}
    obj2 = [len(vals)]
    obj2.extend(vals[::-1])

    # Return the two objects in a tuple
    return (json.dumps(obj1), json.dumps(obj2))


def send_json(sock, data):
    """
    Send data through the socket connection.
    
    :param sock: a socket object connected to a port
    :param data: the data to be sent 
    """
    # Send all data from the JSON object and the JSON list
    sock.sendall(bytes(data[0], 'utf-8'))
    sock.sendall(bytes(data[1], 'utf-8'))


def xtcp():
    """
    Main program logic.
    """
    global DEFAULT_PORT

    # Parse command line arguments
    parser = initialize_arg_parser()
    args = vars(parser.parse_args())

    # Initialize the TCP socket
    sock = initialize_socket(args['port'] if args['port'] else DEFAULT_PORT)

    if sock:
        # Accept string data from the socket
        incoming_json = receive_json(sock)

        # Parse the string data received from the socket into distinct JSON values
        json_vals = get_json_vals(incoming_json.decode("utf-8"))

        # Process the JSON values into the proper JSON object/list
        outgoing_json = convert_json_vals(json_vals)

        # Send the JSON objects through the socket
        send_json(sock, outgoing_json)

        # Close the socket connection
        sock.close()

