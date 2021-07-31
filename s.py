import socket
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
FORMAT = "utf-8"
SIZE = 2048
FILE ="SalesFile.csv"
file = pd.read_csv(FILE)

def salesAnalysis():
    try:
        yr = list(sorted(set(file["Year"])))
        a=list(file.groupby(['Year'])['Number'].max())
        b=list(file.groupby(['Year'])['Number'].min())
        x = np.arange(len(yr))  
        width = 0.35  

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2,a, width, label='Max')
        rects2 = ax.bar(x + width/2, b, width, label='Min')
        
        ax.set_ylabel('Client Count')
        ax.set_xlabel('Year')
        ax.set_xticks(x)
        ax.set_xticklabels(yr)
        ax.set_title('Sales Analysis')
        ax.legend()
        fig.tight_layout()
        plt.show()
        op = plt.savefig("Sales.jpg")
        conn.send(bytes("[Successful] Sales Log Generated ",FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))
    
def revenue():
    try:
        file['NetRevenue'].fillna((file["Number"] * 99), inplace=True)
        file.to_csv(FILE, index=False)
        conn.send(bytes(FILE,FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))


def addAttr(dataSet):
    try:
        fname = os.path.basename(dataSet)
        fileNew = pd.read_csv(fname)
        tempFile=pd.concat([file,fileNew], axis = 1)
        tempFile.to_csv(FILE, index=False)       
        conn.send(bytes(FILE,FORMAT))
    except:
        conn.send(bytes("[Fail] Error",FORMAT))  


host = socket.gethostname() #dynamic IP
port = 5001
print("[STARTING] Server is starting")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
print("[LISTENING] Server is listening")

while True:
    conn, addr = server.accept() # addr = (host,port)
    print("[CONNECTION] Server is connected ", addr)
    inp = (conn.recv(SIZE).decode(FORMAT)).split(" ")
    if inp[0] =="0":
        break
    elif inp[0] =="1":
        salesAnalysis()
    elif inp[0] =="2":
        revenue()
    elif inp[0] == "3":
        addAttr(inp[1])
    conn.close()

server.close()