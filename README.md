# Forum — Q&A web portal (Django)

This repository contains a simple online discussion forum (a Q&A-style web portal) built with Django. It includes standard forum features and a small TF-IDF + Logistic Regression model used to predict the category of a question.

## Highlights

- User registration and login
- Ask questions and post answers
- Like and comment on questions/answers
- Mark best answers and track total views
- Automatic category prediction for questions (TF-IDF + Logistic Regression)

## Screenshots

Home / Feed:


![Forum feed](static/images/feed.png)

Question detail / Notifications:

![Question detail](static/images/detail.png)

> Replace the two placeholder images in `images/` with real screenshots (same filenames) to show real UI.

## Quick start (local)

Prerequisites:

- Python 3.10+ 
- pip

Steps:

```bash
# clone the repo
# git clone <repo_url>
cd Forum

# create a virtualenv (optional — the repo includes `myformenv_new/` but creating a fresh one is recommended)
python3 -m venv .venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# apply migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# run the dev server
python manage.py runserver
```

## Training the question classifier

The small training script is at `forumapp/utils/train.py`. It will create two files:

- `question_model.pkl` — the trained sklearn model
- `vectorizer.pkl` — the TF-IDF vectorizer

Run it from the project root so the pickles are saved in the project directory (or run it with the desired working directory):

```bash
./myformenv_new/bin/python forumapp/utils/train.py
# or with an activated venv:
python forumapp/utils/train.py
```
## Contributing

If you'd like help adding tests or converting the training script into a Django management command, open an issue or submit a PR.

---
README last updated: 2025-11-06
