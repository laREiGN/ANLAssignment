import socket
import sys
import json

ServerIP = "145.24.222.103"
Port = 8001

class Client1:
    def __init__(self):
        self.clientid = None
    def connect(self, clientid):
        self.clientid = clientid
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        msgraw = s.recv(1024)
        msg = msgraw.decode("utf-8")
        print(msg)
        if "connection" in msg:
            reply = {}
            reply["studentnr"] = "123456"
            reply["classname"] = "INF2C"
            reply["clientid"] = self.clientid
            reply["teamname"] = "Gerrie en Timmie"
            reply["ip"] = socket.gethostbyname(socket.gethostname())
            reply["secret"] = None
            reply["status"] = None
            replyserialized = json.dumps(reply)
            s.send(bytes(replyserialized, "utf-8"))
            reply2 = s.recv(1024)
            reply2serialized = json.loads(reply2)
            print(reply2serialized)
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2host = input("Enter the IP of client 2:   ")
        c2port = int(input("Enther the port of clinet 2:   "))
        s.connect((c2host,c2port))

class Client2:
    def listen(self):
        host = '0.0.0.0'
        port = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
            print(socket.gethostname(),",", port)
        except socket.error as e:
            print(str(e))
        s.listen(5)
        conn, addr = s.accept()
        print('connected to: '+ addr[0]+':'+str(addr[1]))

c1 = Client1()
c2 = Client2()


def Main():
    clientprompt = input("Which client do you want to use? Please only use 1 or 2.    :   ")
    if clientprompt == "1":
        clientid = 1
        c1.connect(clientid)
    elif clientprompt == "2":
        clientid = 2
        c2.listen()
    else:
        print("Wrong client ID. Please try again.")
        Main()

Main()
