# FitPulse

FitPulse:
This is a web application designed for users to keep track of their fitness journey, goals, challenges, and progress. The application allows for users to select different goals
that gives them a detailed plan for accomplishing that goal. Additionally, it enables users to log their daily nutrition and food datas and their workout datas. Overall, it enables
for the users to track their progress. Furthermore, the application also includes a challenges feature that includes 3 new challenges for the users to complete everyday. 
By completing all three challenges, the users are able to build up their streaks and also their total challenges completed. There is also a leaderboard feature that dispalys 
the top 20 users with the most streaks and the top 20 users with the most challenges completed. Finally, there is a community chat feature in which users are able to chat with other 
users, possibly to ask for help or to let others know about their progress. 

Features:
This application includes a user authentication system in which the users are able to create accounts through register page. They must create accounts with a unique username that is 
not already taken. Additionally, the users must fill out all fields before submitting for correct results. It also includes a login feature where users are able to login to their 
old accounts that they created previously. Users must enter the correct username and password. This is tracked securely using Flask-login. Furthermore, there is also the ability 
for the users to change their password if they feel that their old password is not secure enough. This is available under the profile --> settings section. This lets them enter their 
old password, and their new password that they would like to change to.

Implementation:
Since the zip file already has most of the files needed to run this program, there shouldn't be much needed to run this program. So, to run this program, unzip the project file and extract
the contents out of the file. Then, set up a virtual environment by typing "python -m venv venv" in the terminal. Activate that environment by typing "source venv/bin/activate" on mac or 
"venv\Scripts\activate" on windows. Then, run the application by typing "flask run" in the terminal. Copy and paste the given link in google to open the website. 

To use this program, first, create an account by going to the register page. Then select a goal to see the plan that you should follow to accomplish that goal. Then go to log to start 
tracking your fitness progress. Then go to dashboard to view your history. Then complete the challenges that are assigned to you and then view the leaderboard to see the top 20 users 
with the greatest streaks and challenges completed. Then finally, communicate with the community, using the chat feature of the website.

