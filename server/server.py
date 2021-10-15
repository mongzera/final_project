import socket
import threading
import helper
 
from common.packet import Packet

from client import Client


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
            Packet.send(conn, 0, "WELCOME!!!")

            packet = Packet(conn)

            if int(packet.type) == 4:
                
                request_code = helper.parse_client_request(packet)
                client = helper.handle_client_request(request_code, packet, (conn, addr, client), self.connectedClients) # NOT WORKING PLEASE FIX
                #print(client.handle_client(packet))
                    
            if packet.type == packet.types[5]:
                if client is not None:
                    client.handle_client(packet)

server = Server()

server.start()
