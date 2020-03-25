#!/usr/bin/env python
# coding: utf-8

import socket
import threading

tcpsock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock_2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock_2.bind(("", 1112))

# On acceuille le poste de commandement
class PC_Thread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port,))

    def send(self, frame, header):
        clientsocket.PC_Thread.sendall(bytes(header))
        clientsocket.sendall(frame)
        
while True:
    tcpsock_2.listen(10)
    print("Mirror en écoute...")

    (clientsocket_2, (ip_2, port_2)) = tcpsock_2.accept()
    newthread = PC_Thread(ip_2, port_2, clientsocket_2)
    newthread.start()


def mirror(frame_2, header_2):
    newthread.send(frame_2, header_2)
