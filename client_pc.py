#!/usr/bin/env python
# coding: utf-8

import socket

hote = "localhost"
port = 1111

while 1:
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))
    print("Début de la récéption vidéo")

    while 1:
        try:
            msg_recu = connexion.recv(128)
            print(msg_recu.decode())
        except Exception as e:
            print("connexion avec le serveur perdue")
            break

    print("Fermeture de la connexion")
    connexion.close()