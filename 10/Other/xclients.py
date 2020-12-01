import sys
import threading

sys.path.append("../Fish/Remote")

from client import Client

DEBUG = False


def xclients(num_clients, port, ip_address):
    if DEBUG:
        Client.DEBUG = True

    clients = [Client(str(index)) for index in range(num_clients)]

    threads = list()

    for client in clients:
        c_thread = threading.Thread(target=thread_func, args=(client, port, ip_address,))
        threads.append(c_thread)
        c_thread.start()

    for thread in threads:
        thread.join()


def thread_func(client, port, ip_address):
    if DEBUG:
        print(f'Running thread for {client.name}...')

    # default: ('localhost', 3000)
    client.run(ip_address, port)

    if DEBUG:
        print(f'Stopping thread for {client.name}...')
