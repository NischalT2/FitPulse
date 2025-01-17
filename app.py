from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_db_connection
import sqlite3
import datetime as dt
from datetime import datetime
import random
import secrets
from dotenv import load_dotenv
import os
from response import responses
from flask_socketio import SocketIO, emit

# loads .env which holds the secret key
load_dotenv()

app = Flask(__name__)
# makes a secure key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")
# used for the community chat feature
socketio = SocketIO(app)

#initializes flash login
login_manager = LoginManager()
login_manager.init_app(app)
# redirects unauthorized users to the login page
login_manager.login_view = "login"

@app.after_request
# Ensures that clients always receive the latest data
def after_request(response):
    #Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#UserMixin inherits methods from Flask-login, creates a user class necessary methods for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        #stores users id and username
        self.id = id
        self.username = username
    
    # returns the user's id as a string
    def get_id(self):
        return str(self.id)


#load user callback for Flask login
@login_manager.user_loader
def load_user(user_id):
    # connects to the database and allows for SQL queries to be executed
    conn = get_db_connection()
    # conn.execute makes the user a dictionary with data from the database
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    # if a user is found, integrates with flask-login to represent the logged in user; otherwise it returns None
    if user:
        return User(id=user["id"], username=user["username"])
    return None

# route for the index page
@app.route("/")
def index():
    return render_template("index.html")
    
# route for the login page
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields need to be filled", "error")
            return redirect(url_for("login"))
        
        # if there are no errors, retrieves user's data using the username inputted
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        # if a user with this username exists and the password is correct, create this user instance
        if user and check_password_hash(user["passhash"], password):
            user_obj = User(user["id"], username = user["username"])
            # log the user in using flask_login feature
            login_user(user_obj)
            flash("Login Successful!", "success")
            return redirect(url_for("index"))
        
        # if this username does not exist or password was incorrect
        flash("Invalid username or password", "danger")
    # if method is "Get" or if the login was not sucessful
    return render_template("login.html")

# route for the register page
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmpass = request.form.get("confirmpass")
        height = request.form.get("height")
        weight = request.form.get("weight")
        age = request.form.get("age")
        gender = request.form.get("gender")

        # if all fields are not filled
        if not username or not password or not confirmpass or not height or not weight or not age or not gender:
            flash("All fields must be filled", "error")
            return redirect(url_for("register"))
        
        if password != confirmpass:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))
        
        #checks that the values entered by the user are valid values
        try:
            height = float(height)
            weight = float(weight)
            age = int(age)
        except ValueError:
            flash("Height, weight, and age must be valid numbers", "danger")
            return redirect(url_for("register"))
        
        # inserts the user into the Users table except if there are errors
        try:
            # this is needed to write sql queries. 
            conn = get_db_connection()
            conn.execute("INSERT INTO Users(username, passhash, height, weight, age, gender) VALUES (?, ?, ?, ?, ?, ?)", (username, generate_password_hash(password), height, weight, age, gender))
            conn.commit()
        # if the username is already taken, let user know and redirect them to the register page
        except sqlite3.IntegrityError:
            flash("Username already taken", "danger")
            return redirect(url_for("register"))
        finally:
            conn.close()
        
        # steps to log the user in after registering
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
        conn.close()
        user_obj = User(user["id"], username = user["username"])
        login_user(user_obj)
        flash("Registration Successful!", "success")
        return redirect(url_for("index"))
    
    # if request method is get
    return render_template("register.html")
    
# route for the settings page
@app.route("/settings")
@login_required
def settings():
    conn = get_db_connection()
    # fetches the user's username, date when account was created, their streak, and total_challenges complete
    username = conn.execute("SELECT username FROM Users WHERE id = ?", (current_user.id,)).fetchone()[0]
    account_date = conn.execute("SELECT created_at FROM Users WHERE id = ?", (current_user.id,)).fetchone()[0]
    streak = conn.execute("SELECT streak FROM stats WHERE user_id = ?", (current_user.id,)).fetchone()[0]
    total_challenges = conn.execute("SELECT total_challenges_completed FROM stats WHERE user_id = ?", (current_user.id,)).fetchone()[0]

    return render_template("settings.html", username = username, streak = streak, total_challenges = total_challenges, date = account_date)

# route to change password page
@app.route("/passwordchange", methods=["GET", "POST"])
@login_required
def passwordchange():
    # if user submitted a form
    if request.method == "POST":
        # store the values that the user input
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        confirmation = request.form.get("confirmpass")

        conn = get_db_connection()
        # finds the hashes of the user's current password
        oldpasshash = conn.execute("SELECT passhash FROM Users WHERE id = ?",(current_user.id,)).fetchone()[0]
        # checks if user submitted any blank fields, if they did, error message
        if not oldpass or not newpass or not confirmation:
            flash("All fields need to be filled", "error")
            return redirect(url_for("passwordchange"))
        # if the current password that the user input does not match the actual password, return apology.
        elif not check_password_hash(oldpasshash, oldpass):
            flash("Incorrect current password entered!")
            return redirect(url_for("passwordchange"))
        # if the new password that the user entered and the confirmation password that they entered do not match,
        # return error
        elif newpass != confirmation:
            flash("New Passwords do not match!")
            return redirect(url_for("passwordchange"))

        # if successful, query updates the user's password
        # it also hashes the password for security
        conn.execute("UPDATE Users SET passhash = ? WHERE id = ?",(generate_password_hash(newpass), current_user.id))
    
        conn.commit()
        conn.close()

        flash("Password changed!")
        return redirect("/")

    return render_template("passwordchange.html")

# route for logging out
@app.route("/logout")
@login_required
def logout():
    # use flask-login feature to log out the user
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))

# route for logsheet page
@app.route("/logsheet", methods = ["GET", "POST"])
@login_required
def logsheet():
    if request.method == "POST":
        # stores the values entered by the user
        calories = request.form.get("calories")
        protein = request.form.get("proteins")
        carbs = request.form.get("carbs")
        duration = request.form.get("workout-duration")
        cal_burnt = request.form.get("calories-burnt")
        steps = request.form.get("steps")

        user_id = current_user.id

        try:
            conn = get_db_connection()
            # inserts the values into the Logs table
            conn.execute("""
                INSERT INTO Logs (user_id, calories, protein, carbs, workout_duration, calories_burnt, steps) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, calories, protein, carbs, duration, cal_burnt, steps))
            conn.commit()
            conn.close()

            flash("Log entry added successfully!", "success")
            return redirect(url_for('dashboard'))
        # if there is an error, error message is shown
        except Exception as e:
            flash(f"An error occured: {e}", "danger")
            return redirect(url_for('logsheet'))
        
    return render_template('logsheet.html')


# route for the dashboard page
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    # for more control over the queries
    cursor = conn.cursor()
    # fetches the sums of all the values submitted in the log of one day and stores them in a descending order
    cursor.execute("""
            SELECT
                DATE(created_at) AS day,
                SUM(calories) AS total_calories,
                SUM(protein) AS total_protein,
                SUM(carbs) AS total_carbs,
                SUM(workout_duration) AS total_workout_duration,
                SUM(calories_burnt) AS total_calories_burnt,
                SUM(steps) AS total_steps
            FROM Logs
            WHERE user_id = ?
            GROUP BY day
            ORDER BY day DESC
    """, (current_user.id,))
    
    #list of tuples but because of get_db_connection(), it acts like dictionaries
    logs = cursor.fetchall()
    conn.close()

    # Makes the dates readable
    processed_logs = []
    for log in logs:
        # Convert to list if it's a tuple
        processed_log = list(log)
        processed_log[0] = datetime.strptime(processed_log[0], "%Y-%m-%d").strftime("%B %d, %Y")
        processed_logs.append(processed_log)

    return render_template("dashboard.html", logs = processed_logs)


# route for the challenges page
@app.route("/challenges")
@login_required
def challenges():
    conn = get_db_connection()
    # stores the current day's date as year-month-date
    current_date = dt.date.today()
    
    # stores the values from stats table
    user_stats = conn.execute("SELECT streak, total_challenges_completed, last_challenge_date FROM stats WHERE user_id = ?",(current_user.id,)).fetchone()
    # if there is already values, sets these variables to those values in the stats table
    if user_stats is not None:
        streak = user_stats["streak"]
        total_challenges_completed = user_stats["total_challenges_completed"]
        last_challenge_date = user_stats["last_challenge_date"]

        print(last_challenge_date)

        # makes it so that the last_challenge_date is stored as the same way as the current_date
        if last_challenge_date:
            last_challenge_date = dt.datetime.strptime(last_challenge_date, "%Y-%m-%d").date()
            print(last_challenge_date)
    # if there are no values in the stats table, set them to default values
    else:
        streak = 0 
        total_challenges_completed = 0 
        last_challenge_date = None 

    # checks if challenges for today already exists
    existing_challenges = conn.execute("SELECT * FROM challenges WHERE user_id = ? AND created_at = ?", (current_user.id, current_date)).fetchall()

    if not existing_challenges:
        # creates three new challenges each day
        random.seed(current_user.id + int(current_date.strftime("%Y%m%d")))
        for i in range(3):
            challengetype_rand = random.randint(1,4)
            if challengetype_rand == 1:
                goal = random.randint(70, 150)
                description = "Eat " + str(goal) + " or more grams of protein today"
            elif challengetype_rand == 2:
                goal = random.randint(150, 300)
                description = "Burn " + str(goal) + " or more calories today"
            elif challengetype_rand == 3:
                goal = random.randint(30, 70)
                description = "Work out for " + str(goal) + " or more minutes today"
            else:
                goal = random.randint(7000, 15000)
                description = "Walk " + str(goal) + " or more steps today"

            # inserts these new challenges into the challenges table
            conn.execute("INSERT INTO challenges (user_id, description, goal, created_at) VALUES (?, ?, ?, ?)",(current_user.id, description, goal, current_date))
        conn.commit()

    # stores the current date's challenges
    challenges = conn.execute("SELECT * FROM challenges WHERE user_id = ? AND created_at = ?",(current_user.id, current_date)).fetchall()
    
    # stores the current date's logs that the user submit
    logs = conn.execute("SELECT * FROM Logs WHERE user_id = ? AND created_at = ?", (current_user.id, current_date)).fetchall()

    # Initialize progress data
    progress_data = {
        "steps": 0,
        "workout_duration": 0,
        "calories_burnt": 0,
        "protein": 0
    }
    # Loop through all logs and adds however much progress the user has made (using the values from the logs table)
    for log in logs:
        progress_data["steps"] += log["steps"]
        progress_data["workout_duration"] += log["workout_duration"]
        progress_data["calories_burnt"] += log["calories_burnt"]
        progress_data["protein"] += log["protein"]

    # Corrected challenge processing
    updated_challenges = []
    all_completed = True  # Assume all are completed until proven otherwise

    for challenge in challenges:
        # Determine progress based on challenge type
        # min makes it so that the smaller value out of the two is recorded so that the max that is recorded for progress is the same as the goal amount
        if "Walk" in challenge["description"]:
            progress = min(progress_data["steps"], challenge["goal"])
        elif "Work out" in challenge["description"]:
            progress = min(progress_data["workout_duration"], challenge["goal"])
        elif "Burn" in challenge["description"]:
            progress = min(progress_data["calories_burnt"], challenge["goal"])
        elif "Eat" in challenge["description"]:
            progress = min(progress_data["protein"], challenge["goal"])
        else:
            progress = 0

        # Check if challenge is completed
        if progress == challenge["goal"] and not challenge["is_completed"]:
            is_completed = 1
            total_challenges_completed += 1
            flash(f"Congratulations! You've completed the challenge: {challenge['description']}", "success")
        else:
            is_completed = challenge["is_completed"]
        
        # If any challenge is not completed, set all_completed to False
        if not is_completed:
            all_completed = False

        # Update challenges table
        conn.execute("UPDATE challenges SET progress = ?, is_completed = ? WHERE id = ?", (progress, is_completed, challenge["id"]))

        # Append to updated challenges
        updated_challenges.append({
            "description": challenge["description"],
            "progress": progress,
            "goal": challenge["goal"],
            "is_completed": is_completed,
        })

    # Streak and stats update logic
    if all_completed:
        if last_challenge_date and (current_date - last_challenge_date).days == 1:
            # If last challenge was completed yesterday, increment streak
            streak += 1
        elif last_challenge_date is None:
            # First time setting a streak, only if all challenges are completed
            streak = 1
        last_challenge_date = current_date
    else:
        # Only reset streak if there's a gap and challenges were not completed
        if last_challenge_date and (current_date - last_challenge_date).days > 1:
            streak = 0

    existing_stats = conn.execute("SELECT * FROM stats WHERE user_id = ?", (current_user.id,)).fetchone()
    if not existing_stats:
    # Insert a new stats entry if it doesn't exist
        conn.execute(
            "INSERT INTO stats (user_id, streak, total_challenges_completed, last_challenge_date) VALUES (?, ?, ?, ?)",
            (current_user.id, streak, total_challenges_completed, last_challenge_date)
        )
    else:
        # Existing update code
        conn.execute(
            "UPDATE stats SET streak = ?, total_challenges_completed = ?, last_challenge_date = ? WHERE user_id = ?",
            (streak, total_challenges_completed, last_challenge_date, current_user.id)
    )

    conn.commit()
    conn.close()

    return render_template("challenges.html", challenges=updated_challenges, streak=streak, total_challenges_completed=total_challenges_completed)


# route for the leaderboard page
@app.route("/leaderboard")
@login_required
def leaderboard():
    conn = get_db_connection()

    # joins the Users and stats table and retrives username, streaks and total_challeges completed
    # one sqlquery ranks it on streaks, while the other ranks it based on total_challenges_completed
    streak_leaderboard = conn.execute("""
        SELECT Users.username, stats.streak, stats.total_challenges_completed
        FROM stats
        INNER JOIN Users ON stats.user_id = Users.id
        ORDER BY stats.streak DESC
        LIMIT 20
        """).fetchall()

    challenges_leaderboard = conn.execute("""
        SELECT Users.username, stats.streak, stats.total_challenges_completed
        FROM stats
        INNER JOIN Users ON stats.user_id = Users.id
        ORDER BY stats.total_challenges_completed DESC
        LIMIT 20
        """).fetchall()

    conn.close()

    return render_template("leaderboard.html", streak_lead = streak_leaderboard, challenges_lead = challenges_leaderboard)


# route for the goal page
@app.route("/goal", methods=["GET", "POST"])
@login_required
def goal():
    goal_response = None  # Initialize goal_response
    if request.method == "POST":
        # stores the users choice for goal
        goal = request.form.get("goal") 
        # get the response from the responses.py page
        goal_response = responses.get(goal, "No plan available for this goal.")
        # Store response in session for retrieval
        session['goal_response'] = goal_response  

        return redirect(url_for('goal'))  # Redirect to avoid form resubmission

    # Retrieve response from session for GET request
    goal_response = session.pop('goal_response', None)

    return render_template("goal.html", goal_response=goal_response)
        

@app.route('/chat')
@login_required
def chat():
    # Fetch the 50 most recent messages
    conn = get_db_connection()
    messages = conn.execute('''
        SELECT messages.content, users.username, messages.timestamp 
        FROM messages 
        JOIN users ON messages.user_id = users.id 
        ORDER BY messages.timestamp ASC 
        LIMIT 50
    ''').fetchall()
    conn.close()
    
    return render_template('chat.html', messages=messages)

# Handles incoming messages
@socketio.on('send_message')
def handle_message(data):
    # stores the message
    message_content = data['message']
    
    # Insert message into database
    conn = get_db_connection()
    conn.execute("INSERT INTO messages (content, user_id) VALUES (?, ?)", (message_content, current_user.id))
    conn.commit()
    conn.close()
    
    # Broadcast message to all the connected users
    emit('new_message', {
        'username': current_user.username,
        'message': message_content,
        'timestamp': dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, broadcast=True) # the broadcast makes sure that the message is sent to all users

# Start the Socket.IO server to handle incoming connections
if __name__ == "__main__":
    socketio.run(app, debug=True)

        
