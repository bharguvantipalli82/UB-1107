# Smart Healthcare Condition Checker

The **Smart Healthcare Condition Checker** is a web-based platform that allows users to input vital health parameters such as sugar level, oxygen level, body temperature, and blood pressure. The system evaluates whether the user is in an emergency condition and provides suggested doctors accordingly. Unlike symptom-based checkers, this platform uses **real-time health values** for accurate risk assessment.

---

## Features

- Enter multiple health parameters (sugar, oxygen, temperature, blood pressure)
- Automatically detects emergency situations
- Suggests relevant doctors or specialists
- User-friendly web interface
- Quick and reliable decision-making

---

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask  
- **Database:** MySQL / SQLite  
- **Logic:** Conditional checks / simple decision-making algorithm  
- **Deployment:** Optional cloud deployment (Heroku / AWS)

---

## System Architecture

```text
+----------------------+        +------------------+       +-------------------+
|     User Interface    | <----> |    Flask Server  | <-->  |  Database (MySQL/SQLite) |
|  (HTML, CSS, JS)     |        |  (Python Logic)  |       |                   |
+----------------------+        +------------------+       +-------------------+
         |                           |
         | Input Health Data         |
         |                           |
         v                           v
  +----------------+          +---------------------+
  | Health Parameter|          | Emergency Check /  |
  |  Entry Form     |          | Doctor Suggestion  |
  +----------------+          +---------------------+
         |                           |
         +----------- Output --------+
drive link:https://drive.google.com/drive/folders/1b0fZQvXcwq-7b0mNGo-bXrbQxUg5RU8C?usp=drive_link
