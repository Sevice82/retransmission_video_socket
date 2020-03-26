#!/usr/bin/env python
# coding: utf-8

import socket

hote = "localhost"
port = 1111
discours = "le test est concluant"
msg_a_envoyer = discours.encode()

while 1:
    connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_serveur.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))

    size = len(discours)
    msg_a_envoyer = b"1;{}".format(size)
    msg_a_envoyer = msg_a_envoyer.encode()
    discours = discours.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_recu = connexion_avec_serveur.recv(10)
    if str(msg_recu.decode()) == "ok":
        print("Début de la transmission vidéo")
        while 1:
            try:
                connexion_avec_serveur.send(discours)
            except Exception as e:
                print("connexion avec le serveur perdue")
                break

    print("Fermeture de la connexion")
    connexion_avec_serveur.close()