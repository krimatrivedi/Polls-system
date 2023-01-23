# Poll System

A poll application in which a user can create a poll and ask questions. Other users can give their answers as votes.
### Registration/Login page

-  User can register new account
-  User can login into existing account

### Homepage

-  User can register new account
-  User can login into existing accoun

### Registration/Login page

- Only registered users can view this page
- User can view poll questions asked by other users
- There must be an option to create poll question


### Create Poll question
- Users can create poll question on this page
- Each question must have 4 options as vote
- User can create up to maximum 5 questions

### User Profile Page
- User details will be displayed on the page - name, email, phone
- Details cannot be edited
- There must be a list of questions created by this user.
------------

+ celery tasks in the project to delete polls which are created before 24 hours.
+ APIs for poll application using django_rest_framework
------------

### list  for programmin
- Python, django, django_rest_framework 
- jquery
- celery

#### run
- activate environment- env\Scripts\activate
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

#### Installation

- celery and depending upon your os rabbitmq/redis
- `     delete_file() ` if don't want to use celery comment this

.


```

