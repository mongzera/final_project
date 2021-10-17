import sqlite3

requests = ["LOGIN_REQUEST", "REGISTER_REQUEST", "CREATE_GROUP_REQUEST", "GROUP_JOIN_REQUEST"]
response = ["LOGIN_AUTHENTICATED", "REGISTRATION_AUTHENTICATED", "CLIENT_CHANNEL_UPDATE", "LOGIN_FAILED", "ACCOUNT_ALREADY_EXISTED", "USER_ALREADY_LOGGED_IN", "CHANNEL_EXISTS", "GROUP_JOINED_SUCCESFULLY", "GROUP_CHANNEL_UPDATE", "CHANNEL_CREATED_SUCCESSFULLY"]

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

        elif message == requests[2]:
            request_code = 2
        elif message == requests[3]:
            request_code = 3
        else:
            request_code = -1
        
        return request_code

def auth_login(info, conn, server):
    from client import Client
    username, password = info

    sqlconn = sqlite3.connect('users.db')

    sqlcur = sqlconn.cursor()

    sqlcur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password))

    output = sqlcur.fetchone()

    sqlconn.close()

    print(output)

    if output == None:
        return Client.wrong_username_and_password(conn[0])
    
    for i in server.connectedClients:
        if info[0] == i.username:
            print("CLIENT ALREADY LOGGED IN")
            return Client.already_logged_in(conn[0])

    return Client(conn, username, password)

def auth_registration(info, conn):
    from common.packet import Packet

    username, password = info

    sqlconn = sqlite3.connect('users.db')

    sqlcur = sqlconn.cursor()

    sqlcur.execute("SELECT * FROM users WHERE username = '{}'".format(username))

    result = sqlcur.fetchone()

    if result != None:
        Packet.send(conn[0], 4, response[4], conn[1])
        return -1
    sqlcur.close()

    sqlcur = sqlconn.cursor()

    sqlcur.execute("INSERT INTO users (username, password) VALUES('{}', '{}')".format(username, password))
    sqlconn.commit()

    sqlconn.close()

    Packet.send(conn[0], 4, response[1], conn[1])

    return -1

def handle_client_request(request_code, packet, conn, server):
    datatype, sender, message, recipient = packet.getall()


    if request_code == 0: #handle login request

        username, password = str(message).split("&")

        print(username, password)

        client = auth_login((username, password), conn, server)
        if client == -1:
            return -1
        client.set_server(server)
        server.connectedClients.append(client)
        server.response_to_all(4, server.get_connected_clients_addr(), response[2])
        return client

    if request_code == 1: #handle registration request

        username, password = str(message).split("&")

        print(f'[A USER IS TRYING TO REGISTER] ({username}, {password})')
        return auth_registration((username, password), conn)

    if request_code == 2:#GROUP CREATE REQUEST

        from common.packet import Packet
        datatype, sender, message, recipient = packet.getall()

        group_name = str(message)
        print(f"GROUP: {group_name}")

        for i in server.activeChannel:
            if group_name == i[0]:
                print("FOUND GROUP")
                Packet.send(conn[0], 4, response[6], conn[1])
                return -1
        create_group(server, group_name, conn)
        return 0

    if request_code == 3: #JOIN GROUP REQUEST

        print("JOIN GROUP REQUEST")
        from common.packet import Packet
        #packet = Packet(conn[0])
        datatype, sender, message, recipient = packet.getall()

        group_name = str(message)
        group_name = group_name.replace(" ", "")
        print("GROUPNAME:"+group_name)
        for i in server.activeChannel:
            if group_name == i[0]:
                print("FOUND GROUP")
                Packet.send(conn[0], 4, response[7], conn[1])
                client = server.search_user(conn[1])
                client.channels.append(i)
                client.message_group(group_name, client.username, "I AM JOINING...")
                
                return 0
        return -1

def create_group(server, group_name, conn):
    from common.packet import Packet

    print(f"[CREATING GROUP]: {group_name}")

    channel_socket = 100100+len(server.activeChannel)

    server.updateActiveChannel(group_name, channel_socket)
    Packet.send(conn[0], 4, response[9], conn[1])
    Packet.send(conn[0], 4, f"{group_name}&{channel_socket}", conn[1])

    server.search_user(conn[1]).channels.append(server.activeChannel[len(server.activeChannel)-1])





