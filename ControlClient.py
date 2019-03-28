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
        Radiobutton(self.frame1,
                            text=language,
                            # indicatoron=0,
                            # width = 20,
                            padx=20,
                            variable=self.v,
                            command=self.ShowChoice,
                            value=val).pack(anchor=W)

    def addClientButton(self, ButtonID):
        Button(self.frame1, text=ButtonID, fg="red", command=self.showDetail(ButtonID))


    def showChoice(self, btn, key, key1):
        val = CtrClient.currClients[key][key1]
        if(key1 == 'STYLE'):
            val = val +1
            if(val > 10):
                val = 0
            CtrClient.currClients[key][key1] = val
            btn.config(text=str(val))

        else:
            CtrClient.currClients[key][key1] = 1 if val == 0 else 0
            text1 = 'OFF' if (CtrClient.currClients[key][key1] == 0) else 'ON'
            btn.config(text=text1)

    def showDetail(self,key):
        Button(self.frame2,text='Power A',width=12,command=lambda:self.showChoice(lebalPA, key, 'PA')).grid(row=0,column=0)
        Button(self.frame2,text='Power B',width=12,command=lambda:self.showChoice(labelPB, key, 'PB')).grid(row=0,column=1)
        Button(self.frame2,text='LED',width=12,command=lambda:self.showChoice(labelLED, key, 'LED')).grid(row=0,column=2)
        Button(self.frame2,text='STYLE',width=12,command=lambda:self.showChoice(labelSTYLE, key, 'STYLE')).grid(row=0,column=3)

        text1 = 'OFF' if(CtrClient.currClients[key]['PA'] == 0) else 'ON'
        lebalPA=Label(self.frame2,relief=RIDGE,text=text1,width=12).grid(row=1,column=0)
        text1 = 'OFF' if(CtrClient.currClients[key]['PB'] == 0) else 'ON'
        labelPB=Label(self.frame2,relief=RIDGE,text=text1,width=12).grid(row=1,column=1)
        text1 = 'OFF' if(CtrClient.currClients[key]['LED'] == 0) else 'ON'
        labelLED=Label(self.frame2,relief=RIDGE,text=text1,width=12).grid(row=1,column=2)
        text1 = str(CtrClient.currClients[key]['STYLE'])
        labelSTYLE=Label(self.frame2,relief=RIDGE,text=text1,width=12).grid(row=1,column=3)


root = Tk()
client = CtrClient(('localhost',4100))

root.title("Control Pedestal GUI")
gui = CtrGui(root)
root.mainloop()