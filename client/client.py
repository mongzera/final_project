import socket
import threading

from common.packet import Packet

class Client():
    def __init__(self):
        self.requests = [0, 1]

        self.SERVER = "192.168.42.169"
        self.PORT = 5000

        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER_SIZE = 2048
        self.FORMAT = "utf-8"

        self.logged_in = False
        
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            self.client.connect(self.ADDR)
            print(f"[CLIENT CONNECTED TO {self.SERVER}]")

            thread = threading.Thread(target=self.handle_server)
            thread.setName("Messaging App")
            thread.start()

            self.user_login()
        except ConnectionError:
            print(f'[CONNECTION CANNOT BE ESTABLISHED]')
            
    def user_login(self):
        transaction_mode = input("Have you registered? (y/n):")

        if transaction_mode == "y":
            print("LOGIN:")
            username = input("USERNAME: ")
            password = input("PASSWORD: ")

            Packet.send(self.client, 4, self.requests[0])
            Packet.send(self.client, 0, f"{username}&{password}")
            return
        elif transaction_mode == "n":
            print("REGISTER:")
            username = input("USERNAME: ")
            password = input("PASSWORD: ")
            
            Packet.send(self.client, 4, self.requests[1])
            Packet.send(self.client, 0, f"{username}&{password}")
            return
        else: 
            print("YOUR INPUT IS INVALID...")
            print("Press any button and enter if you wish to restart...")
            c = input()

            if c:
                self.user_login(self.client)

            else:
                exit()


    def handle_server(self):
        connected = True

        while connected:
            packet = Packet(self.client)
            
            print(packet.message)
        


client = Client()
client.connect()
