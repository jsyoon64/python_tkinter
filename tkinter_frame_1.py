from tkinter import *

class GUI_Start:

    def __init__(self, master):
        self.master = master
        self.master.geometry('300x300')
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.win_colour = '#D2B48C'
        self.current_page=0

        self.pages = []
        for i in range(5):
            page = Page(self.master,i+1)
            page.grid(row=0,column=0,sticky='nsew')
            self.pages.append(page)

        self.pages[0].tkraise()

        def Next_Page():
            next_page_index = self.current_page+1
            if next_page_index >= len(self.pages):
                next_page_index = 0
            print(next_page_index)
            self.pages[next_page_index].tkraise()
            self.current_page = next_page_index

        page1_button = Button(self.master, text='Visit next Page',command = Next_Page)
        page1_button.grid(row=1,column=0)



class Page(Frame):

    def __init__(self,master,number):
        super().__init__(master,bg='#D2B48C')
        self.master = master
        self.master.tkraise()

        page1_label = Label(self, text='PAGE '+str(number))
        page1_label.pack(fill=X,expand=True)



root = Tk()
gui = GUI_Start(root)
root.mainloop()