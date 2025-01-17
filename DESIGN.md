FitPulse:

This program uses Flask, a web framework used for creating service-side logic. It also uses Flask-Login, which provides simple user authentication and session management. It also uses Flask-SocketIO, which allows for real-time communication with the different users of the application. This is needed for enabling the community chat feature. It also uses SQLite3, which is a lightweight relational database used to store user data, logs, challenges, and chat messages. This is needed for creating all the tables in the database and also to use sql queries in the app.py. It also uses Werkzeug, which is a utility library for password hashing and security. This makes it more secure for the users passwords. It also uses dotenv, which loads environment variables for sensitive configuration (e.g., Flask secret key). This is needed for the app.py to use the flask secret key that was stored in the .env file. It also uses HTML/CSS/JS, which is a must need for the frontend and for rendering the user interface and handling interactions. This is what enabled for the creation of all the html webpages and the stylings, and also the chat feature, which was mostly done with javascript. Jinja2 is also used in this program and is needed for rendering HTML dynamically.


The application includes multiple tables which include: 
Users Table
- id: Primary key.
- username: Unique username.
- passhash: Hashed password for authentication.
- age: User's age.
- height: User's height in cm.
- weight: User's weight in kg.
- gender: User's gender.
- created_at: Timestamp of when the user was created.

 Stats Table

- id: Primary key.
- user_id: Foreign key to the Users table.
- streak: Number of consecutive days the user has completed challenges.
- total_challenges_completed: Total number of challenges completed by the user.
- last_challenge_date: The last date the user completed a challenge.

Challenges Table

- id: Primary key.
- user_id: Foreign key to the Users table.
- description: Description of the challenge.
- goal: The target value for the challenge (e.g., steps, calories burned).
- progress: User's progress on the challenge.
- is_completed: Boolean value indicating whether the challenge was completed.
- created_at: Date when the challenge was created.

 Logs Table

- id: Primary key.
- user_id: Foreign key to the Users table.
- calories: Calories consumed by the user.
- protein: Protein consumed by the user.
- carbs: Carbs consumed by the user.
- workout_duration: Duration of the user's workout in minutes.
- calories_burnt: Calories burned during the workout.
- steps: Number of steps taken by the user.
- created_at: Date when the log entry was created.

Messages Table:
- id: Primary key.
- user_id: Foreign key to the Users table
- content: the message that was sent
- timestamp: Date when the message was sent
