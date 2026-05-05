import tkinter as tk
import os 
from PIL import ImageTk, Image

class Task():

    def __init__(self, frame):
        self.frame = frame
        self.tasks = []
        self.vars = []
        if os.path.exists('userInterface/tasks.txt'):
            with open('userInterface/tasks.txt','r') as f:
                self.tasks = [line.strip() for line in f if line.strip()]
            for task in self.tasks:
                var = tk.IntVar()
                self.vars.append(var)
                cb = tk.Checkbutton(self.frame, text=task, variable=var, fg='white', bg='teal', selectcolor='teal')
                cb.pack(anchor='w')

    def add_task(self, task_str):
        if task_str.strip():
            self.tasks.append(task_str)
            with open('userInterface/tasks.txt','a') as f:
                f.write(task_str + '\n')
            var = tk.IntVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self.frame, text=task_str, variable=var, fg='white', bg='teal', selectcolor='teal')
            cb.pack(anchor='w')

    def del_task(self):
        pass

    def display_task(self):
        print(self.task_str)
root = tk.Tk()

root.title("TO-DO_LIST")
# root.minsize(400,200)
root.geometry('350x500')
root.resizable(0,0)
root.configure(background = 'teal')

heading = tk.Label(root, text='My TO-DO-List', fg='white', bg='teal')
heading.pack(pady=(20,10))
heading.config(font=('verdana', 20))

tk.Label(root, text='Type a new Task here!! ', fg='white', bg='teal').pack(pady=(20,0))
entry = tk.Entry(root, width=40)
entry.pack(ipady=5,pady=(0,10))

task_frame = tk.Frame(root, bg='white')
task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

ob = Task(task_frame)

tk.Button(root, text='Add Task', width=25, command=lambda: ob.add_task(entry.get())).pack()

root.mainloop()