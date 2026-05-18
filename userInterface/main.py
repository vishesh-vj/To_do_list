import tkinter as tk
from tkinter import ttk
import os
from time import strftime

from theme import COLORS, FONTS, PRIORITY_LABELS
from reminders import ReminderManager
from task_manager import Task

def update_time(date_label, time_label):
    date_label.config(text=strftime('%Y-%m-%d'))
    time_label.config(text=strftime('%H:%M:%S'))
    date_label.after(1000, lambda: update_time(date_label, time_label))

def main():
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry('550x850')
    root.resizable(True, True)
    root.configure(background=COLORS["bg"])

    reminder_manager = ReminderManager(root)
    
    root.protocol("WM_DELETE_WINDOW", lambda: [reminder_manager.shutdown(), root.destroy()])

    # Header
    header_frame = tk.Frame(root, bg=COLORS["bg"])
    header_frame.pack(fill='x', padx=20, pady=(15, 5))

    tk.Label(
        header_frame, text='Task Manager',
        fg=COLORS["accent_primary"], bg=COLORS["bg"],
        font=FONTS["h1"], anchor='w'
    ).pack(side='left')

    clock_frame = tk.Frame(header_frame, bg=COLORS["bg"])
    clock_frame.pack(side='right', anchor='e', pady=(10, 0))

    date_label = tk.Label(clock_frame, font=FONTS["body_bold"],
                          fg=COLORS["text_muted"], bg=COLORS["bg"], anchor='e')
    date_label.pack(anchor='e')

    time_label = tk.Label(clock_frame, font=FONTS["h2"],
                          fg=COLORS["accent_primary"], bg=COLORS["bg"], anchor='e')
    time_label.pack(anchor='e')

    update_time(date_label, time_label)

    tk.Label(root, text="Organize your day with elegance.",
             font=FONTS["body"], fg=COLORS["accent_primary"], bg=COLORS["bg"], padx=25).pack(anchor="w")
    tk.Frame(root, height=3, bg=COLORS["separator"]).pack(fill='x', pady=5)

    # Input Section
    input_card = tk.Frame(root, bd=0, bg=COLORS["card_bg"], pady=12, padx=12, highlightthickness=2, highlightbackground=COLORS["accent_primary"])
    input_card.pack(fill="x", padx=40, pady=(15, 10))

    tk.Label(input_card, text='New Task', font=FONTS["h2"],
             fg=COLORS["text_main"], bg=COLORS["card_bg"], anchor='w').pack(fill='x', padx=6, pady=(0, 5))

    entry_wrap = tk.Frame(input_card, bg=COLORS["bg"], highlightthickness=2, highlightbackground=COLORS["separator"])
    entry_wrap.pack(fill='x', padx=6, pady=(0, 10), anchor='w')

    entry = tk.Entry(entry_wrap, bd=0, font=FONTS["body"], width=150,
                     background=COLORS["bg"], fg=COLORS["text_muted"], insertbackground=COLORS["accent_primary"])
    entry.pack(ipady=10, fill='x', padx=5)
    entry.insert(0, "Enter task details...")

    def _focus_in(e):
        if entry.get() == "Enter task details...":
            entry.delete(0, tk.END)
            entry.config(fg=COLORS["accent_primary"])
        entry_wrap.config(highlightbackground=COLORS["accent_primary"])

    def _focus_out(e):
        if not entry.get().strip():
            entry.insert(0, "Enter task details...")
            entry.config(fg=COLORS["text_muted"])
        entry_wrap.config(highlightbackground=COLORS["separator"])

    entry.bind("<FocusIn>",  _focus_in)
    entry.bind("<FocusOut>", _focus_out)

    options_row = tk.Frame(input_card, bg=COLORS["card_bg"])
    options_row.pack(fill='x', padx=6, pady=(0, 10))

    # Priority dropdown
    priority_var = tk.StringVar(value="Medium")
    
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TCombobox", fieldbackground=COLORS["bg"], background=COLORS["separator"], foreground="black")

    priority_cb  = ttk.Combobox(
        options_row, textvariable=priority_var,
        values=PRIORITY_LABELS,
        state='readonly', width=12,
        font=FONTS["small"]
    )
    priority_cb.pack(side='left', ipady=4, padx=(0, 12))

    tk.Label(options_row, text="Remind at:",
             font=FONTS["small"], fg=COLORS["text_muted"], bg=COLORS["card_bg"]).pack(side='left')

    hour_var   = tk.StringVar(value="--")
    minute_var = tk.StringVar(value="--")

    hour_cb = ttk.Combobox(options_row, textvariable=hour_var, width=3, state='readonly',
                            values=["--"] + [f"{h:02d}" for h in range(24)])
    hour_cb.pack(side='left', padx=(6, 2))

    tk.Label(options_row, text=":", fg=COLORS["text_muted"], bg=COLORS["card_bg"],
             font=FONTS["body_bold"]).pack(side='left')

    minute_cb = ttk.Combobox(options_row, textvariable=minute_var, width=3, state='readonly',
                              values=[f"{m:02d}" for m in range(60)])
    minute_cb.pack(side='left', padx=(2, 6))

    def on_add_task():
        success = ob.add_task(entry.get(), priority_var.get(), hour_var.get(), minute_var.get())
        if success:
            entry.delete(0, tk.END)
            priority_var.set("Medium")
            hour_var.set("--")
            minute_var.set("--")

    entry.bind("<Return>", lambda e: on_add_task())

    add_tsk_btn = tk.Button(
        input_card, text='Add Task',
        font=FONTS["h2"],
        fg=COLORS["bg"], bg=COLORS["accent_primary"], activebackground=COLORS["accent_high"], activeforeground=COLORS["bg"],
        width=12, height=1, bd=0, cursor="hand2",
        command=on_add_task
    )
    add_tsk_btn.pack(padx=6, anchor='w', pady=(0, 4))

    # Scrollable task area 
    scroll_frame = tk.Frame(root, bg=COLORS["bg"])
    canvas       = tk.Canvas(scroll_frame, bg=COLORS["bg"], highlightthickness=0)
    scrollbar    = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    task_frame   = tk.Frame(canvas, bg=COLORS["bg"])

    canvas_window_id = canvas.create_window((0, 0), window=task_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_task_frame_resize(event):
        canvas.configure(scrollregion=(0, 0, event.width, event.height))
        # canvas.configure(height=min(event.height, 400)) # let pack expand handle it

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
    scroll_frame.pack(fill="both", expand=True, padx=40, pady=(0, 4))

    ob = Task(task_frame, reminder_manager)

    # Task counter 
    counter_label = tk.Label(
        root,
        textvariable=ob.counter_var,
        font=FONTS["h2"],
        fg=COLORS["accent_primary"], bg=COLORS["bg"],
        anchor='w', padx=4, pady=10
    )
    counter_label.pack(fill='x', padx=40, side='top')

    tk.Frame(root, height=3, bg=COLORS["separator"]).pack(fill='x', padx=40)

    del_tsk_btn = tk.Button(
        root, text="Clear Completed", width=20,
        font=FONTS["body_bold"],
        command=ob.clear_table,
        fg=COLORS["bg"], bg=COLORS["separator"],
        activebackground=COLORS["accent_high"], activeforeground=COLORS["bg"],
        bd=0, cursor="hand2"
    )
    del_tsk_btn.pack(anchor='w', pady=15, padx=40)

    root.mainloop()

if __name__ == "__main__":
    main()
