#!/usr/bin/env python
# coding: utf-8

import socket
import threading
import sys

clients = []

def read_from_socket(sock, size):
    buffer = 1024
    bdata = bytearray()
    while len(bdata) < size:
        # print("len(bdata) = {}".format(len(bdata)))
        data = sock.recv(min(buffer, size - len(bdata)))
        # if not data:
        #     raise ConnectionAbortedError
        bdata += data
    return bytes(bdata)

# On acceuille le pilote de drone
class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port,))
        try:
            # Récupération header
            # Il faut avertir le serveur de la quantité de donnée à récupérer
            header = clientsocket.recv(10)
            if len(header.decode().split(";")) > 1:
                # print(header.decode().split(";"))
                size = int(header.decode().split(";")[1])
                if int(header.decode().split(";")[0]) == 1:
                    clientsocket.send(b"ok")
                    clients.remove(clientsocket)
                    socket_pilote = clientsocket
                    while 1:
                        try:
                            texte = read_from_socket(socket_pilote, size)
                        except Exception as e:
                            print("connexion avec le pilote perdue")
                            break
                        if clients:
                            for client in clients:
                                try:
                                    client.sendall(texte)
                                except Exception as e:
                                    print("connexion avec le poste de commandement perdue")
                                    clients.remove(client)
                                    print("suppression du poste de commandement dans la liste des clients")

        except Exception as e:
            print("ERROR!", sys.exc_info())
        # finally:
        #     cv2.destroyAllWindows()


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    clients.append(clientsocket)
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()