import socket
import threading
import os
import time

from common.packet import Packet

SERVER_CODE = "100000"
GLOBAL_CODE = "100001"
requests = ["LOGIN_REQUEST", "REGISTER_REQUEST"]
response = ["LOGIN_AUTHENTICATED", "REGISTRATION_AUTHENTICATED"]

class Client():
    def __init__(self):
        

        self.SERVER = "192.168.42.169"
        self.PORT = 5000

        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER_SIZE = 2048
        self.FORMAT = "utf-8"

        self.logged_in = False
        self.can_input_commands = False

        self.availableChannels = [["SERVER", SERVER_CODE], ["GLOBAL", GLOBAL_CODE]] #[channelname, channelsocket]

        
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            self.client.connect(self.ADDR)
            print(f"[CLIENT CONNECTED TO {self.SERVER}]")

            thread = threading.Thread(target=self.handle_server)
            thread.setName("Messaging App")
            thread.start()

            self.user_login()
            self.command_looper()
        except ConnectionError:
            print(f'[CONNECTION CANNOT BE ESTABLISHED]')
            
    def user_login(self):
        transaction_mode = input("Have you registered? (y/n):")

        if transaction_mode == "y":
            print("LOGIN:")
            username = input("USERNAME: ")
            password = input("PASSWORD: ")

            Packet.send(self.client, 5, requests[0], SERVER_CODE)
            Packet.send(self.client, 0, f"{username}&{password}", SERVER_CODE)
            return
        elif transaction_mode == "n":
            print("REGISTER:")
            username = input("USERNAME: ")
            password = input("PASSWORD: ")
            
            Packet.send(self.client, 5, requests[1], SERVER_CODE)
            Packet.send(self.client, 0, f"{username}&{password}", SERVER_CODE)
            return
        else: 
            print("YOUR INPUT IS INVALID...")
            print("Press any button and enter if you wish to restart...")
            c = input()

            if c:
                self.user_login()

            else:
                exit()


    def handle_server(self):
        connected = True

        while connected:
            packet = Packet(self.client)
            
            if self.logged_in == False:
                datatype, sender, message, recipient = packet.getall()

                if datatype == 4: #IF DATATYPE IS A SERVER_RESPONSE PACKET

                    if message == response[0]:
                        self.logged_in = True
                        print("[LOGIN SUCCESFUL...]")
                        print("[CLEARING]")
                        time.sleep(1) #WAIT 1 SECOND
                        os.system("cls") #CLEAR THE SCREEN
                        print('[THIS IS GLOBAL CHAT]')
                        print('[TYPE /c to change channel]')
                        print('[NOTE: ALL RECEIVED MESSESGES WILL BE CLEARED ONCE YOU LEAVE THE CHANNEL]')
                        print('[YOU MAY NOW TYPE...]')
                        self.can_input_commands = True
                        continue

            else: #IF LOGGED IN

                datatype, sender, message, recipient = packet.getall()

                if datatype == 7: #packet is a message packet.types[7] = "message"
                    
                    print(f'[{sender}]:{message}')
                
    
    def command_looper(self):
        while True:
            if self.can_input_commands:
                self.take_input()


            
    def take_input(self):
        inp = input()
        self.parse_input(inp)

    def parse_input(self, inp):
        if str(inp) == "/c":
            channel = input("[CHANNEL]: ")
            print(channel)
            return

        Packet.send(self.client, 7, str(inp), GLOBAL_CODE)
        pass

client = Client()
client.connect()
