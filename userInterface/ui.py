import tkinter as tk
from tkinter import ttk
import os
from PIL import ImageTk, Image
from time import strftime
import threading
import time
from datetime import datetime, timedelta

try:
    from plyer import notification as plyer_notify
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


PRIORITY_CONFIG = {
    "🔴 High":   {"fg": "#E05252", "order": 0},
    "🟡 Medium": {"fg": "#C5972A", "order": 1},
    "🔵 Low":    {"fg": "#7FB3C8", "order": 2},
}
PRIORITY_LABELS = list(PRIORITY_CONFIG.keys())


class ReminderManager:
    def __init__(self):
        self.reminders   = {}
        self._lock       = threading.Lock()
        self._stop_event = threading.Event()
        self._thread     = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()

    def add_reminder(self, task_title, due_dt, on_due_callback=None):
        with self._lock:
            self.reminders[task_title] = {
                "due":      due_dt,
                "callback": on_due_callback,
                "fired":    False
            }

    def remove_reminder(self, task_title):
        with self._lock:
            self.reminders.pop(task_title, None)

    def shutdown(self):
        self._stop_event.set()

    def _watch(self):
        while not self._stop_event.is_set():
            now = datetime.now()
            with self._lock:
                for title, data in self.reminders.items():
                    if not data["fired"] and now >= data["due"]:
                        data["fired"] = True
                        self._notify(title, data["due"])
                        if data["callback"]:
                            data["callback"](title)
            time.sleep(30)

    def _notify(self, title, due_dt):
        time_str = due_dt.strftime("%I:%M %p")
        if PLYER_AVAILABLE:
            plyer_notify.notify(
                title    = "Task Due — To-Do List",
                message  = f'"{title}" was due at {time_str}',
                app_name = "Task Manager",
                timeout  = 8
            )
        else:
            try:
                root.after(0, lambda t=title, ts=time_str:
                    tk.messagebox.showinfo("Task Due", f'"{t}" was due at {ts}'))
            except Exception:
                pass


class Task():

    def __init__(self, frame):
        self.frame = frame
        self.tasks = []
        self.priorities = []
        self.vars = []
        self.checkbuttons = []

        self.completed_tasks = []
        self.completed_vars = []
        self.completed_checkbuttons = []

        self.counter_var = tk.StringVar(value="0 / 0 tasks completed")

        # Pending section
        self.pending_frame = tk.Frame(frame, bg="#162030")
        self.pending_frame.pack(anchor='w', fill='x')
        tk.Label(
            self.pending_frame, text="Pending Tasks",
            font=("Trebuchet MS", 10, "bold"),
            fg="#C5972A", bg="#1A3248"
        ).pack(anchor='center', fill='x')

        # Completed section 
        self.completed_frame = tk.Frame(frame, bg="#162030", pady=4)
        self.completed_frame.pack(anchor='w', fill='x')
        tk.Label(
            self.completed_frame,
            text="\u2713 Completed Tasks",
            font=("Trebuchet MS", 10, "bold"),
            fg='#546E85', bg='#162030'
        ).pack(fill='both')

        if os.path.exists('userInterface/tasks.txt'):
            raw_tasks, raw_pris = [], []
            with open('userInterface/tasks.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if '||' in line:
                        pri, title = line.split('||', 1)
                        pri = pri if pri in PRIORITY_CONFIG else "🟡 Medium"
                    else:
                        pri, title = "🟡 Medium", line
                    raw_tasks.append(title)
                    raw_pris.append(pri)

            combined = sorted(
                zip(raw_tasks, raw_pris),
                key=lambda x: PRIORITY_CONFIG[x[1]]["order"]
            )
            if combined:
                raw_tasks, raw_pris = map(list, zip(*combined))
            else:
                raw_tasks, raw_pris = [], []

            for title, pri in zip(raw_tasks, raw_pris):
                self.tasks.append(title)
                self.priorities.append(pri)
                var   = tk.IntVar()
                color = PRIORITY_CONFIG[pri]["fg"]
                self.vars.append(var)
                cb = tk.Checkbutton(
                    self.pending_frame,
                    text=f"{pri}  {title}",
                    variable=var,
                    fg=color, bg='#162030',
                    activebackground="#162030", activeforeground=color,
                    selectcolor="#C5972A",
                    command=self.mark_completed,
                    anchor='w', font=("Trebuchet MS", 11)
                )
                cb.pack(anchor='w', fill='x', padx=6, pady=2)
                self.checkbuttons.append(cb)

        self.update_counter()

    # Add_task Functioning
    def add_task(self, task_str, priority="🟡 Medium", hour="--", minute="--"):
        task_str = task_str.strip()
        if not task_str or task_str == "Enter your task here...":
            return
        if priority not in PRIORITY_CONFIG:
            priority = "🟡 Medium"

        with open('userInterface/tasks.txt', 'a', encoding='utf-8') as f:
            f.write(f"{priority}||{task_str}\n")

        order     = PRIORITY_CONFIG[priority]["order"]
        insert_at = len(self.tasks)
        for i, p in enumerate(self.priorities):
            if PRIORITY_CONFIG[p]["order"] > order:
                insert_at = i
                break

        self.tasks.insert(insert_at, task_str)
        self.priorities.insert(insert_at, priority)

        color = PRIORITY_CONFIG[priority]["fg"]
        var   = tk.IntVar()
        self.vars.insert(insert_at, var)

        cb = tk.Checkbutton(
            self.pending_frame,
            text=f"{priority}  {task_str}",
            variable=var,
            fg=color, bg='#162030',
            activebackground="#162030", activeforeground=color,
            selectcolor="#C5972A",
            command=self.mark_completed,
            anchor='w', font=("Trebuchet MS", 11)
        )
        cb.pack(anchor='w', fill='x', padx=6, pady=2)
        self.checkbuttons.insert(insert_at, cb)
        self._repack_pending()

        if hour != "--" and minute != "--":
            due_dt = datetime.now().replace(
                hour=int(hour), minute=int(minute), second=0, microsecond=0
            )
            if due_dt <= datetime.now():
                due_dt += timedelta(days=1)

            def on_due(title, cb_ref=cb):
                try:
                    cb_ref.config(fg="#E05252")
                except tk.TclError:
                    pass

            reminder_manager.add_reminder(task_str, due_dt, on_due_callback=on_due)

        entry.delete(0, tk.END)
        priority_var.set("🟡 Medium")
        hour_var.set("--")
        minute_var.set("--")
        self.update_counter()

    # Mark_Completed 
    def mark_completed(self):
        to_move = [i for i, v in enumerate(self.vars) if v.get() == 1]
        for i in reversed(to_move):
            task     = self.tasks.pop(i)
            priority = self.priorities.pop(i)
            var      = self.vars.pop(i)
            cb       = self.checkbuttons.pop(i)
            cb.destroy()

            reminder_manager.remove_reminder(task)

            self.completed_tasks.append(task)
            self.completed_vars.append(var)

            cb_done = tk.Checkbutton(
                self.completed_frame,
                text=f"{priority}  {task}",
                font=("Trebuchet MS", 11, "overstrike"),
                anchor='w', variable=var,
                fg='#546E85', bg='#162030',
                activebackground='#162030',
                selectcolor='#C5972A',
                command=self.unmark_completed
            )
            cb_done.pack(anchor='w', fill='x', padx=6, pady=2)
            self.completed_checkbuttons.append(cb_done)
        self.update_counter()

    # Unmark_Completed 
    def unmark_completed(self):
        to_move = [i for i, v in enumerate(self.completed_vars) if v.get() == 0]
        for i in reversed(to_move):
            task = self.completed_tasks.pop(i)
            var  = self.completed_vars.pop(i)
            cb   = self.completed_checkbuttons.pop(i)
            cb.destroy()

            priority = "🟡 Medium"
            for p in PRIORITY_CONFIG:
                if task.startswith(p + "  "):
                    priority = p
                    task = task[len(p) + 2:]
                    break

            self.tasks.append(task)
            self.priorities.append(priority)
            self.vars.append(var)

            color = PRIORITY_CONFIG[priority]["fg"]
            cb_pending = tk.Checkbutton(
                self.pending_frame,
                text=f"{priority}  {task}",
                variable=var,
                fg=color, bg='#162030',
                activebackground="#162030", activeforeground=color,
                selectcolor='#C5972A',
                command=self.mark_completed,
                anchor='w', font=("Trebuchet MS", 11)
            )
            cb_pending.pack(anchor='w', fill='x', padx=6, pady=2)
            self.checkbuttons.append(cb_pending)
            self._repack_pending()
        self.update_counter()

    # Clear_Completed_Tasks
    def clear_table(self):
        keep_tasks, keep_vars, keep_cbs = [], [], []
        for task, var, cb in zip(
                self.completed_tasks, self.completed_vars,
                self.completed_checkbuttons):
            if var.get() == 1:
                cb.destroy()
            else:
                keep_tasks.append(task)
                keep_vars.append(var)
                keep_cbs.append(cb)

        self.completed_tasks        = keep_tasks
        self.completed_vars         = keep_vars
        self.completed_checkbuttons = keep_cbs

        with open('userInterface/tasks.txt', 'w', encoding='utf-8') as f:
            for task, pri in zip(self.tasks, self.priorities):
                f.write(f"{pri}||{task}\n")
            for task in self.completed_tasks:
                pri = "🟡 Medium"
                for p in PRIORITY_CONFIG:
                    if task.startswith(p + "  "):
                        pri = p
                        break
                f.write(f"{pri}||{task}\n")

        self.update_counter()

    def _repack_pending(self):
        for cb in self.checkbuttons:
            cb.pack_forget()
        for cb in self.checkbuttons:
            cb.pack(anchor='w', fill='x', padx=6, pady=2)

    def update_counter(self):
        total = len(self.tasks) + len(self.completed_tasks)
        done  = len(self.completed_tasks)
        self.counter_var.set(f"{done} / {total} tasks completed")


def update_time():
    date_label.config(text=strftime('%Y-%m-%d'))
    time_label.config(text=strftime('%H:%M:%S'))
    date_label.after(1000, update_time)


root = tk.Tk()
root.title("TO-DO_LIST")
root.geometry('500x800')
root.resizable(1, 1)
root.configure(background="#0F1923")

# Header
header_frame = tk.Frame(root, bg="#0F1923")
header_frame.pack(fill='x', padx=20, pady=(10, 0))

tk.Label(
    header_frame, text='Task Manager',
    fg='#E8DCC8', bg="#0F1923",
    font=('verdana', 28, 'bold'), anchor='w'
).pack(side='left')

clock_frame = tk.Frame(header_frame, bg="#0F1923")
clock_frame.pack(side='right', anchor='e', pady=(8, 0))

date_label = tk.Label(clock_frame, font=('Trebuchet MS', 11, 'bold'),
                      fg='#C5972A', bg='#0F1923', anchor='e')
date_label.pack(anchor='e')

time_label = tk.Label(clock_frame, font=('Trebuchet MS', 13, 'bold'),
                      fg='#D6E4F0', bg='#0F1923', anchor='e')
time_label.pack(anchor='e')

update_time()

tk.Label(root, text="Stay focused. Stay ahead.",
         font=('italic', 12), fg="#FFC745", bg="#0F1923", padx=22).pack(anchor="w")
tk.Frame(root, height=2, bg="#C38A04").pack(fill='x')

# Input Label
input_card = tk.Frame(root, bd=3, bg="#162030", pady=8, padx=2)
input_card.pack(fill="x", padx=100, pady=(20, 0))

tk.Label(input_card, text='NEW TASK', font=("Trebuchet MS", 10, "bold"),
         fg='#D6E4F0', background="#162030", anchor='w').pack(fill='x', padx=6)

entry_wrap = tk.Frame(input_card, bg="#162030",
                      highlightthickness=2, highlightbackground="#162030")
entry_wrap.pack(fill='x', padx=6, pady=(0, 8), anchor='w')

entry = tk.Entry(entry_wrap, bd=0, font=("Trebuchet MS", 13), width=150,
                 background="#1C2B3A", fg="#8BA3B8", insertbackground="#C5972A")
entry.pack(ipady=9, fill='x')
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
entry.bind("<Return>",
           lambda e: ob.add_task(entry.get(),
                                 priority_var.get(),
                                 hour_var.get(),
                                 minute_var.get()))

options_row = tk.Frame(input_card, bg="#162030")
options_row.pack(fill='x', padx=6, pady=(0, 6))

# Priority dropdown
priority_var = tk.StringVar(value="🟡 Medium")
priority_cb  = ttk.Combobox(
    options_row, textvariable=priority_var,
    values=PRIORITY_LABELS,
    state='readonly', width=12,
    font=("Trebuchet MS", 10)
)
priority_cb.pack(side='left', ipady=3, padx=(0, 12))

tk.Label(options_row, text="Remind at:",
         font=("Trebuchet MS", 9), fg="#546E85", bg="#162030").pack(side='left')

hour_var   = tk.StringVar(value="--")
minute_var = tk.StringVar(value="--")

hour_cb = ttk.Combobox(options_row, textvariable=hour_var, width=3,
                        state='readonly',
                        values=["--"] + [f"{h:02d}" for h in range(24)])
hour_cb.pack(side='left', padx=(6, 2))

tk.Label(options_row, text=":", fg="#546E85", bg="#162030",
         font=("Trebuchet MS", 11, "bold")).pack(side='left')

minute_cb = ttk.Combobox(options_row, textvariable=minute_var, width=3,
                          state='readonly',
                          values=[f"{m:02d}" for m in range(60)])
minute_cb.pack(side='left', padx=(2, 6))

tk.Label(options_row, text="(24 h)", font=("Trebuchet MS", 8),
         fg="#546E85", bg="#162030").pack(side='left')

add_tsk_btn = tk.Button(
    input_card, text='+ ADD TASK',
    font=("Trebuchet MS", 10, "bold"),
    fg="black", bg="#C5972A", activebackground="#C5972A",
    width=12, height=1,
    command=lambda: ob.add_task(entry.get(),
                                priority_var.get(),
                                hour_var.get(),
                                minute_var.get())
)
add_tsk_btn.pack(padx=6, anchor='w', pady=(0, 4))

# Scrollable task area 
scroll_frame = tk.Frame(root, bg="#162030")
canvas       = tk.Canvas(scroll_frame, bg="#162030", highlightthickness=0)
scrollbar    = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
task_frame   = tk.Frame(canvas, bg="#162030")

canvas_window_id = canvas.create_window((0, 0), window=task_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def _on_task_frame_resize(event):
    canvas.configure(scrollregion=(0, 0, event.width, event.height))
    canvas.configure(height=min(event.height, 380))

task_frame.bind("<Configure>", _on_task_frame_resize)

def _on_canvas_resize(event):
    canvas.itemconfig(canvas_window_id, width=event.width)

canvas.bind("<Configure>", _on_canvas_resize)

def _on_mousewheel(event):
    if os.name == 'nt':
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        canvas.yview_scroll(int(-1 * event.delta), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>",   lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>",   lambda e: canvas.yview_scroll(1,  "units"))

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
scroll_frame.pack(fill="x", padx=100, pady=(0, 4))

ob               = Task(task_frame)
reminder_manager = ReminderManager()

root.protocol("WM_DELETE_WINDOW",
              lambda: [reminder_manager.shutdown(), root.destroy()])

# Task counter 
counter_label = tk.Label(
    root,
    textvariable=ob.counter_var,
    font=("Trebuchet MS", 11, "bold"),
    fg="#C5972A", bg="#162030",
    bd=1, relief="groove",
    highlightthickness=1,
    highlightbackground="#C5972A",
    highlightcolor="#C5972A",
    anchor='w', padx=4, pady=4
)
counter_label.pack(fill='x', padx=100, pady=(10, 0))

tk.Frame(root, height=2, bg="#1E3A52").pack(fill='x', padx=100, pady=(10, 0))

del_tsk_btn = tk.Button(
    root, text="Clear Completed Tasks", width=25,
    command=ob.clear_table,
    fg='#8BAFC8', bg='#1E3A52',
    activebackground='#1E3A52', activeforeground='#c5972A'
)
del_tsk_btn.pack(anchor='nw', pady=10, padx=100)

root.mainloop()
