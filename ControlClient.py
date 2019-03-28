import socket
import threading
from tkinter import *
import pickle

class CtrClient:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    currClients = {}
    clientCount = 0

    def __init__(self, address):
        self.sock.connect(address)
        iThread = threading.Thread(target=self.receive)
        iThread.daemon = True
        iThread.start()

    def receive(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break

            clientLists = pickle.loads(data)
            #print(clientLists)
            if(len(clientLists) > len(self.currClients)):
                res = clientLists.keys() - self.currClients.keys()
                newclients = {k:clientLists[k] for k in res}
                self.currClients.update(newclients)

                for key,value in newclients.items():
                    self.clientCount = self.clientCount+1
                    #gui.addClientRButton(key, self.clientCount)
                    gui.addClientButton(key)
                print(newclients)

    def sendMsg(self):
        #data = 'SPP-CG' + id + 'AAAA'
        # self.sock.send(bytes(input(""), 'utf-8'))
        #self.sock.send(bytes(data, 'utf-8'))
        pass

class CtrGui:
    def __init__(self, master):
        self.master = master
        self.master.geometry('300x300')

        self.v = IntVar()
        self.v.set(1)  # initializing the choice, i.e. Python

        #self.master.grid_rowconfigure(0, weight=1)
        #self.master.grid_columnconfigure(0, weight=1)
        self.win_colour = '#D2B48C'
        #self.current_page=0
        self.frame1=Frame(self.master, relief="solid", bd=1)
        self.frame1.pack(side="left", fill="both", expand=True)

        self.frame2=Frame(self.master, relief="solid", bd=1)
        self.frame2.pack(side="right", fill="both", expand=True)

    def addClientRButton(self, language, val):
        tkinter.Radiobutton(self.frame1,
                            text=language,
                            # indicatoron=0,
                            # width = 20,
                            padx=20,
                            variable=self.v,
                            command=self.ShowChoice,
                            value=val).pack(anchor=tkinter.W)

    def addClientButton(self, ButtonID):
        Button(self.frame1, text=ButtonID, fg="red", command=self.showDetail(ButtonID)).pack()


    def ShowChoice(self):
        print(self.v.get())

    def showDetail(self,key):
        Label(self.frame2,relief=RIDGE,text='Power A',width=12).grid(row=0,column=0)
        Label(self.frame2,relief=RIDGE,text='Power B',width=12).grid(row=0,column=1)
        Label(self.frame2,relief=RIDGE,text='LED',width=12).grid(row=0,column=2)
        Label(self.frame2,relief=RIDGE,text='LED STYLE',width=12).grid(row=0,column=3)

        text1 = 'OFF' if(CtrClient.currClients[key]['PA'] == 0) else 'ON'
        Button(self.frame2,text= text1,padx=5).grid(row=1,column=0)
        text1 = 'OFF' if(CtrClient.currClients[key]['PB'] == 0) else 'ON'
        Button(self.frame2,text=text1,padx=5).grid(row=1,column=1)
        text1 = 'OFF' if(CtrClient.currClients[key]['LED'] == 0) else 'ON'
        Button(self.frame2,text=text1,padx=5).grid(row=1,column=2)
        text1 = str(CtrClient.currClients[key]['STYLE'])
        Button(self.frame2,text=text1,padx=5).grid(row=1,column=3)

root = Tk()
client = CtrClient(('localhost',4100))

root.title("Control Pedestal GUI")
gui = CtrGui(root)
root.mainloop()