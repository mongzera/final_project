

requests = ["LOGIN_REQUEST", "REGISTER_REQUEST"]
response = ["LOGIN_AUTHENTICATED", "REGISTRATION_AUTHENTICATED"]

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

               

def parse_client_request(packet):

    datatype, sender, message, recipient = packet.getall()

    datatype = int(datatype)

    message = str(message)

    

    if datatype == 5: #CLIENT_REQUEST packet.types[5] = "client_request"
        if message == requests[0]:
            request_code = 0
        elif message == requests[1]:
            request_code = 1
        else:
            request_code = -1
        
        return request_code

def auth_login(info, conn):

    username, password = info

    names = [['ethan', 'gamat'], ['van', 'quitong']]


    for i in names:
        if username == i[0] and password == i[1]:
            from client import Client
            return Client(conn, username, password)
    return -1

def handle_client_request(request_code, packet, conn):
    datatype, sender, message, recipient = packet.getall()

    if request_code == 0: #handle login request

        username, password = str(message).split("&")

        print(username, password)

        client = auth_login((username, password), conn)
        return client


