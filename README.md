[![Build Status](https://travis-ci.org/andela-sgaamuwa/Checkpoint-2.svg?branch=badges)](https://travis-ci.org/andela-sgaamuwa/Checkpoint-2)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a61f6345a36940539e3f0f1abf13ec01)](https://www.codacy.com/app/samuel-gaamuwa/Checkpoint-2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-sgaamuwa/Checkpoint-2&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/andela-sgaamuwa/Checkpoint-2/tree/develop.svg?style=svg)](https://circleci.com/gh/andela-sgaamuwa/Checkpoint-2/tree/develop)
# BUCKETLIST API APPLICATION 
Bucketlists is a RESTful API application where users can create bucketlists with multiple items.
The application uses Token Based Authentication for user authentication and authorization.

## Application Description

### Dependencies
The Bucketlist API is a python/flask_RESTful application and is mainly dependent on the following technologies

* **[Python3](https://www.python.org/download/releases/3.0/)**
* **[Flask RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.5/)** for route and resource definition
* **[Flast SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)** for database interactions
* **[Werkzeug](http://werkzeug.pocoo.org/docs/0.11/utils/#module-werkzeug.security)** for password security
* **[Itsdangerous](http://pythonhosted.org/itsdangerous/)** for token based authentication
* **[Unittest](https://docs.python.org/2/library/unittest.html)**, **[Nose](http://nose.readthedocs.io/en/latest/)** and **[Tox](http://tox.readthedocs.io/en/latest/)** for the testing

### Functionality
The user of the application has the ability to carry out the following

* Register a new user with the application 
    * Usernames have to be unique for a successful registration
    * Users must provide a password for a successful registration
    * Usernames and passwords must be minimum 4 characters for successful registration 
    ```
        {
            "username": "sample_username",
            "password": "sample_password"
        }
    ```

* Login to use the system with the same information above

* Once logged in, the user then requests for token
    * Each token is valid for 30 minutes after which it is invalid
    * Once logged in, a user can request another token, without having to log back in 

* Users can create new bucketlists each with a unique name with the POST information below
    ```
        {
            "name": "sample_bucketlist"
        }
    ```

* For each bucketlist, a user can add an items with a similar post

* Items and bucketlists can be deleted from the server
    * Deleting a bucketlist deletes all its items

* Bucketlist names can be updated and Items' done statuses can also be updated

* A user can request for all their bucketlists in the system, or a specific bucketlist

* **Users can only interact with bucketlists that they created**

### API endpoints and Routes 

|ENDPOINT | FUNCTIONALITY|
|--- | ---
|POST ```/auth/login``` | Logs a user in|
|POST ```/auth/register``` | Register a user|
|POST ```/bucketlists```| Create a new bucket list|
|GET ```/bucketlists``` | List all the created bucket lists|
|GET ```/bucketlists/<id>```| Get single bucket list|
|PUT ```/bucketlists/<id>```| Update this bucket list|
|DELETE ```/bucketlists/<id>```| Delete this single bucket list|
|POST ```/bucketlists/<id>/items/```| Create a new item in bucket list|
|PUT ```/bucketlists/<id>/items/<item_id>```|Update a bucketlist item|
|DELETE ```/bucketlists/<id>/items/<item_id>```| Delete an item in a bucket list|

## Installation
The bucketlist API is a flask and Python3 application and it is advisable to install it in a virtual environment. 
As most Linux machines come with Python 2 installed, it is required that you install Python 3 through the terminal using the commands 
```
$ sudo apt-get update 
$ sudo apt-get install python3 
```
If you are using macOS, python3 can be installed through the terminal using the command
```
$ brew install python3
```
If you do not already have git installed on your system install it as well
```
$ sudo apt-get install git
```
or on macOS
```
$ brew install git
```
Python3 comes with a package manager called pip, which enables you to install different packages in your environment 
We shall use pip to install virtualenv, which helps us create a virtual environment where dependencies can be installed without impacting the rest of the system
To install virtualenv run the following command 
```
$ pip install virtualenv
```
Once installed, create a directory for the application called Bucketlist and open it using the commands
```
$ mkdir Bucketlist
$ cd Bucketlist
```
Create a virtual environment for the application that is python3 specific 
```
$ virtualenv -p python3 venv-bucketlist
```
Activate the virtual environment 
```
$ source venv-bucketlist/bin/activate 
```
At this point, clone the project into the folder, move into the project directory and run the requirements file
```
$ git clone https://github.com/andela-sgaamuwa/Checkpoint-2.git
$ cd Checkpoint-2
$ pip install -r requirements.txt
```
The application is then ready to run, simply use the command 
```
$ python manage.py runserver
```

## Running tests
Upon installation it is advisable to run the tests to ensure that the application is running as it should and nothing is broken
In the root directory of the application, via the terminal, run the command
```
$ nosetests --with-coverage --cover-package=app
```
A successful test should produce the following results 
```
(cp2-venv) Samuels-MacBook-Pro:bucketlist gaamuwa$ nosetests --with-coverage --cover-package=app
.....................
Name                    Stmts   Miss  Cover
-------------------------------------------
app.py                      0      0   100%
app/app.py                  7      0   100%
app/authentication.py      46      3    93%
app/bucketlist.py         127      0   100%
app/models.py              40      0   100%
app/resource.py           116      1    99%
-------------------------------------------
TOTAL                     336      4    99%
----------------------------------------------------------------------
Ran 21 tests in 3.364s
```