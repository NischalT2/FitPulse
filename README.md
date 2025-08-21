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
