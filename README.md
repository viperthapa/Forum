# Description of project

## Forum

This is a online discussion forum web portal just like Q&A sections built with python django as backend and Html,css and javascript as frontend with simple machine learning predictions using tensorflow with svm for prediction a question in a specific category.

## Features

- Login and registration of user
- Logged in User can ask questions,answers the others questions
- User can like and comment in particular questions
- Mark as a best answer,Total views in questions
- User can delete the questions if the questions doesnot matches the asked questions by the others users
- Automatically prediction of question
- suggestions of similar category of questions

##

To run the project in docker

    git clone repo_url
    pip install -r requirement.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
