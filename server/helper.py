from client import Client
from common.packet import Packet

def parse_userlogin(data):
    underscores = 0

    username = ""
    password = ""

    for i in data:
        if i == "_":
            underscores += 1
            continue
        
        if underscores == 1:
            username += i

        if underscores == 2:
            password += i

    return (username, password)

def auth_login(u_p):
    username = u_p[0]
    password = u_p[1]

    if username == "ethan" and password == "gamat":
        return 0

def parse_client_request(packet):
    requests = ["LOGIN_REQUEST", "REGISTER_REQUEST"]

    datatype, sender, message = packet.getall()


    message = int(message)
    if datatype == packet.types[4]:
        if message == 0:
            request_code = 0
        elif message == 1:
            request_code = 1
        else:
            request_code = -1

def auth_login(info, client_comp):
    username, password = info

    conn, addr = client_comp


    if username == "ethan" and password == "gamat":
        return Client(conn, addr, username, password)
    return -1

def handle_client_request(request_code, packet, client_comp, connected_clients):
    datatype, sender, message = packet.getall()

    if request_code == 0: #handle login request
        username, password = str(message).split("&")

        client = auth_login((username, password), client_comp)
        print(f"CLIENT:{client}")
        return client


