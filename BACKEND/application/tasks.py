from celery import shared_task 
import csv
from jinja2 import Template
from .mail import send_email
from .models import *
import datetime
import requests
import os
import csv
@shared_task(name="download_user_quiz_csv")
def download_user_quiz_csv(user_id):
    from .models import QuizSubmission, Quiz, Chapter
    from app import db  # only if you're using scoped session

    submissions = QuizSubmission.query.filter_by(user_id=user_id).all()

    filename = f"user_csv_{user_id}.csv"
    filepath = os.path.join("static", filename)

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Quiz ID', 'Chapter ID', 'Date of Quiz', 'Score'])

        for s in submissions:
            quiz = Quiz.query.get(s.quiz_id)
            chapter_id = quiz.chapter_id if quiz else 'N/A'
            date_of_quiz = quiz.date_of_quiz.strftime('%Y-%m-%d') if quiz and quiz.date_of_quiz else 'N/A'
            # remarks = "Good" if s.percentage and s.percentage >= 60 else "Needs Improvement"
            writer.writerow([s.quiz_id, chapter_id, date_of_quiz, s.score])

    return filename
@shared_task(name="monthly_html_report")
def monthly_html_report():
    from .models import User, QuizSubmission
    from jinja2 import Template
    from app import db  # adjust if needed

    users = User.query.filter_by(role='user').all()

    for user in users:
        submissions = QuizSubmission.query.filter(
            QuizSubmission.user_id == user.id,
            QuizSubmission.submitted_at >= datetime.datetime.now().replace(day=1)
        ).all()

        if not submissions:
            continue

        total_score = sum(s.score for s in submissions if s.score is not None)
        avg_score = total_score / len(submissions)

        html_template = """
        <h2>Hello {{ name }}</h2>
        <p>Here is your monthly quiz report:</p>
        <ul>
            <li>Quizzes Attempted: {{ quizzes_taken }}</li>
            <li>Average Score: {{ average_score }}</li>
        </ul>
        <table border="1" cellpadding="5">
            <tr><th>Quiz ID</th><th>Score</th><th>Date</th></tr>
            {% for s in submissions %}
            <tr>
                <td>{{ s.quiz_id }}</td>
                <td>{{ s.score }}</td>
                <td>{{ s.submitted_at.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </table>
        """
        html = Template(html_template).render(
            name=user.full_name,
            quizzes_taken=len(submissions),
            average_score=round(avg_score, 2),
            submissions=submissions
        )

        send_email(user.email, subject="📊 Monthly Quiz Report", message=html)

    return "Monthly reports sent."
# 

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
@shared_task(name="daily_reminder_googlechat")
def daily_reminder_googlechat():
    import datetime
    import requests
    from .models import User, QuizSubmission

    print("Task started...")

    users = User.query.filter_by(role='user').all()
    print(f"Found {len(users)} users.")

    today = datetime.date.today()

    for user in users:
        last_submission = QuizSubmission.query.filter_by(user_id=user.id).order_by(QuizSubmission.submitted_at.desc()).first()
        print(f"{user.full_name} | Last submission: {last_submission.submitted_at if last_submission else 'None'}")

        if not last_submission or last_submission.submitted_at.date() < today:
            text = f"Hey {user.full_name}, you haven't attempted any quiz today. New quizzes might be available at http://127.0.0.1:5173 – go check! 📚✨"

            webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAipgYNZ8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=YRuQ2me-gmfCTkAvXgkvS7f7up2R77ECwteqYsIS0Ws"
            res = requests.post(webhook_url, json={"text": text})

            print(f"[Google Chat] Sent to {user.full_name} | Status: {res.status_code} | Response: {res.text}")

    return "Daily reminders sent."

@shared_task(name="admin_user_score_export")
def admin_user_score_export():
    from .models import User, QuizSubmission

    filename = f"admin_user_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = f'static/{filename}'

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', 'Full Name', 'Quizzes Attempted', 'Average Score'])

        users = User.query.filter_by(role='user').all()

        for user in users:
            submissions = QuizSubmission.query.filter_by(user_id=user.id).all()
            total_score = sum(s.score for s in submissions if s.score is not None)
            attempts = len(submissions)
            avg_score = total_score / attempts if attempts > 0 else 0
            writer.writerow([user.id, user.full_name, attempts, round(avg_score, 2)])

    return filename
