import socket
import pandas as pd
import os
FORMAT = "utf-8"
SIZE = 2048

host = socket.gethostname() #dynamic IP
port = 5001
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

lst = {0:"Disconnect",1:"Generate Sales Graph", 2:"Calculate Revenue", 3:"Add Attribute -- Dataset"}

for i, j in lst.items():
    print(i,": ",j)
print()
inp = input()

if inp == "3":
    dfile = (input("Dataset: \n"))
    inp = inp+" "+dfile
    client.send(bytes(inp,FORMAT))
    inp = "3"
else :
    client.send(bytes(inp,FORMAT))


if inp == "2" or inp == "3":
    f =  client.recv(SIZE).decode(FORMAT)
    fname = os.path.basename(f)
    file = pd.read_csv(fname)
    print("FILE INFO:\n")
    print(file.info())
    print("\nFILE CONTENT\n")
    print(file)
    print("[Successful] Updated ")
else:
    print (client.recv(SIZE).decode(FORMAT))

client.close()