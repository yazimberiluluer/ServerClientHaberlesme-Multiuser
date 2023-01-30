#Client Baglantisi

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def gelen_mesaj():
    while True:
        try:
            msg = client_socket.recv(BUFFERSIZE).decode("utf8")
            mesaj_listesi.insert(tkinter.END, msg)
        except:
            break

def gonder(event=None):
    msg = mesajim.get() #mesaji al
    mesajim.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{cikis}":
        client_socket.close()
        app.quit()


def cikis_durumu(event=None):
    mesajim.set("{cikis}")
    gonder()


# App Interface
app = tkinter.Tk()
app.title("Chat Application")

mesaj_alani = tkinter.Frame(app)
mesajim = tkinter.StringVar()
mesajim.set("Please enter your message...")
scrollbar = tkinter.Scrollbar(mesaj_alani)
mesaj_listesi= tkinter.Listbox(mesaj_alani, height=20, width=70, yscrollcommand=scrollbar.set)
mesaj_listesi.see("end")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
mesaj_listesi.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
mesaj_alani.pack()
giris_alani= tkinter.Entry(app, textvariable=mesajim)
giris_alani.bind("<Return>", gonder)
giris_alani.pack()
gonder_buton = tkinter.Button(app, text="Send", command=gonder)
gonder_buton.pack()

app.protocol("VM_DELETE_WINDOW", cikis_durumu)

HOST = '127.0.0.1'
PORT = 23456
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if not PORT:
    PORT =23456
else:
    PORT=int(PORT)

gelen_thread = Thread(target=gelen_mesaj)
gelen_thread.start()
tkinter.mainloop()