import tkinter as tk
import os
from datetime import datetime, timedelta
from theme import COLORS, FONTS, PRIORITY_CONFIG

class Task:
    def __init__(self, frame, reminder_manager, update_counter_callback=None):
        self.frame = frame
        self.reminder_manager = reminder_manager
        self.update_counter_callback = update_counter_callback
        
        self.tasks = []
        self.priorities = []
        self.vars = []
        self.checkbuttons = []

        self.completed_tasks = []
        self.completed_priorities = []
        self.completed_vars = []
        self.completed_checkbuttons = []

        self.counter_var = tk.StringVar(value="0 / 0 Tasks Completed")

        # Pending section card
        self.pending_frame = tk.Frame(frame, bg=COLORS["card_bg"], pady=10, padx=10)
        self.pending_frame.pack(anchor='w', fill='x', pady=5)
        tk.Label(
            self.pending_frame, text="Pending Tasks",
            font=FONTS["h2"],
            fg=COLORS["accent_primary"], bg=COLORS["card_bg"]
        ).pack(anchor='center', fill='x', pady=(0, 10))

        # Completed section card
        self.completed_frame = tk.Frame(frame, bg=COLORS["card_bg"], pady=10, padx=10)
        self.completed_frame.pack(anchor='w', fill='x', pady=5)
        tk.Label(
            self.completed_frame,
            text="Completed Tasks",
            font=FONTS["h2"],
            fg=COLORS["text_muted"], bg=COLORS["card_bg"]
        ).pack(anchor='center', fill='x', pady=(0, 10))

        if os.path.exists('userInterface/tasks.txt'):
            raw_tasks, raw_pris = [], []
            with open('userInterface/tasks.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if '||' in line:
                        pri, title = line.split('||', 1)
                        if pri == "🔴 High": pri = "High"
                        elif pri == "🟡 Medium": pri = "Medium"
                        elif pri == "🔵 Low": pri = "Low"
                        pri = pri if pri in PRIORITY_CONFIG else "Medium"
                    else:
                        pri, title = "Medium", line
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
                    text=f"{title}",
                    variable=var,
                    fg=color, bg=COLORS["card_bg"],
                    activebackground=COLORS["card_bg"], activeforeground=color,
                    selectcolor=COLORS["bg"],
                    command=self.mark_completed,
                    anchor='w', font=FONTS["body_bold"]
                )
                cb.pack(anchor='w', fill='x', padx=6, pady=4)
                self.checkbuttons.append(cb)

        self.update_counter()
        
    def add_task(self, task_str, priority="Medium", hour="--", minute="--"):
        task_str = task_str.strip()
        if not task_str or task_str == "Enter task details...":
            return False
        if priority not in PRIORITY_CONFIG:
            priority = "Medium"

        # Ensure directory exists or file can be created
        os.makedirs('userInterface', exist_ok=True)
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
            text=f"{task_str}",
            variable=var,
            fg=color, bg=COLORS["card_bg"],
            activebackground=COLORS["card_bg"], activeforeground=color,
            selectcolor=COLORS["bg"],
            command=self.mark_completed,
            anchor='w', font=FONTS["body_bold"]
        )
        cb.pack(anchor='w', fill='x', padx=6, pady=4)
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
                    cb_ref.config(fg=COLORS["accent_high"])
                except tk.TclError:
                    pass

            self.reminder_manager.add_reminder(task_str, due_dt, on_due_callback=on_due)

        self.update_counter()
        return True

    def mark_completed(self):
        to_move = [i for i, v in enumerate(self.vars) if v.get() == 1]
        for i in reversed(to_move):
            task     = self.tasks.pop(i)
            priority = self.priorities.pop(i)
            var      = self.vars.pop(i)
            cb       = self.checkbuttons.pop(i)
            cb.destroy()

            self.reminder_manager.remove_reminder(task)

            self.completed_tasks.append(task)
            self.completed_priorities.append(priority)
            self.completed_vars.append(var)

            cb_done = tk.Checkbutton(
                self.completed_frame,
                text=f"{task}",
                font=FONTS["body_strike"],
                anchor='w', variable=var,
                fg=COLORS["text_muted"], bg=COLORS["card_bg"],
                activebackground=COLORS["card_bg"],
                selectcolor=COLORS["bg"],
                command=self.unmark_completed
            )
            cb_done.pack(anchor='w', fill='x', padx=6, pady=4)
            self.completed_checkbuttons.append(cb_done)
        self.update_counter()

    def unmark_completed(self):
        to_move = [i for i, v in enumerate(self.completed_vars) if v.get() == 0]
        for i in reversed(to_move):
            task = self.completed_tasks.pop(i)
            priority = self.completed_priorities.pop(i)
            var  = self.completed_vars.pop(i)
            cb   = self.completed_checkbuttons.pop(i)
            cb.destroy()

            order     = PRIORITY_CONFIG[priority]["order"]
            insert_at = len(self.tasks)
            for j, p in enumerate(self.priorities):
                if PRIORITY_CONFIG[p]["order"] > order:
                    insert_at = j
                    break

            self.tasks.insert(insert_at, task)
            self.priorities.insert(insert_at, priority)
            self.vars.insert(insert_at, var)

            color = PRIORITY_CONFIG[priority]["fg"]
            cb_pending = tk.Checkbutton(
                self.pending_frame,
                text=f"{task}",
                variable=var,
                fg=color, bg=COLORS["card_bg"],
                activebackground=COLORS["card_bg"], activeforeground=color,
                selectcolor=COLORS["bg"],
                command=self.mark_completed,
                anchor='w', font=FONTS["body_bold"]
            )
            cb_pending.pack(anchor='w', fill='x', padx=6, pady=4)
            self.checkbuttons.insert(insert_at, cb_pending)
            self._repack_pending()
        self.update_counter()

    def clear_table(self):
        keep_tasks, keep_pris, keep_vars, keep_cbs = [], [], [], []
        for task, pri, var, cb in zip(
                self.completed_tasks, self.completed_priorities,
                self.completed_vars, self.completed_checkbuttons):
            if var.get() == 1:
                cb.destroy()
            else:
                keep_tasks.append(task)
                keep_pris.append(pri)
                keep_vars.append(var)
                keep_cbs.append(cb)

        self.completed_tasks        = keep_tasks
        self.completed_priorities   = keep_pris
        self.completed_vars         = keep_vars
        self.completed_checkbuttons = keep_cbs

        os.makedirs('userInterface', exist_ok=True)
        with open('userInterface/tasks.txt', 'w', encoding='utf-8') as f:
            for task, pri in zip(self.tasks, self.priorities):
                f.write(f"{pri}||{task}\n")
            for task, pri in zip(self.completed_tasks, self.completed_priorities):
                f.write(f"{pri}||{task}\n")

        self.update_counter()

    def _repack_pending(self):
        for cb in self.checkbuttons:
            cb.pack_forget()
        for cb in self.checkbuttons:
            cb.pack(anchor='w', fill='x', padx=6, pady=4)

    def update_counter(self):
        total = len(self.tasks) + len(self.completed_tasks)
        done  = len(self.completed_tasks)
        self.counter_var.set(f"{done} / {total} Tasks Completed")
        if self.update_counter_callback:
            self.update_counter_callback()
