#!/usr/bin/env python
# coding: utf-8

import socket
import threading
from struct import unpack
import sys
import numpy

def read_from_socket(sock, size):
    buffer = 1024
    bdata = bytearray()
    while len(bdata) < size:
#        print("len(bdata) = {}".format(len(bdata)))
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
        import mirror
        try:
            while True:
                # Récupération header
                # Il faut avertir le serveur de la quantité de donnée à récupérer
                header = clientsocket.recv(20)
                fps = unpack(">f", header[0:4])[0]
                width = unpack(">f", header[4:8])[0]
                height = unpack(">f", header[8:12])[0]
                size = unpack(">q", header[12:20])[0]

                try:
                    # Récupération de la frame + aussitôt rebond vers le poste de commandement
                    size = unpack(">q", header[12:20])[0]
                    print("size = {}".format(size))
                    frame = read_from_socket(clientsocket, size)
                    print("fps = {} width = {} height = {} size = {}".format(fps, width, height, size))
                    frame = numpy.ndarray(
                        (int(width), int(height), 3), dtype="uint8", buffer=frame
                    )
                    mirror.mirror(frame)

#                except ConnectionAbortedError:
#                    break

                except:
                    print("Erreur dans la récupération")
                    print("len(bdata) = {}".format(len(frame)))
                    break

            print("Client déconnecté...")

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
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
