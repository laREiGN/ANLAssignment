import socket
import sys
import json

ServerIP = "145.24.222.103"
Port = 8001

#Client 1 is the Client that contacts the server first. Client 1 listens for a welcome message. 
#If the message is received, client 1 sends a json file to the server containing needed info.
#The Server then responds with an updated json file, which then gets sent to Client 2

#Welcome message from server = welcome_msg
#Client 1 info message = c1message
#Client 1 reply message (sent by server) = c1reply

#Client 1 message to Client 2 = c1toc2_message
#Client 2 updated info message = c2message
#Client 2 reply message (sent by server) = c2reply

class Client1:
    def __init__(self):
        self.clientid = None
    def connect(self, clientid):
        self.clientid = clientid
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        welcome_msg_raw = s.recv(1024)
        welcome_msg = welcome_msg_raw.decode("utf-8")
        print(welcome_msg)
        if "connection" in welcome_msg:
            c1message = {}
            c1message["studentnr"] = input("Please enter your student number: ")
            c1message["classname"] = "INF2C"
            c1message["clientid"] = self.clientid
            c1message["teamname"] = "Gerrie en Timmie"
            c1message["ip"] = socket.gethostbyname(socket.gethostname())
            c1message["secret"] = None
            c1message["status"] = None
            c1message_serialized = json.dumps(c1message)
            s.send(bytes(c1message_serialized, "utf-8"))
            c1replyserialized = s.recv(1024)
            c1reply = json.loads(c1replyserialized)
            print(c1reply["status"])
        else: print("No message received from server.")
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2host = input("Enter the host name of client 2: ")
        c2port = 5000
        s.connect((c2host,c2port))
        s.send(bytes(json.dumps(c1reply), "utf-8"))

#Client 2 first opens as a server. The client listens for connections. When a connection is made, the client waits for a message.
#When the message is received, the client shuts down the server (listener) and connects to the school server.
#Then client 2 updates the json received, and sends it back to the school server. Lastly, it listens for a response, and prints the STATUS.
class Client2:
    def listen(self, clientid):
        self.clientid = clientid
        host = '0.0.0.0'
        port = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
            print("Host name:", socket.gethostname())
            print("Use this when asked for a name by client 1.")
        except socket.error as e:
            print(str(e))
        s.listen(5)
        conn, addr = s.accept()
        print('connected to: '+ addr[0]+':'+str(addr[1]))
        self.c1toc2_message = conn.recv(1024).decode("utf-8")
        s.close()
        self.send()
    def send(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        c1toc2_message_json = json.loads(self.c1toc2_message)
        c1toc2_message_json["studentnr"] = input("Please enter your student number: ")
        c1toc2_message_json["clientid"] = self.clientid
        c1toc2_message_json["ip"] = socket.gethostbyname(socket.gethostname())
        welcome_msg_raw = s.recv(1024)
        welcome_msg = welcome_msg_raw.decode("utf-8")
        print(welcome_msg)
        if "connection" in welcome_msg:
            c2message = json.dumps(c1toc2_message_json)
            s.send(bytes(c2message, "utf-8"))
            c2reply = s.recv(1024)
            c2replyserialized = json.loads(c2reply)
            print(c2replyserialized['status'])
        else: print("No message received from server.")
        



c1 = Client1()
c2 = Client2()


def Main():
    clientprompt = input("Which client do you want to use? Please only use 1 or 2: ")
    if clientprompt == "1":
        clientid = 1
        c1.connect(clientid)
    elif clientprompt == "2":
        clientid = 2
        c2.listen(clientid)
    else:
        print("Wrong client ID. Please try again.")
        Main()

Main()
