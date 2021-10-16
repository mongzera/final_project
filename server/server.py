import socket
import threading
from common.packet import Packet

SERVER_CODE = "100000"
GLOBAL_CODE = "100001"

class Server():
    def __init__(self):
        self.HEADER_SIZE = 2048
        self.FORMAT = 'utf-8'

        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 5000 #preference since this socket is available

        self.ADDR = (self.HOST, self.PORT)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.connectedClients = [] #[client]
        self.activeChannel = [["SERVER", SERVER_CODE], ["GLOBAL", GLOBAL_CODE]] #['channelname', 'channelsocket']

        pass

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
            Packet.send(conn, 0, "WELCOME!!!", conn.getsockname())

            packet = Packet(conn)

            if packet.type == 5:#TYPE IS A CLIENT_REQUEST packet.types[5] = "client_request"
                if packet.recipient == SERVER_CODE:
                    request_code = helper.parse_client_request(packet)

                    packet = Packet(conn)#expecting the login packet

                   # datatype, sender, message, recipient = packet.getall()
                    print(packet.getall())

                    client = helper.handle_client_request(request_code, packet, (conn, addr))
                    client.set_server(self)
                    self.connectedClients.append(client)

                    
            if packet.type == 7: #TYPE IS A MESSAGE packet.types[7] = "message"
                if client is not None:
                    client.handle_client(packet)

    def search_user(self, sockname):
        for i in self.connectedClients:
            if sockname == i.addr:
                return i

        return None

    def updateActiveChannel(self, name, socketorcode, type):#UPDATE ACTIVE CHANNELS
        pass


server = Server()
import helper as helper
server.start()


