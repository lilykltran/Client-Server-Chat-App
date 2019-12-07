#Lily Tran
import socket, pdb, sys

class Peer:
    def __init__(self, socket, name = "New client"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.currentRoom="New room"

    def fileno(self):
        return self.socket.fileno()
 
class Menu:
    def __init__(self):
        self.rooms = {} 
        self.roomMap = {}
	self.membersMap = {}

    def welcome(self, member):
        member.socket.sendall(b'Please enter in a nickname:\n')

    def greeting(self, member, message ):
        instructions = b'Type in:\n\n1. to list all rooms and its members\n\n2. [roomname] to create a new room or join an existing room\n\n3. to switch rooms\n\n4. [roomname] to leave room\n\n5. to show instructions\n\n6. to disconnect from the server\n\n'
        print(member.name + ": " + message )

        caseNum = message.split('.')

        if 'name:' in caseNum[0]:
            name = message .split()[1]
            member.name = name
            print(member.name + ' connected')
	    self.membersMap[member.name]=member
            member.socket.sendall(instructions)

        elif caseNum[0] == '1':
            print self.rooms
            print self.roomMap
            if len(self.rooms) == 0:
                message = 'No rooms. Type in: \n\n2. [roomname] to create a new room\n\n'
                member.socket.sendall(message.encode())
            else:
                message = '\nCurrent rooms and its members: '
                for room in self.rooms:
                    print (self.rooms[room].members)
                    for m in self.rooms[room].members:
                        message += m.name +"\n"
                member.socket.sendall(message .encode())

        elif caseNum[0] == '2':
            isMember = False
            if len(message .split()) >= 2:
                roomName = message.split()[1]
                member.currentRoom = roomName
                if member.name+"-"+roomName in self.roomMap:
                    if self.roomMap[member.name+"-"+roomName] == roomName:
                        member.socket.sendall(b'You are already a member of this room ' + roomName.encode())
                        isMember = True
                    else:
                        old_room = self.roomMap[member.name+"-"+roomName]
                if not isMember:
                    if not roomName in self.rooms: 
                        new_room = Room(roomName)
                        self.rooms[roomName] = new_room
                    self.rooms[roomName].members.append(member)
                    self.rooms[roomName].welcome(member)
                    self.roomMap[member.name+"-"+roomName] = roomName
            else:
                member.socket.sendall(instructions)

        elif caseNum[0] == '3':
            if len(message.split()) >= 2:
                switchroomname=message.split()[1]
                if member.name+"-"+switchroomname in self.roomMap:
                    member.currentRoom = switchroomname
                else:
                    message = "You are not currently a member of this room. Type in: \n\n2. [roomname] to join."
                    member.socket.sendall(message.encode())
            else:
                member.socket.sendall(instructions)

        elif caseNum[0] == '4':
            member.socket.send('You left the room\n')
            member.socket.sendall(instructions)

        elif caseNum[0] == '5':
            member.socket.sendall(instructions)
        
        elif caseNum[0] == '6':
            member.socket.sendall('$QUIT$'.encode())

        #else:
        if member.name+"-"+member.currentRoom in self.roomMap and caseNum[0] != '6':
            self.rooms[self.roomMap[member.name+"-"+member.currentRoom]].send_all(member, message.encode())
        else:
            message = 'You are not a member of a room.  Type in: \n\n1. to see available rooms!\n\n2. [roomname] to join a room!\n\n'
            member.socket.sendall(message.encode())
    
    def remove_member(self, member):
        print(member.name + " left\n")
    
    
class Room:
    def __init__(self, name):
        self.members = [] 
        self.name = name
    
    def send_all(self, from_member, message):
        message = from_member.name.encode() + b":" + message
        for member in self.members:
            member.socket.sendall(message)

    def welcome(self, from_member):
        message = 'Welcome to room: ' + self.name + ', ' + from_member.name + '\n'
        for member in self.members:
            member.socket.sendall(message.encode())