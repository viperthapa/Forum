"""Utility script to bulk-create Question rows from CSV.

This script can be executed directly from the project root like:

  python forumapp/utils/create_questions.py

or with the virtualenv python executable. It ensures the project root
is on sys.path and initializes Django before importing models so
`ModuleNotFoundError: No module named 'forumapp'` is avoided.
"""

import csv
import os
import sys

# Ensure project root is on sys.path so local packages (like `forumapp`)
# can be imported when this script is run as a file.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myforum.settings')
import django
django.setup()

from forumapp.models import Question, NormalUser

CSV_FILE = os.path.join(BASE_DIR, 'question_category.csv')


def main(csv_file_path=CSV_FILE):
    objects = []

    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                user = NormalUser.objects.get(id=row['user_q'])
            except NormalUser.DoesNotExist:
                # skip rows referencing missing users
                continue

            objects.append(
                Question(
                    user_q=user,
                    category=row.get('category', ''),
                    question=row.get('question', '')
                )
            )

    if objects:
        Question.objects.bulk_create(objects, ignore_conflicts=True)
        print("✅ Bulk import completed: {} objects".format(len(objects)))
    else:
        print("⚠️ No objects to import")


if __name__ == '__main__':
    main()
