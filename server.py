# import socket
# from _thread import *
# import sys

# # server = '10.0.220.31'
# server = '127.0.0.1'
# # port = 51578
# port = 8080

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)

# s.listen(2)
# print("Waiting for a connection, Server Started")
# 0

# def threaded_client(conn):
#     conn.send(str.encode("Connected"))
#     reply = ""
#     while True:
#         try:
#             data = conn.recv(2048)
#             reply = data.decode("utf-8")

#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 print("Received: ", reply)
#                 print("Sending : ", reply)

#             conn.sendall(str.encode(reply))
#         except:
#             break

#     print("Lost connection")
#     conn.close()


# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)

#     start_new_thread(threaded_client, (conn,))
    
    
    
# import socket
# import select
    
# """
# Message transmission

# Init new message:
# A = Message ID
# B = User ID
# C = Message Length
# AAAABBBBCCCCCCCC

# Message Body:
# A = Message ID
# B = Message Part
# C = Message Data
# AAAABBBBCCCCCC....:


# Message Wrapper:
# X = Total Message length
# M = Message

# XXXMMMMMMM....:
# """



# """
# Define your data structures up here
# """   

# class Request:
#     def __init__(self, data):
#         self.headers = Headers(data[0])
#         self.body = None
#         self.parameters = None
#         self.protocol = None
    
# class Headers:
#     def __init__(self):
#         pass
    

# class Response:
#     def __init__(self, data):
#         self.code = data
        
#         # self.body = 


# class MessageData:
#     def __init__(self, id, sender, length):
#         self.id = id
#         self.sender = sender
#         self.length = length
#         self.packetSize = 512
#         self.packets = [[] for i in range(floor(length/self.packetSize) + 1)]
#         self.completed = False
        
#     def addData(self, data):
#         """
#             add data logic in here
#         """
        
#     def returnRequest(self):
#         """
#         add logic to instanciate and return a request obj
#         """

# class Server:
#     def __init__(self):
        
#         self.routeTable = {
#             "updatePosition": self.updatePosition,
#             "broadcastPositions": self.broadcastPositions,
#             "addPlayer": self.addPlayer
#         }
        
#         self.HOST = "127.0.0.1"
#         self.PORT = 5555
       
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind(self.HOST, self.PORT)
    
#         self.messageDatas = {}
#         self.clients = {}
#         self.sockets = [self.server_socket]
        
#         self.listen()
    
#     def listen(self):
#         self.server_socket.listen()
#         self.server_socket.setblocking(False) ## -> allows it to async stuff
#         while True:
#             """CHECK TO SEE IF ANY REQUESTS HAVE COME IN"""
#             readable_sockets, _, _ = select.select(self.sockets, [], [])
            
#             for sock in readable_sockets:
#                 if sock is self.server_socket:
#                     # Handle new connection to the server
#                     conn, addr = self.server_socket.accept()
#                     conn.setblocking(False)
#                     self.sockets.append(conn)
#                 else:
#                     # Handle msg data from an existing client connected to server
#                     try:
#                         # data = sock.recv(512).decode("utf-8")
#                         data = self._recv(sock)
#                         if data:
#                             # handle if new message or not
#                             if data[3:7] not in self.messageDatas:
#                                 self.messageDatas = MessageData(data[3:7], data[7:11], data[11:19])
#                             else:
#                                 self.messageDatas[data[3:7]].addData(data)
#                         else:
#                             # No data means the client has disconnected
#                             self.disconnectClient(sock)

#                     except ConnectionResetError:
#                         # Handle abrupt client disconnection
#                         self.disconnectClient(sock)
            
#             for request_id, request in self.messageDatas.items():
#                 if request.complete:
#                     del self.messageDatas[request_id]
#                     self.handleRequest(request)

                
#     def _recv(self, sock):
#         try:
#             # Get data from socket
#             data = sock.recv(512).decode("utf-8")
#             # Check length is correct
#             length = int(data[:3])
#             if length != len(data[3:]):
#                 return None
#             else:
#                 return data
                
#         except Exception as e:
#             print(e)
#             return None
    
#     def connectClient(self):
#         pass
    
#     def disconnectClient(self, sock):
#         self.sockets.remove(sock)
#         sock.close()
    
#     def handleRequest(self, request):
#         """
#         Stage 1. Parse the reqeust
        
#         - Identify protocol (HTTP, FTP, WS, Custom etc...)
#         - Parse the method (GET, POST, PUT etc...)
#         - extract headers, body and parameters
        
#         """
#         headers, body, parameters, protocol, method = self.parseRequest(request)
        
#         """
#         Stage 2. Route the Request (find Endpoint)
        
#         - Pass the extracted header, body and parameters to the correct part of the application
#         - Typically done by a route table (dictionary)
#         - Return Unknown if route doesn exist (404 for HTTP)
        
#         """
        
#         endpoint = self.routeRequest(protocol, method, headers)
        
#         """
#         Stage 3. Process the request
        
#         - Execute the approriate function/method/code for the specific route
        
#         """
        
#         result = endpoint(headers, body, parameters)
                
#         """
#         Stage 5. Generate Response
        
#         - Format the result into a reponse
        
#         """
        
#         response = self.generateReponse(result)
        
#         """
#         Stage 6. Send Response
        
#         - Send the response back to the client 
        
#         """
        
#         self.sendResponse(response)
        
#     def parseRequest(self, request):
        
        
#         return headers, body, parameters, protocol, method
    
#     def decodeRequest(self, request):
#         """
#         Here you need a method to validate whether you have a full and valid request.

#         """
    
#     def routeRequest(self, protocol, method, headers):
#         """ 
#         Find the correct method on your server.
        
#         This may request various routing depending on how complex your server is.
        
#         Different protocols may be forwarded to different servers.
        
#         For simplicity, we will just have this will just look up the method via name
#         on the sever class. We will look in our header for the route
#         """
#         # Grab route from header
#         route = headers.route
        
#         # Check if route exists, if so return code obj, else return routeNotFound obj
#         if route not in self.routeTable:
#             return self.routeNotFound
#         else:
#             return self.routeTable[route] 
    
#     def routeNotFound(self, headers, body, parameters):
#         """
#         Add error handling in here
#         """
        
#         return (False, "Route not found")
    
    
#     ###################################################################################
#     ################################# Begining API logic ##############################
#     ###################################################################################

#     def updatePosition(self, *args, **kwargs):
#         return (True, "some result")
    
#     def broadcastPositions(self, *args, **kwargs):
#         return (True, "some result")

#     def addPlayer(self, *args, **kwargs):
#         return (True, "some result")

            