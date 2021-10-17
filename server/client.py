import json
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

        self.channels = []#CHANNELS ["NAME", CODE]

        Packet.send(self.conn, 4, helper.response[0], str(self.addr), server=self.serverObject)
        print("SENT AUTHENTICATION")


    def handle_client(self, packet):
        datatype, sender, message, recipient = packet.getall()

        if datatype == 7: #MESSAGE
            print("RECIPIENT:"+recipient)
            recipient = str(recipient)

            for i in self.serverObject.activeChannel:
                if int(recipient) == i[1]:
                    print("GROUP MESSG")
                    self.message_group(recipient, sender, message)
                    return

            if recipient == GLOBAL_CODE: #RECIPIENT IS GLOBAL
                print("GLOBAL MSSG")
                self.message_all(datatype, sender, message)
                return

            

            if "(" in recipient and ")" in recipient:
                # recipient = recipient.replace("(", "")
                # recipient = recipient.replace(")", "")
                # recipient = recipient.replace('"', "")
                # recipient = recipient.replace("'", "")
                # recipient = recipient.replace(" ", "")
                # recipient = recipient.split(",")
                
                for i in self.serverObject.connectedClients:
                    if recipient == str(i.addr):
                        print("PRVT MESSG")
                        self.messege(i.conn, datatype, sender, message, recipient)
                        return

        

    def messege(self,conn, datatype, sender, message, recipient):
        Packet.sendToClient(conn, datatype, self.username, message, recipient, server=self.serverObject)
        

    def message_all(self, datatype, sender, message):
        for i in self.serverObject.connectedClients:
            print("ME:", i.addr == self.addr)
            if str(i.addr) == str(self.addr):
                continue
            
            Packet.sendToClient(i.conn, datatype, self.username, message, i.username, server=self.serverObject)

    def message_group(self, group, sender, message):
        print("FINDING GROUPMATES")
        for i in self.serverObject.connectedClients:
            print("FOUNG GROUPMATE")
            for j in i.channels:
                print("CHECKING GROUPMATE")
                print(str(group), str(j[1]))
                if str(group) == str(j[1]):
                    print("SENDING TO" + i.username)
                    Packet.sendToClient(i.conn, 7, sender, message, i.username)
                    

    def set_server(self, server):
        self.serverObject = server
        self.server = server.server

    def wrong_username_and_password(conn):
        Packet.send(conn, 4, helper.response[3], conn.getsockname())
        return -1

    def already_logged_in(conn):
        Packet.send(conn, 4, helper.response[5], conn.getsockname())
        return -1



