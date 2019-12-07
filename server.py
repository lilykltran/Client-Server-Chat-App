#Lily Tran
import select, socket, sys, pdb
import chat
from chat import Menu, Room, Peer

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allow to reuse a socket before it times out
server.setblocking(0)
server.bind(('localhost', 50000))
server.listen(10) #10 clients connected
print('IRC chat is up and running at localhost:50000')
menu = Menu()
inputs = [] #sockets from which we expect to read
inputs.append(server)
outputs = [] #sockets from which we expect to write

while True:
    #asynchronous way to work with sockets. Delegate maintaining the socket's state to an operating system and letting it notify the program when there is something to read from the socket or when it is ready for writing.
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
	    
    for s in readable:
        if s is server: 
            connection, client_address = s.accept()
            connection.setblocking(0)
            newMember = Peer(connection)
            inputs.append(newMember)
            menu.welcome(newMember)
	
        else:
            message = s.socket.recv(4000)
            if message:
                message = message.decode()
                menu.greeting(s, message)
            else:
                s.socket.close()
                inputs.remove(s)
    
    for s in exceptional:
        inputs.remove(s)
        s.close()
