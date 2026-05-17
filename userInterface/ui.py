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
        self.counter_var = tk.StringVar()
        self.counter_var.set("0 / 0 tasks completed")
        self.pending_frame = tk.Frame(frame, bg="#162030")
        self.pending_frame.pack(anchor='w')
        tk.Label(self.pending_frame, text="Pending Tasks",font=("Trebuchet MS", 10, "bold"), fg="#C5972A", bg="#1A3248").pack(anchor='center', fill='x')

        self.completed_frame = tk.Frame(frame, bg="#162030", pady=4)
        self.completed_frame.pack(anchor='w', fill='x')
        tk.Label(self.completed_frame, text="\u2713 Completed Tasks", font=("Trebuchet MS", 10, "bold"), fg='#546E85', bg='#162030').pack(fill='both')
        if os.path.exists('userInterface/tasks.txt'):
            with open('userInterface/tasks.txt','r') as f:
                self.tasks = [line.strip() for line in f if line.strip()]
            for task in self.tasks:
                var = tk.IntVar()
                self.vars.append(var)
                cb = tk.Checkbutton(self.pending_frame, text=task, variable=var, fg='white',bg='#162030',activebackground="#162030",activeforeground="#C5972A", selectcolor="#C5972A", command=self.mark_completed)
                cb.pack(anchor='w', pady=4)
                self.checkbuttons.append(cb)

    def add_task(self, task_str):
        if task_str.strip():
            self.tasks.append(task_str)
            with open('userInterface/tasks.txt','a') as f:
                f.write(task_str + '\n')
            var = tk.IntVar()
            self.vars.append(var)
            cb = tk.Checkbutton(self.pending_frame, text=task_str, variable=var, fg='#D6E4F0', bg='#162030', selectcolor="#C5972A", command=self.mark_completed)
            cb.pack(anchor='w',pady=4)
            self.checkbuttons.append(cb)
            entry.delete(0, tk.END)
        self.update_counter()

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
                font=("Trebuchet MS", 12,"overstrike"),
                anchor='w',
                variable=var,
                fg='#546E85',
                bg='#162030',
                activebackground='#162030',
                selectcolor='#C5972A',
                command=self.unmark_completed
            )
            cb_completed.pack(anchor='w',fill='x')
            self.completed_checkbuttons.append(cb_completed)
        self.update_counter()

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
                fg='white',
                bg='#162030',
                activebackground="#162030",
                selectcolor='#C5972A',
                command=self.mark_completed
            )
            cb_pending.pack(anchor='w',pady=4)
            self.checkbuttons.append(cb_pending)
        self.update_counter()

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
        self.update_counter()

    def update_counter(self):
        total = len(self.tasks) + len(self.completed_tasks)
        done = len(self.completed_tasks)
        self.counter_var.set(f"{done} / {total} tasks completed")

    def display_task(self):
        print(self.task_str)
root = tk.Tk()

root.title("TO-DO_LIST")
# root.minsize(400,200)
root.geometry('500x800')
root.resizable(1,1)
root.configure(background = "#0F1923")

heading = tk.Label(root, text='Task Manager', fg='#E8DCC8', bg="#0F1923",anchor='w')
heading.pack(padx=(20),anchor="w",fill="x")
heading.config(font=('verdana', 28,'bold'))
tk.Label(
    root,
    text="Stay focused. Stay ahead.",
    font=('italic', 12), fg="#FFC745", bg="#0F1923",
    padx=22
).pack(anchor="w")
tk.Frame(root, height=2, bg="#C38A04").pack(fill='x')

input_card = tk.Frame(root,bd=3, bg="#162030", pady=8, padx=2)
input_card.pack(fill="x", padx=100, pady=(20, 0))

tk.Label(input_card, text='NEW TASK',font=("Trebuchet MS", 10, "bold"),fg='#D6E4F0', background="#162030",anchor='w').pack(fill='x',padx=6)
entry_wrap = tk.Frame(input_card, bg="#162030", highlightthickness=2, highlightbackground="#162030")
entry_wrap.pack(fill='x', padx=6, pady=(0,10), anchor='w')
entry = tk.Entry(entry_wrap,bd=0,font=("Trebuchet MS", 13),width=150,background="#1C2B3A",fg="#8BA3B8",insertbackground="#C5972A")
entry.pack(ipady=9,fill='x')
entry.insert(0, "Enter your task here...")

def _focus_in(e):
    if entry.get() == "Enter your task here...":
        entry.delete(0, tk.END)
        entry.config(fg="#C5972A")
    entry_wrap.config(highlightbackground="#C5972A")

def _focus_out(e):
    if not entry.get().strip():
        entry.insert(0, "Enter your task here...")
        entry.config(fg="#8BA3B8")
    entry_wrap.config(highlightbackground="#162030")
 
entry.bind("<FocusIn>",  _focus_in)
entry.bind("<FocusOut>", _focus_out)
entry.bind("<Return>",   lambda e: ob.add_task(entry.get()))


add_tsk_btn = tk.Button(input_card, text='+ ADD TASK',font=("Trebuchet MS", 10, "bold"),fg="black",bg="#C5972A",activebackground="#C5972A",width=12,height=1, command=lambda: ob.add_task(entry.get()))
add_tsk_btn.pack(padx=6,anchor='w')

scroll_frame = tk.Frame(root, bg="#162030")
canvas = tk.Canvas(scroll_frame, bg="#162030", highlightthickness=0)
scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
task_frame = tk.Frame(canvas, bg="#162030")

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
# canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
# canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

canvas.pack(side="left", expand=True, fill="both")
scrollbar.pack(side="right", fill="y")

scroll_frame.pack(expand=True, fill="both", padx=100)

ob = Task(task_frame)

counter_label = tk.Label(
    root,
    textvariable=ob.counter_var,
    font=("Trebuchet MS", 11, "bold"),
    fg="#C5972A",
    bg="#162030",
    bd=1,
    relief="groove",
    highlightthickness=1,
    highlightbackground="#C5972A",
    highlightcolor="#C5972A",
    anchor='w',
    padx=4,
    pady=4
)
counter_label.pack(fill='x', padx=100, pady=(10, 0))



tk.Frame(root, height=2, bg="#1E3A52").pack(fill='x',padx=100,pady=(10,0))

del_tsk_btn = tk.Button(root, text="Clear Completed Tasks", width=25, command=ob.clear_table,fg='#8BAFC8', bg='#1E3A52', activebackground='#1E3A52', activeforeground='#c5972A')
del_tsk_btn.pack(anchor='nw',pady=10,padx=100)


# completed_Tasks = tk.Label(task_frame, text="Completed Tasks", fg='black').pack()
root.mainloop()