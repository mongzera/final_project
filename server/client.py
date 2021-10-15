from common.packet import Packet
class Client():
    def __init__(self, conn, addr, username, password):
        self.requests = ["LOGIN_REQUEST"]

        self.username = username
        self.password = password

        self.addr = addr

        self.conn = conn

        Packet.send(self.conn, 0, "SERVER", "0")

        pass

    def handle_client(self, packet):
        return "YES"

        pass