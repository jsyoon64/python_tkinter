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

    def sendMsg(self,val):
        self.sock.send(bytes(val, 'utf-8'))

class CtrGui:

    def __init__(self, master):
        self.master = master
        self.master.geometry('600x300')

        self.v = IntVar()
        self.v.set(1)  # initializing the choice, i.e. Python

        #self.master.grid_rowconfigure(0, weight=1)
        #self.master.grid_columnconfigure(0, weight=1)
        self.win_colour = '#D2B48C'
        #self.current_page=0
        self.frame1=Frame(self.master, relief="solid", bd=1, width=150)
        self.frame1.pack(side="left", fill="both", expand=True)

        self.frame2=Frame(self.master, relief="solid", bd=1,width=450)
        self.frame2.pack(side="right", fill="both", expand=True)


    def addClientButton(self, ButtonID):
        buttonx = Button(self.frame1, text=ButtonID, fg="red", width=15)
        buttonx.grid()
        buttonx.config(command=lambda:self.showDetail(ButtonID))


    def showChoice(self, Label, key, key1):
        val = CtrClient.currClients[key][key1]
        if(key1 == 'STYLE'):
            val = val +1
            if(val > 9):
                val = 0
            CtrClient.currClients[key][key1] = val
            Label.config(text=str(val))

        else:
            val = 1 if val == 0 else 0
            CtrClient.currClients[key][key1] = val
            text1 = 'OFF' if (val == 0) else 'ON'
            Label.config(text=text1)

        ctrMsg = 'SPP-CG'+key+ chr(0x00)+ chr(0x00)

        if(key1 == 'PA'):
            payload = '<json>{"CON1":'+ str(val) + '}</json>'
            ctrMsg = ctrMsg + chr(0xA0) + chr(len(payload)) +payload

        elif(key1 == 'PB'):
            payload = '<json>{"CON2":'+ str(val) + '}</json>'
            ctrMsg = ctrMsg + chr(0xA0) + chr(len(payload)) +payload

        elif(key1 == 'LED'):
            payload = '<json>{"OPER":'+ str(val) + ',"STYLE":'+ str(CtrClient.currClients[key]['STYLE'])
            payload += '"ONTIME":"00:00","OFFTIME":"00:00"}</json>'
            ctrMsg = ctrMsg + chr(0xA1) + chr(len(payload)) +payload

        else:
            ctrMsg = ''

        if(ctrMsg != ''):
            CtrClient.sendMsg(CtrClient,ctrMsg)
            print(ctrMsg)


    def showDetail(self,key):
        Button(self.frame2,text='Power A',width=12,command=lambda:self.showChoice(labelPA, key, 'PA')).grid(row=0,column=0)
        Button(self.frame2,text='Power B',width=12,command=lambda:self.showChoice(labelPB, key, 'PB')).grid(row=0,column=1)
        Button(self.frame2,text='LED',width=12,command=lambda:self.showChoice(labelLED, key, 'LED')).grid(row=0,column=2)
        Button(self.frame2,text='STYLE',width=12,command=lambda:self.showChoice(labelSTYLE, key, 'STYLE')).grid(row=0,column=3)

        text1 = 'OFF' if(CtrClient.currClients[key]['PA'] == 0) else 'ON'
        labelPA=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        labelPA.grid(row=1,column=0)
        text1 = 'OFF' if(CtrClient.currClients[key]['PB'] == 0) else 'ON'
        labelPB=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        labelPB.grid(row=1,column=1)
        text1 = 'OFF' if(CtrClient.currClients[key]['LED'] == 0) else 'ON'
        labelLED=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        labelLED.grid(row=1,column=2)
        text1 = str(CtrClient.currClients[key]['STYLE'])
        labelSTYLE=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        labelSTYLE.grid(row=1,column=3)


root = Tk()
client = CtrClient(('localhost',4100))

root.title("Control Pedestal GUI")
gui = CtrGui(root)
root.mainloop()