import socket
import threading
from tkinter import *
import pickle
import tkinter.ttk

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
                root.destroy()
                break

            clientLists = pickle.loads(data)
            #print(self.currClients)
            if(len(clientLists) > len(self.currClients)):
                res = clientLists.keys() - self.currClients.keys()
                newclients = {k:clientLists[k] for k in res}
                #self.currClients.update(newclients)
                CtrGui.guiClients.update(newclients)

                for key,value in newclients.items():
                    self.clientCount = self.clientCount+1
                    gui.addClientButton(key,value)
                #print(newclients)
            self.currClients.update(clientLists)

    def sendMsg(self,val):
        self.sock.send(val)

class CtrGui:

    guiClients = {}
    def __init__(self, master):
        self.master = master
        self.master.geometry('500x200')

        self.v = IntVar()
        self.v.set(1)  # initializing the choice, i.e. Python

        self.detailButton = 0

        #self.master.grid_rowconfigure(0, weight=1)
        #self.master.grid_columnconfigure(0, weight=1)
        self.win_colour = '#D2B48C'
        #self.current_page=0
        self.frame1=Frame(self.master, relief="solid", bd=1, width=150)
        self.frame1.pack(side="left", fill="both", expand=False)

        self.frame2=Frame(self.master, relief="solid", bd=1,width=350)
        self.frame2.pack(side="right", fill="both", expand=True)


    def addClientButton(self, ButtonID,value):
        buttonx = Button(self.frame1, text=ButtonID, fg="red", width=10)
        buttonx.grid(sticky='N',padx=5,pady=5)
        buttonx.config(command=lambda:self.showDetail(ButtonID))
        if(self.detailButton == 0):
            self.makeDetailButton(ButtonID,value)
            self.detailButton = 1


    def showChoice(self, Label, key, key1):
        val = self.guiClients[key][key1]
        #val = CtrClient.currClients[key][key1]
        if(key1 == 'STYLE'):
            val = val +1
            if(val > 9):
                val = 0
            #CtrClient.currClients[key][key1] = val
            self.guiClients[key][key1] =val
            #Label.config(text=str(val))
            self.comboboxSTYLE.set(val)

        else:
            val = 1 if val == 0 else 0
            self.guiClients[key][key1] = val
            text1 = 'OFF' if (val == 0) else 'ON'
            Label.config(text=text1)

        ctrMsg = ('SPP-CG'+key+ chr(0x00)+ chr(0x00)).encode('utf-8')

        if(key1 == 'PA'):
            payload = '<json>{"CON1":'+ str(val) + '}</json>'
            ctrMsg += b'\xA0' + bytes([len(payload)]) + payload.encode('utf-8')

        elif(key1 == 'PB'):
            payload = '<json>{"CON2":'+ str(val) + '}</json>'
            ctrMsg += b'\xA0' + bytes([len(payload)]) + payload.encode('utf-8')

        elif(key1 == 'LED'):
            #payload = '<json>{"OPER":'+ str(val) + ',"STYLE":'+ str(self.guiClients[key]['STYLE'])
            payload = '<json>{"OPER":'+ str(val) + ',"STYLE":'+ str(self.comboboxSTYLE.get())
            payload += ',"ONTIME":"00:00","OFFTIME":"00:00"}</json>'
            ctrMsg += b'\xA1' + bytes([len(payload)]) + payload.encode('utf-8')

        else:
            ctrMsg = ''

        if(ctrMsg != ''):
            CtrClient.sendMsg(CtrClient,ctrMsg)
            print(ctrMsg)


    def showDetail(self,key):
        print(key)
        self.buttonPA.config(command=lambda:self.showChoice(self.labelPA, key, 'PA'))
        self.buttonPB.config(command=lambda:self.showChoice(self.labelPB, key, 'PB'))
        self.buttonLED.config(command=lambda:self.showChoice(self.labelLED, key, 'LED'))
        self.buttonSTYLE.config(command=lambda:self.showChoice(self.labelSTYLE, key, 'STYLE'))

        text1 = 'OFF' if(CtrClient.currClients[key]['PA'] == 0) else 'ON'
        self.labelPA.config(text=text1)

        text1 = 'OFF' if(CtrClient.currClients[key]['PB'] == 0) else 'ON'
        self.labelPB.config(text=text1)
        text1 = 'OFF' if(CtrClient.currClients[key]['LED'] == 0) else 'ON'
        self.labelLED.config(text=text1)
        #text1 = str(CtrClient.currClients[key]['STYLE'])
        #self.labelSTYLE.config(text=text1)
        self.comboboxSTYLE.set(CtrClient.currClients[key]['STYLE'])

    def makeDetailButton(self,key,value):
        self.buttonPA = Button(self.frame2,text='Power A',width=12)
        self.buttonPA.grid(row=0,column=0,padx=2,pady=2)
        self.buttonPA.config(command=lambda:self.showChoice(self.labelPA, key, 'PA'))

        self.buttonPB = Button(self.frame2,text='Power B',width=12)
        self.buttonPB.grid(row=0,column=1,padx=2,pady=2)
        self.buttonPB.config(command=lambda:self.showChoice(self.labelPB, key, 'PB'))

        self.buttonLED = Button(self.frame2,text='LED',width=12)
        self.buttonLED.grid(row=0,column=2,padx=2,pady=2)
        self.buttonLED.config(command=lambda:self.showChoice(self.labelLED, key, 'LED'))

        self.buttonSTYLE = Button(self.frame2,text='STYLE',width=12)
        self.buttonSTYLE.grid(row=0,column=3,padx=2,pady=2)
        #self.buttonSTYLE.config(command=lambda:self.showChoice(self.labelSTYLE, key, 'STYLE'))
        self.buttonSTYLE.config(command=lambda:self.showChoice(self.comboboxSTYLE, key, 'STYLE'))

        text1 = 'OFF' if(value['PA'] == 0) else 'ON'
        self.labelPA=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        self.labelPA.grid(row=1,column=0,padx=2)
        text1 = 'OFF' if(value['PB'] == 0) else 'ON'
        self.labelPB=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        self.labelPB.grid(row=1,column=1,padx=2)
        text1 = 'OFF' if(value['LED'] == 0) else 'ON'
        self.labelLED=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        self.labelLED.grid(row=1,column=2,padx=2)

        #values = ['style '+str(i) for i in range(0,9)]
        values = [i for i in range(0,9)]
        self.comboboxSTYLE = tkinter.ttk.Combobox(self.frame2,values=values,justify='center',width=10)
        self.comboboxSTYLE.grid(row=1,column=3,padx=2)
        #self.comboboxSTYLE['values'] = ('style 0','style 1', 'style 2')
        self.comboboxSTYLE.set(value['STYLE'])
        #text1 = str(value['STYLE'])
        #self.labelSTYLE=Label(self.frame2,relief=RIDGE,text=text1,width=12)
        #self.labelSTYLE.grid(row=1,column=3,padx=2)

root = Tk()
client = CtrClient(('localhost',3100))

root.title("Control Pedestal GUI")
gui = CtrGui(root)
root.mainloop()