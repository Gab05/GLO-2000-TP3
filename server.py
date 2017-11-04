import socket, optparse, sys
from socketUtil import recv_msg, send_msg
from datetime import datetime
from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire


#choisissez l’adresse avec l’option -a et le port avec -p
parser = optparse.OptionParser()
parser.add_option("-s", "--server", action="store_true", dest="serveur", default=False)
parser.add_option("-d", "--destination", action="store", dest="dest", default=False)
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=False)
opts = parser.parse_args(sys.argv[1:])[0]
if opts.serveur and not opts.port:
    print("Erreur : L’option -p est obligatoire")
    file = open("Error.log", "a")
    file.write(str(datetime.now()) + " -> " + "Erreur : L’option -p est obligatoire" + "\n")
    file.close()
elif opts.serveur and opts.dest:
    print("Erreur : L’application ne peut pas utiliser -d et -s simultanément")
    file = open("Error.log", "a")
    file.write(str(datetime.now()) + " -> " + "Erreur : L’application ne peut pas utiliser -d et -s simultanément" + "\n")
    file.close()
else:
    if opts.serveur and opts.port: #mode serveur
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("localhost", opts.port))
        serversocket.listen(5)
        print("Listening on port " + str(serversocket.getsockname()[1]))
        i = 0
        while True:
            (s, address) = serversocket.accept()
            i += 1
            print(str(i) + "e connexion au serveur")

            print("----------")
            m = trouverNombrePremier()
            n = entierAleatoire(m)
            print("Envoi du modulo: " + str(m))
            print("Envoi de la base: " + str(n))
            print("----------")
            send_msg(s, str(m))
            send_msg(s, str(n))

            serSecretKey = entierAleatoire(m)
            serPublicKey = exponentiationModulaire(n, serSecretKey, m)
            print("Cle privée: " + str(serSecretKey))
            print("Cle publique a envoyer: " + str(serPublicKey))
            send_msg(s, str(serPublicKey))
            pubKeyCli = int(recv_msg(s))
            print("Cle publique recu: " + str(pubKeyCli))
            servSharedKey = exponentiationModulaire(pubKeyCli, serSecretKey, m)
            print("Cle partagee: " + str(servSharedKey))
            print("----------")
            s.close()

    else: #mode client
        destination = (opts.dest, opts.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(destination)

        mod = int(recv_msg(s)) #Reception mod
        base = int(recv_msg(s)) #Reception base
        print("Reception du modulo: " + str(mod))
        print("Reception de la base: " + str(base))
        print("----------")
        cliSecretKey = entierAleatoire(mod)
        cliPublicKey = exponentiationModulaire(base, cliSecretKey, mod)
        print("Cle privee: " + str(cliSecretKey))
        print("Cle publique a envoyer: " + str(cliPublicKey))
        pubKeyServ = int(recv_msg(s))
        print("Cle publique recu: " + str(pubKeyServ))
        send_msg(s, str(cliPublicKey))
        cliSharedKey = exponentiationModulaire(pubKeyServ, cliSecretKey, mod)
        print("Cle partagee: " + str(cliSharedKey))
        print("----------")

        s.close()

