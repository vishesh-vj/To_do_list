import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

try:
    from plyer import notification as plyer_notify
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


class ReminderManager:
    def __init__(self, root):
        self.root = root
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
                self.root.after(0, lambda t=title, ts=time_str:
                    messagebox.showinfo("Task Due", f'"{t}" was due at {ts}'))
            except Exception:
                pass
