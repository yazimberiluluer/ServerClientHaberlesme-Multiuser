#MULTICLINET HABERLESME
from socket import AF_INET , socket, SOCK_STREAM
#AF_INET yereş int adresini bulmak icin
from threading import Thread

"""birden fazla client olduguicin bunların isimlerini ve ıp adreslerini
tutacagımız listeler """
clients = {}
adresses = {}

HOST = '127.0.0.1'
"""host -> localhost, IP adresi ya da dinamik dns serverı (dyndns) olabilir"""
PORT = 23456
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET,SOCK_STREAM)
"""Server INET e baglanacakve stream yapacak yani kendi ıp si olacak ve stream i porttan yapacak"""
SERVER.bind(ADDR)

def gelen_mesaj():
    "gelen mesajlarin kotnrolunu saglayan fonksiyon"
    #daima gelen mesajı kabul edecek
    while True:
        client, client_adress = SERVER.accept() #gelen clienti ve adresini servera kabul et
        print("%s:%s baglandı" %client_adress) #hangi clientin baglandigini gormek icin addr3esini yani
        #host ve portunu print ediyorum
        client.send(bytes("Chat Application \n" +
                          "Please enter your name: ", "utf8")) #gelen clienta gonderılen mesaj
        adresses[client] = client_adress #gelen clientın adresini adres listeisne ekledik
        Thread(target= baglan_client, args= (client,)).start()
        """clientlar, baglan_client() fonksiyonundan
        gelecek bu nedenle targetimiz bu fonk, her bir client bir arg dır ve bu liste uzayabilir
        o nedenle virgul koyup bıraktık. Yani eş zamanlı olarak farklı clientları al baglan_client fınk.nuna client gelcikce
        """


def baglan_client(client):
        "Client baglantisinin gerceklestigi yer"
        isim = client.recv(BUFFERSIZE).decode("utf8")
        hosgeldin = "Hosgeldin %s! Cikmak icin {cikis} yaziniz!" %isim
        client.send(bytes(hosgeldin, "utf8"))
        msg = "%s connected to Chat Application" %isim
        """bir client katildiginda diger clientlara gidecek mesaj"""
        yayin(bytes(msg, "utf8"))
        """bu fonksiyon gelen giden her turlu mesajin yayinlanmasını saglar"""
        clients[client] = isim #gelen clientın ismini clients listeisne ekledik
        while True:
            msg = client.recv(BUFFERSIZE)
            if msg != bytes("{cikis}", "utf8"):
                yayin(msg, isim + ": ")
            else:
                client.send(bytes("{cikis}", "utf8"))
                del clients[client]
                yayin(bytes("%s quit the chat application" %isim, "utf8"))
                """client {cikis} yazarsa clients listes,nden onu siliyoruz ve 
                diger clientlara bu clientin ciktigini haber veriyoruz"""
                break

def yayin(msg, kisi=""):
    for yayim in clients:
        yayim.send(bytes(kisi, "utf8")+ msg)


if __name__ == "__main__":
    SERVER.listen(10) #max 10 client baglanabilir
    print("Baglanti bekleniyor...")
    ACCEPT_Thread = Thread(target=gelen_mesaj)
    ACCEPT_Thread.start()
    ACCEPT_Thread.join()
    SERVER.close()
