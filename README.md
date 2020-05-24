# Design of Application
Our application is a music quiz website.
We decided to stream the music off of youtube for the purposes of our quiz, we did this by utilising the youtube iframeplayer api.
As for the answer options for our quizzes we opted to go with multiple choice quiz with four options and automated marking.
For our database we decided to utilise sqlite as we were just running our site from localhost. 
## Admin Features
* Ability to create new quizzes
* Ability to toggle the visibility(to users) of a quiz
* Ability to permanently remove a quiz and all data related to quiz(questions,results,final results)
* Ability to remove users and all data related to that user(results, final results)
* Ability to view user's results and answers
## User Features
* Ability to register/login
* Ability to view and attempt all quizzes available(each quiz can only be done once, a quiz is considered completed when a user uses the submit answers button on the final quiz questio page)
* Users can exit the quiz whenever they wish to and all answers selected previous will be saved
* Ability to view results for quizzes they have previous completed
* User has the ability to replay sound clip an unlimited amount of times
* User has the ability to go to previous questions whenever they wish
## Database Schema
* User - Contains all information regarding users 
    * user id (int)
    * username (string)
    * hashed password (hashed string)
    * email (string)
* Quiz  - Contains information regarding a quiz
  * quiz name (string)
  * quiz id (int)
  * quiz image (string)
  * Hidden(boolean - whether or not a quiz is currently visible to users)
* Question - Contains information regarding a question
  * Question id (int)
  * Quiz Id (int)
  * youtube video id (string)
  * correct answer (string)
  * option 1 (string)
  * option 2 (string)
  * option 3 (string)
  * start time(int - time in seconds we start the song at)
  * duration(int - time in second song is played for)
* Results - Contains information regarding the answer from a user to a particular question
  * Result id (int)
  * user id (int)
  * quiz id (int)
  * question id (int)
  * user's answer (string)
  * correct(boolean - determining whether user got answer correct)
* finalResults  - Contains information regarding the user's final score for a quiz
  * final result id (int)
  * user id (int)
  * quiz id (int)
  * total correct (string)


NOTE: user_id 0 is reserved for the admin, database is initialised with user_id = 0, username = admin, password = admin


# List of dependencies:
    -Flask
    -Flask Migrate
    -Flask Login
    -Flask Login Manager
    -Flask SQLAlchemy
    -Flask WTForms
    -werkzeug.security
	-Bootstrap CDN
	-JQuery
	-Raleway font
    -UNPKG
	-Popper Javascript
	-Tippy Javascript
    -Youtube iframe API

# Setup Guide for localhost:
1. Ensure python3 is installed
2. Extract zip folder
3. Change directory to Music_Site_Env in extracted folder
4. Run command "python3 -m venv venv" in terminal to initialise venv
5. Run command "source venv/bin/activate" in terminal to activate venv
6. Run command "pip install -r requirements.txt" to install all requirements
7. Run command "flask db init" to initialise database
8. Run command 'flask db migrate -m "users table"' for database migration
9. Run command "flask db upgrade" for database to apply changes to database
10. Run command "python3 database.py" to initialise admin account (username : admin | pssword : admin)
11. flask run

NOTE:Use http://localhost:5000/ instead of http://127.0.0.1:5000/ due to youtube iframeapi block on non registered domains
# Final Distribution of workload:
* Ben:
  * Documentation: All documentation
  * Backend : Entire backend
  * Javascript: userValidation, question_page
  * HTML: Skeleton code for all .html files + bugfixes and minor updates
  * CSS : Minor bug + styling fixes
  * Jinja : All Jinja code
        
* Zac:    
  * CSS: base, index, question page, admin home, create_question, create_quiz + minor bug fixes to other files
  * HTML: base, index, question page, admin home, create_question, create_quiz + minor bug fixes to other files
  * Jinja : Minor bug fixes
        
* Stephen:
  * CSS: base, login, register, quiz results, manage_answers, manage_quizzes, manage_users
  * HTML: base, login, register, quiz results, manage_answers, manage_quizzes, manage_users

* Paula:  
  * CSS: view quizzes, my results, user_answers, user_results, view_questions
  * HTML: view quizzes, my results, user_answers, user_results, view_questions
  * Javascript: misc.js
      

# Development Timeline + Sprint information:

* 5th May :   
  * Group formed with two group memebers - Benjamin Nguyen(22246919|Github: LLKanan) and Zac(22717772|Github: Blankest)
  * Ben creates Github + initial header design + overall design for the project(In design documentation)
            
* 6th May : 
  * Two new group members join - Stephen(22586578|Github: Fmkunle) and Pauline(22550007|Github : PaulineG9)
  * First group meeting:
    * 4 Sprints
        * Base website with no styling and minimum features to meet project spec
        * Adding additional features (Begins 13th May)
        * Styling and aesthetic design for site(Begins 17th May)
        * Integration(Begins 21st May)
    * Initial distribution of workload:
        * Ben - SQL Database + Populate test data,Basic SQL Scripts
        * Zac - Headers, Navigation element, footer
        * Stephen - Login Page, Introduction page, Leaderboard page
        * Paula - Quiz page(List of quizzes), Question page, Results page
    * Ben explains overall design for project to new group members
    * Decide that 21st of May is deadline and all components will be frozen for integration
                
* 8th May: 
  * Second group meeting(Paula absent):
  * Discuss general aesthetic of website
    * Progress updates from members who attended:
      * Zac: header.html (WIP)
      * Ben: database, skeleton code html + jinja for multiple webpages(WIP), backend(WIP)
      * Stephen : home page (WIP)

* 13th May:   
  * Second sprint begins
  * Third group meeting:
    * Progress updates from all members:
      * Ben - Backend(Bugs + youtube id validation remaining),jinja + html skeleton code for all webpages
      * Everyone else - Essentially the same as the previous meeting
    * Zac,Stephen,Paula distribute front end html and css among themselves:
      * Zak: base, index, question page, admin home, create_question, create_quiz
      * Femi: login, register, quiz results, manage_answers, manage_quizzes, manage_users
      * Paula: view quizzes, my results, user_answers, user_results, view_questions

* 15th May:
  * Fourth Group meeting(Ben absent):
    * Front end discussion
  * Ben posts comments regarding designs selected during meeting
         
* 16th May:
    * Fifth Group meeting(Paula Absent):
      * Front end development and discussion(Zac and Stephen)
      * Ben makes some comments on designs chosen
    
* 17th May:
    * Third Sprint begins
    * Ben decreases scope for project due to time restriction limits
    * Features removed
      * Admin feature - edit quizzes
      * Admin feature - manually modify marks
      * Admin feature - give users feedback
      * User Feature - Leaderboards

* 21st May: 
    * Fourth Sprint postponed 1 day
    * Initial Date for integration(postponed)
    * Sixth Group meeting:
      * Stephen and Pauline haven't completed their components and requested 24 hour extension

* 22/23 May:
    * Seventh Group meeting:
      * Integration begins
      * Multiple changes to front end so that style is consistent across site
              
* 24th May:
  * Ben tests and finalises all code + completes all documentation
  * Remaining members comment their respective code
  * Project Completed
