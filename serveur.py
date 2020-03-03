#!/usr/bin/env python
# coding: utf-8

import socket
import threading
from struct import unpack
import cv2
import sys
import numpy

def read_from_socket(sock, size):
    buffer = 1024
    bdata = bytearray()
    while len(bdata) < size:
        data = sock.recv(min(buffer, size - len(bdata)))
        if not data:
            raise ConnectionAbortedError
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
            while True:
                # Récupération header
                # Il faut avertir le serveur de la quantité de donnée à récupérer
                header = clientsocket.recv(20)
                try:
                    # Récupération de la frame + aussitôt rebond vers le poste de commandement
                    size = unpack(">q", data[12:20])[0]
                    frame = read_from_socket(clientsocket, size)
                    clientsocket2.PC_Thread.sendall(bytes(header))
                    clientsocket2.sendall(frame)
                except ConnectionAbortedError:
                    break

            print("Client déconnecté...")

        except Exception as e:
            print("ERROR!", sys.exc_info())
        finally:
            cv2.destroyAllWindows()

# On acceuille le poste de commandement
class PC_Thread(threading.Thread):

    def __init__(self, ip2, port2, clientsocket2):
        threading2.Thread.__init__(self)
        self.ip2 = ip2
        self.port2 = port2
        self.clientsocket2 = clientsocket2
        print("[+] Nouveau thread pour %s %s" % (self.ip2, self.port2,))

    def run(self):
        print("Connexion de %s %s" % (self.ip2, self.port2,))


tcpsock = tcpsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

# Ne fonctionne pas, on ne peut bind qu'un seul port visiblement même avec un autre tcpsocket

tcpsock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock2.bind(("", 1112))



while True:
    tcpsock.listen(10)
    tcpsock2.listen(10)
    print("En écoute...")

    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()

    (clientsocket2, (ip2, port2)) = tcpsock2.accept()
    newthread2 = PC_Thread(ip2, port2, clientsocket2)
    newthread2.start()
