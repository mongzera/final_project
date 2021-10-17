
import socket
import threading

SERVER_CODE = "100000"
GLOBAL_CODE = "100001"

class Server():
    def __init__(self):
        #connect to sqlite

        self.HEADER_SIZE = 2048
        self.FORMAT = 'utf-8'

        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5000 #preference since this socket is available

        self.ADDR = (self.HOST, self.PORT)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.connectedClients = [] #[client]
        self.activeChannel = [["SERVER", SERVER_CODE], ["GLOBAL", GLOBAL_CODE], ["JAJA", 100010]] #['channelname', 'channelsocket']
        

    def start(self):
        self.server.listen()
        print(f"[SERVER LISTENING AT {self.ADDR}]")

        while True: #listen for connecting clients
            conn, addr = self.server.accept()
            print(f'[A USER CONNECTED {addr}]')
            user_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            user_thread.setName(addr)
            user_thread.start()

    def handle_client(self, conn, addr):
        connected = True

        client = None 

        while connected:
            server.response_to_all(4, server.get_connected_clients_addr(), helper.response[2])
            self.response_to_all(4, self.get_active_channels(), helper.response[8])

            packet = Packet(conn)

            #print("PACKET:",packet.getall())



            if packet.type == 5:#TYPE IS A CLIENT_REQUEST packet.types[5] = "client_request"
                if packet.recipient == SERVER_CODE:
                    request_code = helper.parse_client_request(packet)

                    packet = Packet(conn)#expecting the login packet
                    #print("PACKET_2:",packet.getall())
                   # datatype, sender, message, recipient = packet.getall()
                    #print(packet.getall())

                    status_code = helper.handle_client_request(request_code, packet, (conn, addr), self)

                    if status_code == -1 or status_code == 0:
                        continue

                    client = status_code

              
            if packet.type == 7: #TYPE IS A MESSAGE packet.types[7] = "message"
                #print("handle")
                if client is not None:
                    
                    client.handle_client(packet)

        exit()

    def search_user(self, sockname):
        for i in self.connectedClients:
            if sockname == i.addr:
                return i

        return None

    def updateActiveChannel(self, name, socketorcode):#UPDATE ACTIVE CHANNELS
        self.activeChannel.append([name, socketorcode])
        self.response_to_all(4, self.get_active_channels(), helper.response[8])
        pass

    def get_connected_clients_addr(self):
        clients = ""

        for i in self.connectedClients:
            clients += f"{i.username}:{i.addr}/"

        clients = clients.removesuffix("/")
        return clients

    def get_active_channels(self):
        channels = ""
        for i in self.activeChannel:
            channels += f"{i[0]}:{i[1]}/"

        channels = channels.removesuffix("/")
        return channels

    def response_to_all(self, datatype, message, response):
        for i in self.connectedClients:
            print(message)
            Packet.send(i.conn, datatype, response, i.addr, server=self)
            Packet.send(i.conn, datatype, message, i.addr, server=self)



server = Server()
from common.packet import Packet
import helper as helper
server.start()


