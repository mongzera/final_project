from helper import response

class Packet():

    #packet format
    # DATATYPE_SENDER_RECIPIENT:MESSAGE
    # 0_SERVER_12550:AUTHENTICATED_LOGIN_REQUEST

    def __init__(self, conn):

        self.types = ("string", "int", "float", "server_request", "server_response", "client_request", "client_response", "message")

        self.type = None
        self.sender = None
        self.message = None
        self.recipient = None

        self.packet_decoded = None

        self.parsed_packet = None

        try:
            header_size = conn.recv(Packet.HEADER_SIZE()).decode(Packet.FORMAT())

            if header_size:
                #header_size = 16bytes


                #first_message"14              " 16bytes

                #second_message "hello im alvin" 14 * 1byte = 14bytes


                header_size = int(header_size)

                packet = conn.recv(header_size).decode(Packet.FORMAT())

                self.parsed_packet = self.parse(packet)

                self.type, self.sender, self.message, self.recipient = self.parsed_packet

        except ConnectionResetError:
            pass

    def parse(self, packet):
        packet = str(packet)

        sender = ""

        datatype = int(packet[0])


        sender_ok = False

        recipient = ""

        recipient_ok = False

        message = ""


        for i in range(len(packet)):
            if i > 0 and sender_ok == False:

                if len(sender) > 1:
                    if packet[i] == "_":
                        sender_ok = True
                        continue

                if packet[i] != "_":
                    sender += packet[i]
                    continue


            if sender_ok:
                if recipient_ok == False:
                    if packet[i] == ":":
                        recipient_ok = True
                        continue
                    recipient += packet[i]
                    continue

                message += packet[i]
                
        #print(datatype, sender, message, recipient) 
        return (datatype, sender, message, recipient) #(int, string, string)

    def getall(self):
        return (self.type, self.sender, self.message, self.recipient)

    def HEADER_SIZE():
        return int(2048)

    def FORMAT():
        return str('utf-8')

    def send(conn, datatype, message, recipient, server = None):

        sender = conn.getsockname()

        recipient = str(recipient)
        
        raw_msg = f"{str(datatype)}_{str(sender)}_{recipient}:{str(message)}".encode(Packet.FORMAT())
        
        size = str(len(raw_msg)).encode(Packet.FORMAT())
        size += b' ' * (Packet.HEADER_SIZE() - len(size))

        try:
            conn.send(size)
            conn.send(raw_msg)
        except ConnectionResetError:
            if server != None:
                
                for i in server.connectedClients:
                    if conn == i.conn:
                        server.connectedClients.remove(i)
                        server.response_to_all(4, server.get_connected_clients_addr(), response[2])
                        print("REMOVE")
                        return -1
            

    def sendToClient(conn, datatype, sender, message, recipient, server = None):

        recipient = str(recipient)
        
        raw_msg = f"{str(datatype)}_{str(sender)}_{recipient}:{str(message)}".encode(Packet.FORMAT())
        
        size = str(len(raw_msg)).encode(Packet.FORMAT())
        size += b' ' * (Packet.HEADER_SIZE() - len(size))

        try:
            conn.send(size)
            conn.send(raw_msg)
        except ConnectionResetError:
            #close connection
            if server != None:
                
                for i in server.connectedClients:
                    if conn == i.conn:
                        server.connectedClients.remove(i)
                        server.response_to_all(4, server.get_connected_clients_addr(), response[2])
                        print("REMOVE")
                        return -1
            
            


                