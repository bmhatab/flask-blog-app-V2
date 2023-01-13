# Welcome to the Flask Blog App</h1>

<p>This app is a simple blogging platform built using the Flask framework. It allows users to create an account, log in, create posts, view other users' posts, edit their own posts, and edit their personal profiles. The app also utilizes encryption to securely store user password hashes in the database, rather than storing the actual passwords.</p>

## Features
- User registration and login
- Create, view, and edit posts
- Edit personal profile
- Secure password storage using encryption

## Getting Started
### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- Werkzeug
- bcrypt


### Installation
-Clone the repository to your local machine
-Copy code
-git clone https://github.com/bmhatab/flask-blog-app-V2.git
-Copy code
-cd flask-blog-app-V2/app/venv
#### Install the required packages
-Copy code
-pip install -r requirements.txt

#### Look for a file called "config.py" in the 'venv' directory and set the following environment variables:
SECRET_KEY
SQLALCHEMY_DATABASE_URI (for example: "sqlite:///test.db")
Run the command
#### At the root directory where 'manager.py' lives
Run once in the terminal
- set FLASK_APP = manager.py
After this you can launch the app with
- flask run 

## Usage
Register for an account by navigating to the "Sign Up" page
Log in to your account
Create a new post by navigating to the "Add Post" page
View other users' posts by navigating to the "Posts" page
Edit your own posts by navigating to the "Posts" page and clicking the "Edit" button on a post
Edit your personal profile by navigating to the "Dashboard" page
Security
The app utilizes encryption to securely store user password hashes in the database, rather than storing the actual passwords. This helps to protect user data in the event of a security breach. Additionally, the app uses the Flask-Login library to handle user authentication and session management, which also helps to protect user data.

## Contribution
If you find any bug or have any ideas to improve this application, please feel free to open a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
Flask and the Flask community for creating and maintaining the Flask framework
The creators and contributors of the various packages used in this project, including Flask-SQLAlchemy, Flask-WTF, Flask-Login, and bcrypt.
