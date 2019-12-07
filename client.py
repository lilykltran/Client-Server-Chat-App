#Lily Tran
import select, socket, sys

#AF_INET is the address domain of the socket. This is used when we have an Internet Domain with any two hosts
#The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allow to reuse a socket before it times out
server.connect(('localhost', 50000)) #trying to connect to server
print("Server connected\n")
inputs = [sys.stdin, server]
outputs = []

try:
	while True:
	    readable, writable, exceptional = select.select(inputs, outputs, inputs)
	    for s in readable:
			if s is server:
				message = s.recv(4000)
				if not message:
					print("Uh oh...server is down.")
					sys.exit(0)
				else:
					if message == '$QUIT$'.encode():
						sys.stdout.write('Exited server.\n')
						sys.exit(0)
					else:
						sys.stdout.write(message.decode())
						if 'Please enter in a nickname' in message.decode():
							namePrompt = True
						else:
							namePrompt = False
						sys.stdout.flush()
			else:
				if(namePrompt):
					message = 'name: ' + sys.stdin.readline()
				else:
					message = sys.stdin.readline()
				server.sendall(message.encode())

except KeyboardInterrupt:
    sys.exit(0)
		
