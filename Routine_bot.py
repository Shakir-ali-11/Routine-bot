import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
import datetime
import json
import re
import os

# ─────────────────────────────────────────────
#  COLOR THEME
# ─────────────────────────────────────────────
BG_DARK      = "#0F1117"
BG_PANEL     = "#1A1D27"
BG_CARD      = "#22263A"
BG_INPUT     = "#2A2F45"
ACCENT       = "#6C63FF"
ACCENT_LIGHT = "#8B85FF"
SUCCESS      = "#00D4A1"
WARNING      = "#FFB347"
DANGER       = "#FF6B6B"
TEXT_PRIMARY = "#EAEAEA"
TEXT_MUTED   = "#7A7F9A"
TEXT_WHITE   = "#FFFFFF"
BORDER       = "#2E3350"

# ─────────────────────────────────────────────
#  DEFAULT SCHEDULE  (24-hr format)
# ─────────────────────────────────────────────
DEFAULT_SCHEDULE = {
    "Fajr Prayer":        {"time": "05:00", "icon": "", "color": SUCCESS,  "tag": "prayer"},
    "Morning Workout":    {"time": "06:30", "icon": "", "color": WARNING,  "tag": "gym"},
    "Breakfast":          {"time": "08:00", "icon": "", "color": "#FF9A9E","tag": "meal"},
    "Study Session":      {"time": "09:00", "icon": "", "color": ACCENT,   "tag": "study"},
    "Dhuhr Prayer":       {"time": "13:00", "icon": "", "color": SUCCESS,  "tag": "prayer"},
    "Lunch":              {"time": "13:30", "icon": "", "color": "#FF9A9E","tag": "meal"},
    "Pending Assignments":{"time": "15:00", "icon": "", "color": DANGER,   "tag": "assignment"},
    "Asr Prayer":         {"time": "16:15", "icon": "", "color": SUCCESS,  "tag": "prayer"},
    "Outdoor Games":      {"time": "17:00", "icon": "", "color": "#43E97B","tag": "outdoor"},
    "Friends Hangout":    {"time": "18:00", "icon": "", "color": "#F093FB","tag": "social"},
    "Maghrib Prayer":     {"time": "18:45", "icon": "", "color": SUCCESS,  "tag": "prayer"},
    "Dinner":             {"time": "20:00", "icon": "", "color": "#FF9A9E","tag": "meal"},
    "Isha Prayer":        {"time": "21:00", "icon": "", "color": SUCCESS,  "tag": "prayer"},
    "Night Study":        {"time": "21:30", "icon": "", "color": ACCENT,   "tag": "study"},
}

# ─────────────────────────────────────────────
#  CHATBOT BRAIN
# ─────────────────────────────────────────────
class ChatBot:
    def __init__(self, schedule):
        self.schedule = schedule
        self.name = "RoutineBot"

    def get_next_task(self):
        now = datetime.datetime.now().strftime("%H:%M")
        upcoming = []
        for task, info in self.schedule.items():
            if info["time"] > now:
                upcoming.append((info["time"], task, info))
        if upcoming:
            upcoming.sort()
            t, task, info = upcoming[0]
            return task, info
        return None, None

    def respond(self, user_input):
        text = user_input.lower().strip()

        greetings = ["hi", "hello", "hey", "salam", "assalam"]
        if any(g in text for g in greetings):
            task, info = self.get_next_task()
            if task:
                return (f"Wa Alaikum Assalam!  I'm {self.name}.\n"
                        f"Your next task is  {info['icon']} {task}  at  {info['time']}.\n"
                        f"Stay on track - you're doing great!")
            return f"Hey there!  I'm {self.name}, your personal routine assistant. How can I help?"

        if any(w in text for w in ["schedule", "today", "plan", "routine", "all tasks"]):
            lines = [f"  {v['icon']}  {k:25s}  ->  {v['time']}" for k, v in
                     sorted(self.schedule.items(), key=lambda x: x[1]["time"])]
            return "Here's your full schedule for today:\n\n" + "\n".join(lines)

        if any(w in text for w in ["next", "upcoming", "what's next", "whats next"]):
            task, info = self.get_next_task()
            if task:
                now = datetime.datetime.now()
                t   = datetime.datetime.strptime(info["time"], "%H:%M").replace(
                          year=now.year, month=now.month, day=now.day)
                diff = int((t - now).total_seconds() / 60)
                return (f"{info['icon']}  Next up: **{task}**\n"
                        f"Time:  {info['time']}  ({diff} minutes from now)\nGet ready!")
            return "All tasks for today are done! Great job - rest well tonight."

        if any(w in text for w in ["prayer", "namaz", "salah", "salat"]):
            prayers = {k: v for k, v in self.schedule.items() if v["tag"] == "prayer"}
            lines   = [f"  {v['icon']}  {k:20s}  ->  {v['time']}" for k, v in
                       sorted(prayers.items(), key=lambda x: x[1]["time"])]
            return "Prayer Schedule:\n\n" + "\n".join(lines) + "\n\nNever miss a prayer!"

        if any(w in text for w in ["meal", "food", "eat", "lunch", "dinner", "breakfast"]):
            meals = {k: v for k, v in self.schedule.items() if v["tag"] == "meal"}
            lines  = [f"  {v['icon']}  {k:20s}  ->  {v['time']}" for k, v in
                      sorted(meals.items(), key=lambda x: x[1]["time"])]
            return "Meal Schedule:\n\n" + "\n".join(lines) + "\n\nEat healthy, stay energized!"

        if any(w in text for w in ["gym", "workout", "exercise", "fitness"]):
            return ("Gym / Workout Time:  06:30 AM\n\n"
                    "Tips for today:\n"
                    "  - Warm up for 10 minutes\n"
                    "  - Stay hydrated\n"
                    "  - Push yourself but listen to your body\n"
                    "  - Track your progress\nLet's get those gains!")

        if any(w in text for w in ["study", "assignment", "homework", "task"]):
            return ("Study Schedule:\n\n"
                    "  Morning Study  ->  09:00 AM\n"
                    "  Pending Work   ->  03:00 PM\n"
                    "  Night Study    ->  09:30 PM\n\n"
                    "Pro tip: Use the Pomodoro technique!\n"
                    "  25 min focus -> 5 min break\nYou've got this!")

        if any(w in text for w in ["friend", "hangout", "social", "chill", "meet"]):
            return ("Friends Hangout:  06:00 PM\n\n"
                    "Social connections are important!\n"
                    "  - Plan something fun\n"
                    "  - Be present, put the phone away\n"
                    "  - Make memories!\nEnjoy your time!")

        if any(w in text for w in ["outdoor", "game", "play", "sport", "football", "cricket"]):
            return ("Outdoor Games:  05:00 PM\n\n"
                    "Get outside and move!\n"
                    "  - Fresh air is good for focus\n"
                    "  - Team sports build character\n"
                    "  - Stay active, stay healthy\nHave fun out there!")

        if any(w in text for w in ["time", "now", "current", "clock"]):
            now = datetime.datetime.now()
            return (f"Current Time:  {now.strftime('%I:%M %p')}\n"
                    f"Date:  {now.strftime('%A, %d %B %Y')}")

        if any(w in text for w in ["help", "what can you do", "commands"]):
            return ("I can help you with:\n\n"
                    "  'schedule'     - View full daily routine\n"
                    "  'next'         - What's coming up next\n"
                    "  'prayer'       - Prayer timings\n"
                    "  'meal'         - Meal timings\n"
                    "  'gym'          - Workout info\n"
                    "  'study'        - Study schedule\n"
                    "  'friends'      - Hangout time\n"
                    "  'outdoor'      - Games time\n"
                    "  'time'         - Current time\n\n"
                    "Just type naturally - I'll understand!")

        if any(w in text for w in ["bye", "goodbye", "exit", "quit", "later"]):
            return "Take care! Stay consistent with your routine.\nSee you soon!"

        if any(w in text for w in ["motivat", "inspire", "encourage", "sad", "lazy", "tired"]):
            quotes = [
                "'Discipline is the bridge between goals and accomplishment.' - Jim Rohn",
                "'Small daily improvements are the key to staggering long-term results.'",
                "'The secret to your future is hidden in your daily routine.'",
                "'You don't have to be great to start, but you have to start to be great.'",
                "'Motivation gets you started. Habit keeps you going.'"
            ]
            import random
            return random.choice(quotes) + "\n\nYou've got this!"

        return ("I didn't quite catch that.\nTry asking about:\n"
                "  - 'schedule', 'next task', 'prayer times'\n"
                "  - 'meals', 'gym', 'study', 'friends'\n"
                "  - Type 'help' for all commands")


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class RoutineBotApp:
    def __init__(self, root):
        self.root      = root
        self.schedule  = DEFAULT_SCHEDULE.copy()
        self.bot       = ChatBot(self.schedule)
        self.notified  = set()
        self.running   = True

        self._setup_window()
        self._build_ui()
        self._start_reminder_thread()
        self._welcome_message()

    # ── Window setup ──
    def _setup_window(self):
        self.root.title("RoutineBot - Your Smart Daily Planner")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_DARK)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        try:
            self.root.iconbitmap("")
        except Exception:
            pass

    # ── Full UI ──
    def _build_ui(self):
        # ── Top bar ──
        topbar = tk.Frame(self.root, bg=BG_PANEL, height=62)
        topbar.pack(fill=tk.X, side=tk.TOP)
        topbar.pack_propagate(False)

        tk.Label(topbar, text="", font=("Segoe UI Emoji", 22),
                 bg=BG_PANEL, fg=ACCENT).pack(side=tk.LEFT, padx=(18, 6), pady=12)
        tk.Label(topbar, text="RoutineBot", font=("Segoe UI", 16, "bold"),
                 bg=BG_PANEL, fg=TEXT_WHITE).pack(side=tk.LEFT)
        tk.Label(topbar, text="Your Smart Daily Planner",
                 font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MUTED).pack(side=tk.LEFT, padx=(8, 0))

        self.clock_lbl = tk.Label(topbar, text="", font=("Segoe UI", 11, "bold"),
                                   bg=BG_PANEL, fg=ACCENT_LIGHT)
        self.clock_lbl.pack(side=tk.RIGHT, padx=20)
        self._update_clock()

        # ── Body ──
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True)

        # Left sidebar
        self._build_sidebar(body)

        # Chat area
        self._build_chat(body)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_PANEL, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Today's Schedule",
                 font=("Segoe UI", 11, "bold"), bg=BG_PANEL, fg=TEXT_WHITE,
                 anchor="w").pack(fill=tk.X, padx=14, pady=(14, 6))

        sep = tk.Frame(sidebar, bg=BORDER, height=1)
        sep.pack(fill=tk.X, padx=12, pady=(0, 8))

        # Scrollable task list
        container = tk.Frame(sidebar, bg=BG_PANEL)
        container.pack(fill=tk.BOTH, expand=True, padx=8)

        canvas = tk.Canvas(container, bg=BG_PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.task_frame = tk.Frame(canvas, bg=BG_PANEL)

        self.task_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._populate_tasks()

        # Add task button
        add_btn = tk.Button(sidebar, text="Add Reminder",
                            font=("Segoe UI", 10, "bold"),
                            bg=ACCENT, fg=TEXT_WHITE, relief=tk.FLAT,
                            activebackground=ACCENT_LIGHT, cursor="hand2",
                            command=self._open_add_task)
        add_btn.pack(fill=tk.X, padx=12, pady=(8, 12), ipady=8)

    def _populate_tasks(self):
        for w in self.task_frame.winfo_children():
            w.destroy()

        now = datetime.datetime.now().strftime("%H:%M")
        sorted_tasks = sorted(self.schedule.items(), key=lambda x: x[1]["time"])

        for task, info in sorted_tasks:
            done = info["time"] < now
            card = tk.Frame(self.task_frame, bg=BG_CARD if not done else BG_INPUT,
                            cursor="hand2")
            card.pack(fill=tk.X, pady=2, padx=2)

            # Color accent bar
            tk.Frame(card, bg=info["color"] if not done else TEXT_MUTED,
                     width=4).pack(side=tk.LEFT, fill=tk.Y)

            inner = tk.Frame(card, bg=BG_CARD if not done else BG_INPUT)
            inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=6)

            top_row = tk.Frame(inner, bg=BG_CARD if not done else BG_INPUT)
            top_row.pack(fill=tk.X)

            tk.Label(top_row, text=info["icon"],
                     font=("Segoe UI Emoji", 13),
                     bg=BG_CARD if not done else BG_INPUT,
                     fg=info["color"] if not done else TEXT_MUTED).pack(side=tk.LEFT)

            tk.Label(top_row, text=task,
                     font=("Segoe UI", 9, "bold" if not done else "normal"),
                     bg=BG_CARD if not done else BG_INPUT,
                     fg=TEXT_PRIMARY if not done else TEXT_MUTED,
                     anchor="w").pack(side=tk.LEFT, padx=(4, 0))

            tk.Label(inner,
                     text=datetime.datetime.strptime(info["time"], "%H:%M").strftime("%I:%M %p"),
                     font=("Segoe UI", 8),
                     bg=BG_CARD if not done else BG_INPUT,
                     fg=info["color"] if not done else TEXT_MUTED,
                     anchor="w").pack(fill=tk.X)

            if done:
                tk.Label(inner, text="Done",
                         font=("Segoe UI", 7), bg=BG_INPUT,
                         fg=SUCCESS).pack(anchor="w")

    def _build_chat(self, parent):
        chat_outer = tk.Frame(parent, bg=BG_DARK)
        chat_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                        padx=10, pady=10)

        # Chat header
        chat_header = tk.Frame(chat_outer, bg=BG_PANEL, height=46)
        chat_header.pack(fill=tk.X)
        chat_header.pack_propagate(False)

        self.status_dot = tk.Label(chat_header, text="|", font=("Segoe UI", 10),
                                    bg=BG_PANEL, fg=SUCCESS)
        self.status_dot.pack(side=tk.LEFT, padx=(14, 4))
        tk.Label(chat_header, text="Online - Ready to assist",
                 font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_MUTED).pack(side=tk.LEFT)

        clr_btn = tk.Button(chat_header, text="Clear Chat",
                             font=("Segoe UI", 9), bg=BG_PANEL, fg=TEXT_MUTED,
                             relief=tk.FLAT, activebackground=BG_CARD,
                             cursor="hand2", command=self._clear_chat, bd=0)
        clr_btn.pack(side=tk.RIGHT, padx=12)

        # ── Pack BOTTOM elements FIRST so chat_display fills remaining space ──

        # Input bar
        input_bar = tk.Frame(chat_outer, bg=BG_PANEL, height=54)
        input_bar.pack(side=tk.BOTTOM, fill=tk.X)
        input_bar.pack_propagate(False)

        self.msg_entry = tk.Entry(
            input_bar,
            font=("Segoe UI", 12),
            bg=BG_INPUT, fg=TEXT_WHITE,
            relief=tk.FLAT, bd=0,
            insertbackground=ACCENT_LIGHT,
            selectbackground=ACCENT,
            selectforeground=TEXT_WHITE,
            highlightthickness=2,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                            padx=(12, 6), pady=10)
        self.msg_entry.bind("<Return>", lambda e: self._send_message())
        self.msg_entry.insert(0, "Type your message here...")
        self.msg_entry.config(fg=TEXT_MUTED)
        self.msg_entry.bind("<FocusIn>",  self._on_entry_focus)
        self.msg_entry.bind("<FocusOut>", self._on_entry_unfocus)

        send_btn = tk.Button(
            input_bar, text="Send  ->",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg=TEXT_WHITE,
            relief=tk.FLAT, bd=0,
            activebackground=ACCENT_LIGHT,
            activeforeground=TEXT_WHITE,
            cursor="hand2",
            command=self._send_message
        )
        send_btn.pack(side=tk.RIGHT, padx=(0, 12), pady=10, ipadx=16, ipady=4)

        # Quick-action chips (above input bar)
        chips_bar = tk.Frame(chat_outer, bg=BG_DARK)
        chips_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(2, 2))

        chip_data = [
            ("Schedule", "show my schedule"),
            ("Next Task", "what's next"),
            ("Prayers",  "prayer times"),
            ("Meals",    "meal times"),
            ("Gym",      "gym time"),
            ("Study",    "study schedule"),
        ]
        for label, cmd in chip_data:
            btn = tk.Button(chips_bar, text=label,
                            font=("Segoe UI", 9),
                            bg=BG_CARD, fg=TEXT_MUTED, relief=tk.FLAT,
                            activebackground=BG_INPUT, activeforeground=TEXT_WHITE,
                            cursor="hand2", bd=0,
                            command=lambda c=cmd: self._quick_send(c))
            btn.pack(side=tk.LEFT, padx=3, pady=4, ipadx=8, ipady=4)

        # Message display - fills all remaining space
        self.chat_display = tk.Text(
            chat_outer, state=tk.DISABLED,
            bg=BG_DARK, fg=TEXT_PRIMARY,
            font=("Consolas", 11), relief=tk.FLAT,
            padx=16, pady=12, wrap=tk.WORD,
            cursor="arrow", spacing1=4, spacing3=4
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        scrollbar = tk.Scrollbar(self.chat_display)
        self.chat_display.configure(yscrollcommand=scrollbar.set)

        # Tag styles
        self.chat_display.tag_configure("bot_name",   foreground=ACCENT,       font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("bot_msg",    foreground=TEXT_PRIMARY,  font=("Consolas", 11))
        self.chat_display.tag_configure("user_name",  foreground=SUCCESS,       font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("user_msg",   foreground="#C9F0E3",     font=("Consolas", 11))
        self.chat_display.tag_configure("time_stamp", foreground=TEXT_MUTED,    font=("Segoe UI", 8))
        self.chat_display.tag_configure("divider",    foreground=BORDER)
        self.chat_display.tag_configure("reminder",   foreground=WARNING,       font=("Segoe UI", 11, "bold"))

    # ── Messages ──
    def _welcome_message(self):
        now  = datetime.datetime.now()
        hour = now.hour
        if hour < 12:
            greet = "Good Morning"
        elif hour < 17:
            greet = "Good Afternoon"
        else:
            greet = "Good Evening"

        msg = (f"{greet}! I'm RoutineBot\n"
               f"Today is {now.strftime('%A, %d %B %Y')}\n\n"
               f"I'm here to keep your daily routine on track.\n"
               f"Type 'help' to see what I can do, or ask me anything!")
        self._append_bot(msg)

    def _append_bot(self, msg):
        self.chat_display.config(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\nRoutineBot  ", "bot_name")
        self.chat_display.insert(tk.END, f"[{ts}]\n", "time_stamp")
        self.chat_display.insert(tk.END, f"{msg}\n", "bot_msg")
        self.chat_display.insert(tk.END, "─" * 55 + "\n", "divider")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_user(self, msg):
        self.chat_display.config(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(tk.END, f"\nYou  ", "user_name")
        self.chat_display.insert(tk.END, f"[{ts}]\n", "time_stamp")
        self.chat_display.insert(tk.END, f"{msg}\n", "user_msg")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_reminder(self, msg):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{msg}\n", "reminder")
        self.chat_display.insert(tk.END, "─" * 55 + "\n", "divider")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _send_message(self):
        msg = self.msg_entry.get().strip()
        if not msg or msg == "Type your message here...":
            return
        self._append_user(msg)
        self.msg_entry.delete(0, tk.END)
        response = self.bot.respond(msg)
        self.root.after(400, lambda: self._append_bot(response))

    def _quick_send(self, cmd):
        self._append_user(cmd)
        response = self.bot.respond(cmd)
        self.root.after(300, lambda: self._append_bot(response))

    def _clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._welcome_message()

    # ── Entry placeholder ──
    def _on_entry_focus(self, event):
        if self.msg_entry.get() == "Type your message here...":
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.config(fg=TEXT_WHITE)

    def _on_entry_unfocus(self, event):
        if not self.msg_entry.get():
            self.msg_entry.insert(0, "Type your message here...")
            self.msg_entry.config(fg=TEXT_MUTED)

    # ── Clock ──
    def _update_clock(self):
        now = datetime.datetime.now().strftime("%I:%M:%S %p  |  %a %d %b")
        self.clock_lbl.config(text=now)
        self.root.after(1000, self._update_clock)

    # ── Add task dialog ──
    def _open_add_task(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Reminder")
        dialog.geometry("360x280")
        dialog.configure(bg=BG_PANEL)
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="New Reminder",
                 font=("Segoe UI", 13, "bold"), bg=BG_PANEL, fg=TEXT_WHITE
                 ).pack(pady=(18, 12))

        fields = tk.Frame(dialog, bg=BG_PANEL)
        fields.pack(padx=24, fill=tk.X)

        tk.Label(fields, text="Task Name:", font=("Segoe UI", 10),
                 bg=BG_PANEL, fg=TEXT_MUTED, anchor="w").pack(fill=tk.X, pady=(0, 3))
        name_var = tk.StringVar()
        tk.Entry(fields, textvariable=name_var, font=("Segoe UI", 11),
                 bg=BG_INPUT, fg=TEXT_WHITE, relief=tk.FLAT,
                 insertbackground=ACCENT).pack(fill=tk.X, ipady=6, pady=(0, 10))

        tk.Label(fields, text="Time (HH:MM - 24hr):", font=("Segoe UI", 10),
                 bg=BG_PANEL, fg=TEXT_MUTED, anchor="w").pack(fill=tk.X, pady=(0, 3))
        time_var = tk.StringVar(value="12:00")
        tk.Entry(fields, textvariable=time_var, font=("Segoe UI", 11),
                 bg=BG_INPUT, fg=TEXT_WHITE, relief=tk.FLAT,
                 insertbackground=ACCENT).pack(fill=tk.X, ipady=6)

        def save():
            name = name_var.get().strip()
            t    = time_var.get().strip()
            if not name:
                messagebox.showwarning("Missing", "Please enter a task name.", parent=dialog)
                return
            try:
                datetime.datetime.strptime(t, "%H:%M")
            except ValueError:
                messagebox.showwarning("Invalid", "Use HH:MM format (e.g. 14:30).", parent=dialog)
                return
            self.schedule[name] = {"time": t, "icon": "", "color": ACCENT, "tag": "custom"}
            self.bot.schedule    = self.schedule
            self._populate_tasks()
            self._append_bot(f"Reminder added!\n{name}  ->  {t}\nI'll remind you on time!")
            dialog.destroy()

        tk.Button(dialog, text="Save Reminder",
                  font=("Segoe UI", 11, "bold"), bg=ACCENT, fg=TEXT_WHITE,
                  relief=tk.FLAT, activebackground=ACCENT_LIGHT,
                  cursor="hand2", command=save).pack(pady=18, ipadx=20, ipady=6)

    # ── Reminder thread ──
    def _start_reminder_thread(self):
        t = threading.Thread(target=self._reminder_loop, daemon=True)
        t.start()

    def _reminder_loop(self):
        while self.running:
            now = datetime.datetime.now().strftime("%H:%M")
            day = datetime.datetime.now().strftime("%Y-%m-%d")

            for task, info in self.schedule.items():
                key = f"{day}_{task}"
                if info["time"] == now and key not in self.notified:
                    self.notified.add(key)
                    msg = (f"REMINDER  ─────────────────────\n"
                           f"  {info['icon']}  Time for:  {task}\n"
                           f"  {datetime.datetime.now().strftime('%I:%M %p')}\n"
                           f"─────────────────────────────────────")
                    self.root.after(0, lambda m=msg: self._append_reminder(m))
                    self.root.after(0, lambda t=task, i=info: self._show_popup(t, i))
                    self.root.after(0, self._populate_tasks)

            time.sleep(30)

    def _show_popup(self, task, info):
        popup = tk.Toplevel(self.root)
        popup.title("Reminder!")
        popup.geometry("340x160")
        popup.configure(bg=BG_PANEL)
        popup.resizable(False, False)
        popup.attributes("-topmost", True)

        tk.Label(popup, text="Reminder!",
                 font=("Segoe UI", 14, "bold"), bg=BG_PANEL,
                 fg=info["color"]).pack(pady=(22, 6))
        tk.Label(popup, text=f"Time for:  {task}",
                 font=("Segoe UI", 12), bg=BG_PANEL,
                 fg=TEXT_WHITE).pack()
        tk.Label(popup, text=datetime.datetime.now().strftime("%I:%M %p"),
                 font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MUTED).pack(pady=(4, 12))

        tk.Button(popup, text="Got it!",
                  font=("Segoe UI", 10, "bold"), bg=ACCENT, fg=TEXT_WHITE,
                  relief=tk.FLAT, cursor="hand2",
                  command=popup.destroy).pack(ipadx=20, ipady=6)

        popup.after(12000, lambda: popup.destroy() if popup.winfo_exists() else None)

    def _on_close(self):
        self.running = False
        self.root.destroy()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = RoutineBotApp(root)
    root.mainloop()
