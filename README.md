# RoutineBot – Personal Routine Chatbot (Python + Tkinter)

RoutineBot is a desktop application built with Python and Tkinter that acts as your personal routine assistant. It shows your daily schedule, sends pop‑up reminders, and lets you chat in natural language about your day (prayers, study, meals, gym, friends, etc.).  

This project is part of my portfolio and demonstrates GUI development, threading, and basic rule‑based chatbot logic in Python.

---

## Demo

Watch a short demo of RoutineBot in action:

👉 **Demo video (Google Drive):**  
https://drive.google.com/file/d/1eiGq8P5Y2lkTGP977Y3btoJI3Ra2fdXC/view?usp=drivesdk

If the link does not open, please make sure “Anyone with the link” has **Viewer** access in Google Drive settings.

---

## Features

- Modern dark UI built with **Tkinter**
- Sidebar showing **Today’s Schedule** with completed vs upcoming tasks
- **Chatbot interface** for asking about:
  - Full schedule  
  - Next upcoming task  
  - Prayer times  
  - Meals (breakfast, lunch, dinner)  
  - Gym / workout time  
  - Study sessions and assignments  
  - Friends hangout and outdoor games  
  - Current time and date  
- **Smart reminders**:
  - Background thread checks times every few seconds
  - In‑app reminder messages
  - Pop‑up reminder windows for each task
- **Add custom reminders** via a dialog (task name + 24‑hour time)
- Motivational quotes when you feel tired or unmotivated
- Single‑file Python implementation that is easy to read and extend

These sections follow common structure used in good open‑source Tkinter project READMEs.

---

## Tech Stack

- Python 3.x
- Tkinter (standard library GUI toolkit)
- threading, datetime, time, random, json, os (Python standard library)

No external third‑party libraries are required beyond a standard Python installation.

---

## Getting Started

### Prerequisites

- Python 3.x installed on your system  
- OS: Windows / Linux / macOS (Tkinter is available on all major platforms)

You can optionally create a virtual environment, but it is not strictly required for this project.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Shakir-ali-11/Routine-bot.git
cd Routine-bot

# (Optional) Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate

# Install dependencies (if you add any in the future)
pip install -r requirements.txt
```

If you are only using Python standard library modules (Tkinter, datetime, etc.), `requirements.txt` can be minimal or even empty, but it is kept for future extension.

---

## Usage

Run the main application file:

```bash
python Routine_bot.py
```

When the app starts:

- You’ll see the main window with:
  - Top bar (title and live clock)
  - Left sidebar with **Today’s Schedule**
  - Right side chat window
- Type messages like:
  - `hi` / `hello` / `assalam`  
  - `show my schedule`  
  - `what's next`  
  - `prayer times`  
  - `meal times`  
  - `gym time`  
  - `study schedule`  
  - `time`  
  - `help`  

You can also use the quick buttons at the bottom (Schedule, Next Task, Prayers, Meals, Gym, Study) to send predefined queries.

---

## Project Structure

```text
Routine-bot/
├── Routine_bot.py            # Main application (Tkinter GUI + ChatBot logic)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies (optional / future use)
└── .gitignore                # Git ignore rules for Python
```

A clear folder layout like this is considered good practice for Python GUI projects.

---

## How It Works (High Level)

- **ChatBot class**
  - Holds a schedule dictionary with tasks, times, tags, and colors.
  - Parses user input with simple keyword checks.
  - Responds with:
    - Full schedule view
    - Next task and time difference in minutes
    - Filtered views (prayers, meals, study, social, outdoor, gym)
    - Motivational quotes and help commands

- **RoutineBotApp (Tkinter GUI)**
  - Builds a modern two‑panel layout (schedule + chat).
  - Shows tasks in cards with time and status (Done vs upcoming).
  - Handles sending and displaying chat messages.
  - Runs a background thread that:
    - Checks the current time
    - Triggers in‑app reminders
    - Opens reminder pop‑ups
    - Refreshes task status visually

Separating chatbot logic from GUI logic is a common pattern in Tkinter applications and makes future changes easier.

---

## Future Improvements

Some ideas for future work:

- Save and load schedule from a JSON or database file (so custom reminders persist)
- Allow editing and deleting existing tasks
- Support multiple daily profiles (weekday vs weekend)
- Settings panel for custom colors and notification options
- Export schedule to CSV / PDF

Including a “Future Improvements” list is a common way to show planning and growth potential in portfolio projects.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Author

**Shakir Ali**  
Personal routine chatbot project for learning and portfolio purposes.
