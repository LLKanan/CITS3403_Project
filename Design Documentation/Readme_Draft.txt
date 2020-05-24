Design of Application:
Our application is a music quiz website.
We decided to stream the music off of youtube for the purposes of our quiz, we did this by utilising the youtube iframeplayer api.
As for the answer options for our quizzes we opted to go with multiple choice options and automated marking.
For our database we decided to utilise sqlite as we were just running our site from localhost. 
Our database contains 5 tables:
User  - Contains all information regarding users 
      - username,hashed password,email, user id
Quiz  - Contains information regarding a quiz
      - quiz name, quiz id, quiz image, Hidden(whether or not a quiz is currently visible to users)
Question  - Contains information regarding a question
          -Question id, Quiz Id, youtube video id, correct answer, 3 alternative options, 
           start time(time in seconds we start the song at),  duration(time in second song is played for)
Results - Contains information regarding the answer from a user to a particular question
        - Result id, userid, quiz id, question id, user's answer, correct(boolean determining whether user got answer correct)
finalResults  - Contains information regarding the user's final score for a quiz
              - final result id, user id, quiz id, total correct
NOTE: user_id 0 is reserved for the admin, database is initialised with user_id = 0, username = admin, password = admin

Admin Features:
-Ability to create new quizzes
-Ability to toggle the visibility(to users) of a quiz
-Ability to permanently remove a quiz and all data related to quiz(questions,results,final results)
-Ability to remove users and all data related to that user(results, final results)
-Ability to view user's results and answers

User Features:
-Ability to register/login
-Ability to view and attempt all quizzes available(each quiz can only be done once, a quiz is considered completed when a user uses the submit answers button on the final quiz questio page)
-Users can exit the quiz whenever they wish to and all answers selected previous will be saved
-Ability to view results for quizzes they have previous completed
-User has the ability to replay sound clip an unlimited amount of times
-User has the ability to go to previous questions whenever they wish

Setup Guide for localhost
1.Ensure python3 is installed
2.Extract zip folder
3.Change directory to Music_Site_Env in extracted folder
4.Run command "python3 -m venv venv" in terminal to initialise venv
5.Run command "source venv/bin/activate" in terminal to activate venv
6.Run command "pip install -r requirements.txt" to install all requirements
7.Run command "flask db init" to initialise database
8.Run command 'flask db migrate -m "users table"' for database migration
9.Run command "flask db upgrade" for database to apply changes to database
10. Run command "python3 database.py" to initialise admin account (username : admin | pssword : admin)
11. flask run
NOTE:Use http://localhost:5000/ instead of http://127.0.0.1:5000/ due to youtube iframeapi block on non registered domains

