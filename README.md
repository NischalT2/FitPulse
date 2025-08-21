# FitPulse

**FitPulse** is a full-stack web application that helps users track their **fitness journey, goals, challenges, nutrition, and progress**.

Within the webpage, users can:
- Set fitness goals with **personalized plans**
- Log **daily nutrition and workouts**
- Complete **3 new challenges daily** to build streaks and track consistency
- Compete on a **leaderboard** of top streaks and completed challenges
- Connect with others via a built-in **community chat**

----

Features:
- **User Autehntication**
    - Register with unique username (validated for duplicates)
    - Secure login/logout system with Flask-Login
    - Change password anytime from **Profile -> Settings**

- **Progress Tracking**
    - Log workouts and nutrition and exercise data
    - Dashboard view for history

- **Goals & Challenges**
    - Select from multiple fitness goals with tailored diet and workout plans
    - 3 new challenges every day to stay engaged
    - Build streaks & track total challenges completed

- **Leaderboard**
    - Top 20 users ranked by streaks
    - Top 20 users ranked by challenges completed

- **Community Chat**
    - Real-time chat system to share progress, ask for help, or find a community

---
**Tech Stack**
- **Backend:** Python, Flask, Flask-Login, SQLAlchemy
- **Frontend:** HTML, CSS
- **Database:** SQLite

---

### Setup

```bash
# Clone repo
git clone https://github.com/NischalT2/FitPulse
cd FitPulse

# Create virtual environment
python -m venv venv
# Activate (Mac/Linux)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

#Run application
flask run
```

---

## Screenshots

### Landing Page
<img width="2940" height="1536" alt="image" src="https://github.com/user-attachments/assets/905d2115-d618-4b27-81e4-7e6cfc44b081" />


### Log
<img width="2910" height="1516" alt="image" src="https://github.com/user-attachments/assets/d3d8dfa1-1f7c-4e49-9fce-a14329cded1c" />

### Dashboard
<img width="2914" height="1496" alt="image" src="https://github.com/user-attachments/assets/cf2b2580-4d11-4ce3-ad1b-38867722dad8" />

### Challenges
<img width="2920" height="1380" alt="image" src="https://github.com/user-attachments/assets/3acf6372-1f3a-4982-a9e7-9d7169a342e4" />

### Leaderboard
<img width="2854" height="1478" alt="image" src="https://github.com/user-attachments/assets/386349ca-50ac-4cfe-bd3b-67b4820620c7" />

### Community Chat
<img width="2778" height="1034" alt="image" src="https://github.com/user-attachments/assets/86bbf640-aca2-4125-80c6-9aa626fbfa9d" />

### Goals
<img width="2872" height="1446" alt="image" src="https://github.com/user-attachments/assets/1325c0a0-3638-4c9f-be5a-54d7d3c18d8b" />






