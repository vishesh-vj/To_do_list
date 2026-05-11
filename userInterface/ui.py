import tkinter as tk
import os 
from PIL import ImageTk, Image

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
root.geometry('350x500')
root.resizable(1,1)
root.configure(background = '#9BCACD')

heading = tk.Label(root, text='My TO-DO-List', fg='white', bg='#006564')
heading.pack(pady=(20,10))
heading.config(font=('verdana', 20))

tk.Label(root, text='Type a new Task here!! ', fg='white', bg='#006564').pack(pady=(20,0))
entry = tk.Entry(root, width=40)
entry.pack(ipady=5,pady=(0,10))

scroll_frame = tk.Frame(root, bg="#84BEC4")
canvas = tk.Canvas(scroll_frame, bg="#84BEC4", highlightthickness=0)
scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#84BEC4")

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

add_tsk_btn = tk.Button(root, text='Add Task', width=25, command=lambda: ob.add_task(entry.get()))
add_tsk_btn.pack(anchor='nw')

del_tsk_btn = tk.Button(root, text="Delete Task", width=25, command=ob.del_task)
del_tsk_btn.pack(anchor='nw',pady=10)


root.mainloop()