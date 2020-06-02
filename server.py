# will be run in the server which has a static IP
import socket
import sys

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

def create_socket():
    try:
        global serverIP
        global portNo
        global s
        serverIP = ""
        portNo = 1234
        print("Creating socket: "+serverIP+":"+str(portNo))
        s = socket.socket()
    except socket.error as err:
        print("Error while creating socket: "+str(err))

def bind_socket():
    try:
        global serverIP
        global portNo
        global s
        print("Binding socket...")
        s.bind((serverIP, portNo))
        s.listen(5)

    except socket.error as err:
        print("Error while binding socket: "+str(err))

def accepting_connection():
    # close if any open connection
    for conn from all_connections:
        conn.close()

    del all_connections[:]
    del all_address[:]

    while true:
        try:
            conn, addr = s.accept()
            s.setblocking(1) # to avoid timeout

            all_address.append(addr)
            all_connections.append(conn)

            print("Connection established with: "+addr)
        except:
            print("Error making connection.. :(")

def main():
    create_socket()
    bind_socket()

main()