import tkinter as tk
import os 
from PIL import ImageTk, Image
import customtkinter as ctk


class Task():

    def __init__(self, frame):
        self.frame = frame
        self.tasks = []
        self.vars = []
        self.checkbuttons = []
        if os.path.exists('userInterface/tasks.txt'):
            with open('userInterface/tasks.txt','r') as f:
                self.tasks = [line.strip() for line in f if line.strip()]
            for task in self.tasks:
                var = tk.IntVar()
                self.vars.append(var)
                cb = tk.Checkbutton(self.frame, text=task, variable=var, fg='black', bg='#84BEC4', selectcolor='white')
                cb.pack(anchor='w')
                self.checkbuttons.append(cb)

    def add_task(self, task_str):
        if task_str.strip():
            self.tasks.append(task_str)
            with open('userInterface/tasks.txt','a') as f:
                f.write(task_str + '\n')
            var = tk.IntVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self.frame, text=task_str, variable=var, fg='black', bg='#84BEC4', selectcolor='white')
            cb.pack(anchor='w')
            self.checkbuttons.append(cb)
            entry.delete(0, tk.END)

    def del_task(self):
        remaining_tasks = []
        remaining_vars = []
        remaining_cbs = []

        for task, var, cb in zip(self.tasks, self.vars, self.checkbuttons):
            if var.get() == 1:
                cb.destroy()
            else:
                remaining_tasks.append(task)
                remaining_vars.append(var)
                remaining_cbs.append(cb)

        self.tasks = remaining_tasks
        self.vars = remaining_vars
        self.checkbuttons = remaining_cbs

        with open('userInterface/tasks.txt', 'w') as f:
            for task in self.tasks:
                f.write(task + '\n')

    def display_task(self):
        print(self.task_str)
root = tk.Tk()

root.title("TO-DO_LIST")
# root.minsize(400,200)
root.geometry('500x800')
root.resizable(1,1)
root.configure(background = "#FFFFFF")

heading = tk.Label(root, text='TO-DO App', fg='white', bg="#0D0245",anchor='w')
heading.pack(pady=(2),anchor="w",fill="x")
heading.config(font=('verdana', 28,'bold'))

tk.Label(root, text='Active task',font=('arieal',20,'bold'),fg='white', background="#000000",foreground="yellow").pack(pady=(15,15),fill='x',padx=150)
entry = tk.Entry(root,text="Entry your Task",width=150,background="white")
entry.pack(ipady=9,pady=(0,10),anchor='center')

add_tsk_btn = tk.Button(root, text='Add', width=25, command=lambda: ob.add_task(entry.get()))
add_tsk_btn.pack(anchor='se')

scroll_frame = tk.Frame(root, bg="#ECEFDA")
canvas = tk.Canvas(scroll_frame, bg="#ECEFDA", highlightthickness=0)
scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#ECEFDA")

task_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def _on_mousewheel(event):
    if os.name == 'nt':
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        canvas.yview_scroll(int(-1 * event.delta), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

canvas.pack(side="left", expand=True, fill="both")
scrollbar.pack(side="right", fill="y")

scroll_frame.pack(expand=True, fill="both", padx=10)

incomplete_Tasks = tk.Label(task_frame, text="Incomplete Tasks", fg='black')

ob = Task(task_frame)

del_tsk_btn = tk.Button(root, text="Delete Task", width=25, command=ob.del_task)
del_tsk_btn.pack(anchor='nw',pady=10)


root.mainloop()