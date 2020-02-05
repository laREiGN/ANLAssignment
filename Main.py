import socket
import sys
import json

ServerIP = "145.24.222.103"
Port = 8200

#Welcome message from server = welcome_msg
#Client 1 info message = c1message
#Client 1 reply message (sent by server) = c1reply

#Client 1 message to Client 2 = c1toc2_message
#Client 2 updated info message = c2message
#Client 2 reply message (sent by server) = c2reply

#Client 1 is the Client that contacts the server first. Client 1 listens for a welcome message. 
#If the message is received, client 1 sends a json file to the server containing needed info.
#The Server then responds with an updated json file, which then gets sent to Client 2
class Client1:
    def __init__(self):
        self.clientid = None
    def connect(self, clientid):
        #STEP 1: Connection to server
        self.clientid = clientid
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #AF_INET = ipv4 (internet protocol version, ip adress versie 4) 
        #SOCK_STREAM = connection via TCP Protocol
        s.connect((ServerIP, Port))
        #STEP 2: Welcome message from server
        welcome_msg_raw = s.recv(1024)
        #ontvangen in 1024 bytes
        welcome_msg = welcome_msg_raw.decode("utf-8")
        #vertalen naar utf-8 string (standaard formaat voor codering)
        print(welcome_msg)
        #Quick check on the welcome message received
        if "connection" in welcome_msg:
            #Client info message preparation
            c1message = {}
            c1message["studentnr"] = input("Please enter your student number: ")
            c1message["classname"] = "INF2C"
            c1message["clientid"] = self.clientid
            c1message["teamname"] = "Gerrie en Timmie"
            c1message["ip"] = socket.gethostbyname(socket.gethostname())
            c1message["secret"] = None
            c1message["status"] = None
            #STEP 3: Client info message sent to server
            c1message_serialized = json.dumps(c1message)
            #make a json from the object
            s.send(bytes(c1message_serialized, "utf-8"))
            #reduce back to bytes
            #STEP 4: Updated client info message received from server.
            c1replyserialized = s.recv(1024)
            c1reply = json.loads(c1replyserialized)
            #receive a json back from the server
            print("Current status: " + c1reply["status"])
            #print hidden status
        else: print("No message received from server.")
        s.close()
        #STEP 5.1: Message sent from Client 1 to Client 2
        if "waiting for message 2" in c1reply["status"]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c2host = input("Enter the host name of client 2: ")
            c2port = 8001
            s.connect((c2host,c2port))
            s.send(bytes(json.dumps(c1reply), "utf-8"))
        else: print("Incorrect message received")
        print("Client 1 shutting off")

#Client 2 first opens as a server. The client listens for connections. When a connection is made, the client waits for a message.
#When the message is received, the client shuts down the server (listener) and connects to the school server.
#Then client 2 updates the json received, and sends it back to the school server. Lastly, it listens for a response, and prints the STATUS.
class Client2:
    def listen(self, clientid):
        self.clientid = clientid
        host = '0.0.0.0'
        port = 8001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, port))
            #verbinding maken tussen host ip en port nr
            print("Host name:", socket.gethostbyname(socket.gethostname()))
            print("Use this when asked for a name by client 1.")
        except socket.error as e:
            print(str(e))
        s.listen(5)
        #luisterd naar conecties met als max 5 parralel
        conn, addr = s.accept()
        print('connected to: '+ addr[0]+':'+str(addr[1]))
        #STEP 5.2: Message received by Client 2
        self.c1toc2_message = conn.recv(1024).decode("utf-8")
        #recieve and decode json
        s.close()
        self.send()
        #ontvangen en decoden
    def send(self):
        #STEP 6: Connection made betweed Client 2 and Server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ServerIP, Port))
        #client opzetten
        #Client info message gets updated with Client 2 info.
        c1toc2_message_json = json.loads(self.c1toc2_message)
        #make json object
        c1toc2_message_json["studentnr"] = input("Please enter your student number: ")
        c1toc2_message_json["clientid"] = self.clientid
        c1toc2_message_json["ip"] = socket.gethostbyname(socket.gethostname())
        #STEP 7: Welcome message from server
        welcome_msg_raw = s.recv(1024)
        welcome_msg = welcome_msg_raw.decode("utf-8")
        print(welcome_msg)
        #Quick check on the welcome message received
        if "connection" in welcome_msg:
            #STEP 8: Updated Client info message (with secret and status) sent to server
            c2message = json.dumps(c1toc2_message_json)
            s.send(bytes(c2message, "utf-8"))
            #STEP 9: Final message received from server. Only the status gets printed.
            c2reply = s.recv(1024)
            c2replyserialized = json.loads(c2reply)
            print("Current status: " + c2replyserialized['status'])
        else: print("No message received from server.")
        print("Client 2 shutting off")
        



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
