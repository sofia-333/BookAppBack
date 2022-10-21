# Book App

### Description

A web-app that provides metadata information about books by providing the ISBN 10 or ISBN 13 number of the book.
Ability to register user, login(with expiring token), reset password.

Rest API used: [OpenLibrary](https://openlibrary.org/).

### Preinstallation

Should have installed pip3, python3, python virtualenv, postgresql
(Linux: https://www.postgresql.org/download/linux/ubuntu/)

## Project setup

After cloning the repository use following commands in the cloned directory to:

### Create and activate VENV

```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies in activated venv from requirements.txt file

```
pip3 install -r requirements.txt
```

### Set up the database

If you're using postgres, create the db with following configurations (may be changed from settings.py):

    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',
Run migrations:
```
python manage.py migrate
```

### Create the superuser

```
python3 manage.py createsuperuser
```

### Configure credentials for SMTP in settings.py for email sending functionality
(later should be moved to .env)

```
EMAIL_HOST_USER = 'your_email'
EMAIL_HOST_PASSWORD = 'your_generated_password'
```
[SMTP email configuration tutorial](https://www.youtube.com/watch?v=ql5Dex4m40w).

### Run the project
```
python manage.py runserver
```
