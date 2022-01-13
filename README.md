# DOECE Alumni Portal
A project for Department Of Electronics and Computer Engineering (DOECE), Pulchowk Campus!!!

### A DBMS project by:<br>
Jiwan Prasad Guragain 075bct041<br>
Yaman Subedi          075bct045<br>
Luna Manandhar        075bct047<br>
Bipin Khanal          075bct021<br>

### ... Continued on the project by:<br>
Anusandhan Pokhrel 073BCT507<br>
Baibhav Bista      073BCT511<br>
Lumanti Dangol     073BCT521<br>
Mohit Kedia        073BCT523<br>


### Languages, Frameworks:
Python, Django, PostGreSQL


### Project Details
Main django app- DOECEAlumniStudent<br>
Django app for records - records<br>

Requirements are in requirements.txt<br>
pip install -r requirements.txt<br>

Will  also have to set up the database.
Database settings are in DOECEAlumniStudent/settings.py, towards the end.
Make sure to change the credentials to something that is not so 
laughably guessable and save it as an environment variable or something.


venv and media are not supposed to be in this repo.
Once the server was up and we were getting responses, 
I did not want to mess it up.<br>
Hopefully, you guys know what you are doing 
and remove these two from the repo.


Development branch - master<br>
Server branch - server<br>

Development:<br>
In settings.py, at the end, 
1) comment out the lines between 
    "#PRODUCTION(Manaslu Server) START"
    and
    "#PRODUCTION(Manaslu Server) END"
2) uncomment out the lines between 
    "#DEVELOPMENT START"
    and
    "#DEVELOPMENT END"
    
Production:<br>
The opposite of the above

backup_script.sh backups the PostGreSQL database as well as the media files.
More details in server_notes/ directory.

