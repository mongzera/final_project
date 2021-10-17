import os
import sys
import socket
import threading
import time

from colorama import Fore
from colorama import Style

from common.packet import Packet

SERVER_CODE = "100000"
GLOBAL_CODE = "100001"
requests = ["LOGIN_REQUEST", "REGISTER_REQUEST", "CREATE_GROUP_REQUEST", "GROUP_JOIN_REQUEST"]
response = ["LOGIN_AUTHENTICATED", "REGISTRATION_AUTHENTICATED", "CLIENT_CHANNEL_UPDATE", "LOGIN_FAILED", "ACCOUNT_ALREADY_EXISTED", "USER_ALREADY_LOGGED_IN", "CHANNEL_EXISTS", "GROUP_JOINED_SUCCESFULLY", "GROUP_CHANNEL_UPDATE", "CHANNEL_CREATED_SUCCESSFULLY"]

green = "color 0a"
red = "color 0a"
yellow = "color 06"
light_blue = "color 09"
purple = "color 05"
white = "color 07"

class Client():
    def __init__(self):
        

        self.SERVER = "192.168.42.169"
        self.PORT = 5000

        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER_SIZE = 2048
        self.FORMAT = "utf-8"

        self.logged_in = False
        self.can_input_commands = False
        self.idle = False
        self.idlePacket = None

        self.username = ""

        self.defaultChannels = [("GLOBAL", GLOBAL_CODE)] #[channelname, channelsocket]
        self.availableChannels = [("GLOBAL", GLOBAL_CODE)] #[channelname, channelsocket]
        self.availableGroupChannels = [] #[channelname, channelsocket]

        self.recipientCode = None

        
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            self.client.connect(self.ADDR)
            print(f"[CLIENT CONNECTED TO {self.SERVER}]")
            os.system("cls")
            thread = threading.Thread(target=self.handle_server)
            thread.setName("Messaging App")
            thread.start()

            self.user_login()
            self.command_looper()
        except ConnectionError:
            
            print(f'{Fore.RED}[CONNECTION CANNOT BE ESTABLISHED]{Style.RESET_ALL}')
            
    def user_login(self, just_registered = False, retry=False):
        if just_registered == True and retry == False:
            transaction_mode = "y"
        elif just_registered == False and retry == True:
            transaction_mode = "n"
        else:
            transaction_mode = input("[HAVE YOU REGISTERED?] (y/n):")

        if transaction_mode == "y":
            print("LOGIN:")
            username = input("USERNAME: ")
            password = input("PASSWORD: ")

            self.username = username

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
            print("[YOUR INPUT IS INVALID...]")
            print("[PRESS ENTER IF YOU WISH TO RESTART...]")
            c = input()

            if c:
                self.user_login()

            else:
                exit()

        


    def handle_server(self):
        connected = True

        while connected:
            
            if self.idle:
                continue

            if self.idlePacket != None:
                packet = self.idlePacket
                self.idlePacket = None
            else:
                packet = Packet(self.client)

            if self.idle:
                self.idlePacket = packet
                continue

            #print(packet.getall()[0], self.logged_in, packet.getall()[2])
            
            if self.logged_in == False:
                datatype, sender, message, recipient = packet.getall()
                
                if datatype == 4: #IF DATATYPE IS A SERVER_RESPONSE PACKET
                    
                    if message == response[0]:
                        self.logged_in = True
                        self.recipientCode = self.availableChannels[0]
                        print("[LOGIN SUCCESFUL...]")
                        print("[CLEARING]")
                        time.sleep(1) #WAIT 1 SECOND
                        os.system("cls") #CLEAR THE SCREEN
                        self.help()
                        
                        self.can_input_commands = True
                        continue

                    if message == response[1]:
                        print("[REGISTRATION SUCCESFUL...]")
                        print("[CLEARING]")
                        time.sleep(1) #WAIT 1 SECOND
                        os.system("cls") #CLEAR THE SCREEN
                        to_login = input('[WOULD YOU LIKE TO LOGIN?] (y/n)')
                        
                        if to_login == "y":
                            self.user_login(just_registered=True)
                            continue
                        else:
                            print('[GOODBYE!]')
                            print("[EXITING]")
                            time.sleep(1.5)
                            connected = False
                            exit()

                    if message == response[3]:
                        print(Fore.RED)
                        print("[WRONG USERNAME OR PASSWORD...]")
                        print("[CLEARING]")
                        print(Style.RESET_ALL)
                        time.sleep(1)
                        os.system("cls")
                        self.user_login(just_registered=True)
                        continue

                    if message == response[4]: #ACCOUNT ALREADY EXISTED
                        print(Fore.RED)
                        print("[USERNAME ALREADY EXISTS...]")
                        try_again = input("[WANT TO TRY AGAIN?] (y/n):")
                        if try_again == "y":
                            self.user_login(retry=True)
                            print(Style.RESET_ALL)
                            continue
                        else:
                            connected = False
                            return

                    if message == response[5]:
                        print(Fore.RED)
                        print('[THIS ACCOUNT HAS LOGGED IN]')
                        print('[ONLY ONE INSTANCE IS ALLOWED...]')
                        x = input("[PRESS ENTER TO EXIT...]")
                        connected = False
                        return

            else: #IF LOGGED IN

                datatype, sender, message, recipient = packet.getall()

                if datatype == 7: #packet is a message packet.types[7] = "message"
                    
                    print(f'{Fore.RED}[{sender}]{Style.RESET_ALL}:{Fore.CYAN}{message}{Style.RESET_ALL}')
                    

                if datatype == 4: #packet is a server response 

                    if message == response[2]: #if client_channel_update

                        msg = Packet(self.client)

                        datatype, sender, message, recipient = msg.getall()

                        self.client_conn_update(message)
                        continue
                    if message == response[9]:
                        packet = Packet(self.client)

                        datatype, sender, message, recipient = packet.getall()\

                        channel = str(message).split("&")

                        self.availableChannels.append(channel)
                        print(f"{Fore.GREEN}[GROUP CREATED SUCCESFULLY]{Style.RESET_ALL}")
                        print(f"[CONNECTED TO GROUP]:{message}")
                        continue

                    if message == response[7]:
                        packet = Packet(self.client)

                        datatype, sender, message, recipient = packet.getall()

                        if message == response[7]:
                            print("[GROUP JOINED SUCCESFULLY]")
                            print('[YOU CAN NOW CHANGE THE CHANNEL WITH THE GROUP NAME]')

                    if message == response[8]:
                        msg = Packet(self.client)

                        datatype, sender, message, recipient = msg.getall()

                        self.active_channel_update(message)
                        continue

                
    
    def command_looper(self):
        while True:
            if self.can_input_commands:
                self.take_input()


            
    def take_input(self):
        print(f'{Fore.BLUE}[YOU ARE CHATTING {self.recipientCode[0]}]{Style.RESET_ALL}')

        outpt = input("")
        #sys.stdout.write("\033[F") #back to previous line 
        #sys.stdout.write("\033[K") #clear line 
        
        print(Style.RESET_ALL)
        self.parse_input(outpt)

    def parse_input(self, inp):
        if str(inp).startswith("/c"): #CHECK CHANNELS
            self.idle = True
            print(f"{Fore.GREEN}[AVAILABLE CHANNELS]")

            for i in self.availableChannels:
                print(f"{i[0]}")
            for i in self.availableGroupChannels:
                print(f"{i[0]}")
            print("_____________________")
            channel = input("[TYPE NAME]: ")

            for i in self.availableChannels:
                if i[0] == str(channel):
                    self.recipientCode = i
                    break

            for i in self.availableGroupChannels:
                if i[0] == str(channel):
                    self.recipientCode = i
                    break
            self.idle = False

            print(f"[CHANGING >>> {channel}]{Style.RESET_ALL}")
            time.sleep(1)
            os.system("cls")
            
            return

        elif str(inp).startswith("/g"): #CREATE A CHANNEL
            group_name = str(inp).removeprefix("/g").replace(" ", "")
            if len(group_name) == 0:
                print("[NAME IS EMPTY]")
                print("Syntax: /g (name)")
                return
            print(f"[CREATING GROUP]: {group_name}")
            Packet.send(self.client, 5, requests[2], SERVER_CODE)
            Packet.send(self.client, 5, group_name, SERVER_CODE)
            return

        elif str(inp).startswith("/j"): #JOIN CHANNEL
            group_name = str(inp).removeprefix("/j").replace(" ", "")
            if len(group_name) == 0:
                print("[NAME IS EMPTY]")
                print("Syntax: /j (name)")
                return
            print(f"[JOINING GROUP]: {group_name}")
            Packet.send(self.client, 5, requests[3], SERVER_CODE)
            Packet.send(self.client, 5, group_name, SERVER_CODE)

        elif str(inp).startswith("/h"): #HELP
            self.help()
            return
        else:
            print(f'{Fore.LIGHTGREEN_EX}[YOU]:{Fore.YELLOW} {inp}{Style.RESET_ALL}')

            Packet.send(self.client, 7, str(inp), self.recipientCode[1])

    def help(self):
        print(Fore.LIGHTCYAN_EX)
        print('[THIS IS GLOBAL CHAT]')
        print('[TYPE /h for help]')
        print('[TYPE /c to change channel]')
        print('[TYPE /g (name) to make a channel]')
        print('[TYPE /j (name) to join a channel]')
        print('[NOTE: ALL RECEIVED MESSESGES WILL BE CLEARED ONCE YOU LEAVE THE CHANNEL]')
        print('[YOU MAY NOW TYPE...]')
        print(Style.RESET_ALL)
    
    def client_conn_update(self, message):
        clients = str(message).split("/")
        self.availableChannels = list(self.defaultChannels)
        for client in clients:
            name_addr = client.split(":")
            if name_addr[0] == self.username:
                continue

            self.availableChannels.append((name_addr[0], name_addr[1]))

    def active_channel_update(self, message):
        groups = str(message).split("/")

        updated_groups = []
        for client in groups:
            name_addr = client.split(":")
            if name_addr[0] == self.username:
                continue

            updated_groups.append((name_addr[0], name_addr[1]))

        self.availableGroupChannels = list(updated_groups)


client = Client()
client.connect()
