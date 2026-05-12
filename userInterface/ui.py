import tkinter as tk
import os 
from PIL import ImageTk, Image

class Task():

    def __init__(self, frame):
        self.frame = frame
        self.tasks = []
        self.vars = []
        self.checkbuttons = []
        self.completed_tasks = []
        self.completed_vars = []
        self.completed_checkbuttons = []
        self.pending_frame = tk.Frame(frame, bg="#84BEC4")
        self.pending_frame.pack(anchor='w')
        tk.Label(self.pending_frame, text="Pending Tasks", fg='black', bg='#84BEC4').pack(anchor='w')
        self.completed_frame = tk.Frame(frame, bg="#84BEC4")
        self.completed_frame.pack(anchor='w', pady=(20,0))
        tk.Label(self.completed_frame, text="Completed Tasks", fg='black', bg='#84BEC4').pack(anchor='w')
        if os.path.exists('userInterface/tasks.txt'):
            with open('userInterface/tasks.txt','r') as f:
                self.tasks = [line.strip() for line in f if line.strip()]
            for task in self.tasks:
                var = tk.IntVar()
                self.vars.append(var)
                cb = tk.Checkbutton(self.pending_frame, text=task, variable=var, fg='black', bg='#84BEC4', selectcolor='white', command=self.mark_completed)
                cb.pack(anchor='w')
                self.checkbuttons.append(cb)

    def add_task(self, task_str):
        if task_str.strip():
            self.tasks.append(task_str)
            with open('userInterface/tasks.txt','a') as f:
                f.write(task_str + '\n')
            var = tk.IntVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self.pending_frame, text=task_str, variable=var, fg='black', bg='#84BEC4', selectcolor='white', command=self.mark_completed)
            cb.pack(anchor='w')
            self.checkbuttons.append(cb)
            entry.delete(0, tk.END)

    def mark_completed(self):
        to_move = []
        for i, var in enumerate(self.vars):
            if var.get() == 1:
                to_move.append(i)
        for i in reversed(to_move):
            task = self.tasks.pop(i)
            var = self.vars.pop(i)
            cb = self.checkbuttons.pop(i)
            cb.destroy()
            self.completed_tasks.append(task)
            self.completed_vars.append(var)
            cb_completed = tk.Checkbutton(
                self.completed_frame,
                text=task,
                variable=var,
                fg='black',
                bg='#84BEC4',
                selectcolor='white',
                command=self.unmark_completed
            )
            cb_completed.pack(anchor='w')
            self.completed_checkbuttons.append(cb_completed)

    def unmark_completed(self):
        to_move = []
        for i, var in enumerate(self.completed_vars):
            if var.get() == 0:
                to_move.append(i)
        for i in reversed(to_move):
            task = self.completed_tasks.pop(i)
            var = self.completed_vars.pop(i)
            cb = self.completed_checkbuttons.pop(i)
            cb.destroy()
            self.tasks.append(task)
            self.vars.append(var)
            cb_pending = tk.Checkbutton(
                self.pending_frame,
                text=task,
                variable=var,
                fg='black',
                bg='#84BEC4',
                selectcolor='white',
                command=self.mark_completed
            )
            cb_pending.pack(anchor='w')
            self.checkbuttons.append(cb_pending)

    def clear_table(self):
        remaining_completed = []
        remaining_completed_vars = []
        remaining_completed_cbs = []
        for task, var, cb in zip(self.completed_tasks, self.completed_vars, self.completed_checkbuttons):
            if var.get() == 1:
                cb.destroy()
            else:
                remaining_completed.append(task)
                remaining_completed_vars.append(var)
                remaining_completed_cbs.append(cb)
        self.completed_tasks = remaining_completed
        self.completed_vars = remaining_completed_vars
        self.completed_checkbuttons = remaining_completed_cbs
        with open('userInterface/tasks.txt','w') as f:
            for task in self.tasks + self.completed_tasks:
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


ob = Task(task_frame)

add_tsk_btn = tk.Button(root, text='Add Task', width=25, command=lambda: ob.add_task(entry.get()))
add_tsk_btn.pack(anchor='nw')
entry.bind("<Return>", lambda event: ob.add_task(entry.get()))

del_tsk_btn = tk.Button(root, text="Clear Completed Tasks", width=25, command=ob.clear_table)
del_tsk_btn.pack(anchor='nw',pady=10)


# completed_Tasks = tk.Label(task_frame, text="Completed Tasks", fg='black').pack()
root.mainloop()