class Packet():

    #packet format
    # DATATYPE_SENDER_MESSAGE
    # 0_SERVER_AUTHENTICATED_LOGIN_REQUEST

    def __init__(self, conn):

        self.types = ("string", "int", "float", "server_request", "client_request", "message")

        self.type = None
        self.sender = None
        self.message = None

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

                self.type, self.sender, self.message = self.parsed_packet

        except ConnectionResetError:
            pass

    def parse(self, packet):
        packet = str(packet)

        sender = ""

        datatype = int(packet[0])

        message = ""

        sender_ok = False

        for i in range(len(packet)):

            if i > 0 and sender_ok == False:

                if len(sender) > 1:
                    if packet[i] == "_":
                        sender_ok = True

                sender += packet[i]
                if sender_ok:
                    continue

            if sender_ok:
                message += packet[i]

        return (datatype, sender, message) #(int, string, string)

    def getall(self):
        return (self.datatype, self.sender, self.message)

    def HEADER_SIZE():
        return int(2048)

    def FORMAT():
        return str('utf-8')

    def send(conn, datatype, message):

        sender = conn.getsockname()
        
        raw_msg = f"{str(datatype)}_{str(sender)}_{str(message)}".encode(Packet.FORMAT())
        
        size = str(len(raw_msg)).encode(Packet.FORMAT())
        size += b' ' * (Packet.HEADER_SIZE() - len(size))

        try:
            conn.send(size)
            conn.send(raw_msg)
        except ConnectionResetError:
            #close connection
            pass

                