
from common.packet import Packet
import helper as helper

SERVER_CODE = "100000"
GLOBAL_CODE = "100001"

class Client():
    def __init__(self, conn, username, password):
        self.serverObject = None
        self.server = None
        self.username = username
        self.password = password


        self.conn = conn[0]
        self.addr = conn[1]

        Packet.send(self.conn, 4, helper.response[0], str(self.addr))
        print("SENT AUTHENTICATION")


        pass

    def handle_client(self, packet):
        datatype, sender, message, recipient = packet.getall()

        if datatype == 7: #MESSAGE
            if recipient == GLOBAL_CODE: #RECIPIENT IS GLOBAL
                print("messgrecved")
                self.message_all(datatype, sender, message)
        

    def messege(self, datatype, sender, message, recipient):
        recver = self.serverObject.search_user(recipient)

        Packet.sendToClient(recver.conn, datatype, self.username, message, recver.username)
        

    def message_all(self, datatype, sender, message):
        for i in self.serverObject.connectedClients:
            print("ME:", i.addr == self.addr)
            if str(i.addr) == str(self.addr):
                continue
            
            Packet.sendToClient(i.conn, datatype, self.username, message, i.username)

    def set_server(self, server):
        self.serverObject = server
        self.server = server.server

        self.serverObject.updateActiveChannel(self.username, self.addr, 1)



