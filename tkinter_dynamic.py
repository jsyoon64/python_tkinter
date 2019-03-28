import tkinter as tk

counter = 0

def counter_label(label):
    counter = 0

    def count():
        global counter
        counter += 1
        label.config(text=str(counter))

        """
        .after(delay, callback=None) is a method defined for all tkinter widgets.
        This method simply calls the function callback after the given delay in ms.
        """
        label.after(1000, count)

    count()

root = tk.Tk()
root.title("Counting Seconds")
label = tk.Label(root, fg="dark green")
label.pack()
counter_label(label)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
root.mainloop()