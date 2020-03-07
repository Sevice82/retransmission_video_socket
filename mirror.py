#!/usr/bin/env python
# coding: utf-8

import socket
import threading

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1112))

# On acceuille le poste de commandement
class PC_Thread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip2, self.port2,))

    def run(self):
        print("Connexion de %s %s" % (self.ip2, self.port2,))

    def send(self, frame, header):
        clientsocket.PC_Thread.sendall(bytes(header))
        clientsocket.sendall(frame)
        
while True:
    tcpsock.listen(10)
    print("En écoute...")

    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = PC_Thread(ip, port, clientsocket)
    newthread.start()


def mirror(frame, header):
    newthread.send(frame, header)
