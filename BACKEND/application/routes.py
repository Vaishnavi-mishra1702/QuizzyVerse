from flask import current_app as app,jsonify,request,abort
from .models import *
from flask_jwt_extended import create_access_token,current_user,jwt_required, get_jwt_identity
from .database import db
from functools import wraps
from datetime import datetime
import json

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(msg="Access denied: insufficient role"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper



def register_routes(app, db):
    # Setup Admin on App Start
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@batman.com").first():
            admin = User(
                email="admin@batman.com",
                password="123456",
                full_name="Admin User",
                qualification="Superuser",
                dob=datetime(1990, 1, 1),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    @app.route("/api/register", methods=["POST"])
    def register():
        try:
            data = request.get_json()

            if data.get('role') == 'admin':
                return jsonify({"error": "Registration as Admin is not allowed"}), 403

            if User.query.filter_by(email=data.get('email')).first():
                return jsonify({"error": "User already exists"}), 400

            dob_date = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()


            user = User(
                email=data.get('email'),
                password=data.get('password'),
                full_name=data.get('full_name'),
                qualification=data.get('qualification'),
                dob=dob_date,
                role="user"
            )
            db.session.add(user)
            db.session.commit()

            return jsonify({"message": "User registered successfully"}), 201

        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or user.password != data.get('password'):
        return jsonify({"error": "Invalid Credentials"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token, role=user.role)


# @app.route("/dashboard", methods=["GET"])
# @role_required('admin')
# def dashboard():
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if user.role == 'admin':
#         return jsonify("Welcome to Admin Dashboard")
#     return jsonify("Welcome to User Dashboard")
# Admin-only route
@app.route("/admin/dashboard", methods=["GET"])
@role_required('admin')
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify("Welcome to Admin Dashboard")


# User-only route
@app.route("/user/dashboard", methods=["GET"])
@role_required('user')  # optional check
def user_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify("Welcome to User Dashboard")

@app.route("/api/subjects", methods=["POST"])
@role_required('admin')
def create_subject():
    try:
        data = request.get_json()
        print("Received Data:", data)

        if not data or not data.get('name'):
            return jsonify({'error': 'Subject name is required'}), 400

        subject = Subject(name=data['name'], description=data.get('description'))
        db.session.add(subject)
        db.session.commit()

        return jsonify({'message': 'Subject Created'}), 201

    except Exception as e:
        print('Error while creating subject:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route("/api/subjects/<int:subject_id>", methods=["GET"])
@role_required('admin')
def get_subject(subject_id):
    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404

        subject_data = {
            'id': subject.id,
            'name': subject.name,
            'description': subject.description
        }

        return jsonify(subject_data), 200

    except Exception as e:
        print('Error fetching subject:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
@role_required('admin')
def update_subject(subject_id):
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Subject name is required'}), 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404

        subject.name = data['name']
        subject.description = data.get('description')
        db.session.commit()

        return jsonify({'message': 'Subject updated successfully'}), 200

    except Exception as e:
        print('Error updating subject:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/api/subjects/<int:subject_id>/chapters", methods=["POST"])
@role_required('admin')
def create_chapter(subject_id):
    try:
        data = request.get_json()
        if not data.get('name'):
            return jsonify({"error": "Chapter name is required"}), 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404

        chapter = Chapter(
            subject_id=subject_id,
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(chapter)
        db.session.commit()

        return jsonify({"message": "Chapter created successfully", "chapter_id": chapter.id}), 201

    except Exception as e:
        print('Error creating chapter:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route("/api/subjects", methods=["GET"])
@role_required('admin')
def get_subjects():
    try:
        subjects = Subject.query.all()
        result = []
        for subject in subjects:
            subject_data = {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'chapters': []
            }
            for chapter in subject.chapters:
                chapter_data = {
                    'id': chapter.id,
                    'name': chapter.name,
                    'description': chapter.description,
                    'quizzes': []
                }
                for quiz in chapter.quizzes:
                    chapter_data['quizzes'].append({
                        'id': quiz.id,
                        'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
                        'time_duration': quiz.time_duration,
                        'remarks': quiz.remarks
                    })
                subject_data['chapters'].append(chapter_data)
            result.append(subject_data)
        return jsonify(result), 200

    except Exception as e:
        print('Error fetching subjects:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/api/chapters/<int:chapter_id>", methods=["GET"])
@role_required('admin')
def get_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        chapter_data = {
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description
        }
        return jsonify(chapter_data), 200

    except Exception as e:
        print('Error fetching chapter:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route("/api/chapters/<int:chapter_id>", methods=["PUT"])
@role_required('admin')
def update_chapter(chapter_id):
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Chapter name is required'}), 400

        chapter = Chapter.query.get_or_404(chapter_id)
        chapter.name = data['name']
        chapter.description = data.get('description')
        db.session.commit()

        return jsonify({'message': 'Chapter updated successfully'}), 200

    except Exception as e:
        print('Error updating chapter:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route("/api/chapters/<int:chapter_id>", methods=["DELETE"])
@role_required('admin')
def delete_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({'message': 'Chapter deleted successfully'}), 200

    except Exception as e:
        print('Error deleting chapter:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
@app.route('/admin/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@jwt_required()
def add_quiz(chapter_id):
    data = request.get_json()
    date_of_quiz = data.get('date_of_quiz')
    time_duration = data.get('time_duration')
    remarks = data.get('remarks')

    if not date_of_quiz or not time_duration:
        return jsonify({'error': 'Missing required fields.'}), 400

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({'error': 'Chapter not found.'}), 404

    try:
        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d').date(),
            time_duration=str(time_duration),  # Assuming minutes stored as string
            remarks=remarks
        )
        db.session.add(quiz)
        db.session.commit()

        return jsonify({'message': 'Quiz added successfully.', 'quiz_id': quiz.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error adding quiz.'}), 500

@app.route("/admin/chapters/<int:chapter_id>/quizzes", methods=["POST"])
@role_required('admin')
def create_quiz(chapter_id):
    data = request.json

    try:
        date_of_quiz = datetime.strptime(data['date_of_quiz'], "%d-%m-%Y").date()

        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=data['time_duration'],
            remarks=data.get('remarks')
        )
        db.session.add(quiz)
        db.session.commit()

        return jsonify("Quiz Created"), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Data"}), 400

@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
@role_required('admin')
def delete_subject(subject_id):
    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404

        db.session.delete(subject)
        db.session.commit()

        return jsonify({'message': 'Subject deleted successfully'}), 200

    except Exception as e:
        print('Error deleting subject:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/admin/quizzes/<int:quiz_id>/questions", methods=["POST"])
@role_required('admin')
def add_question(quiz_id):
    data = request.json
    question = Question(
        quiz_id=quiz_id,
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify("Question Added"), 201
@app.route("/admin/questions/<int:question_id>", methods=["DELETE"])
@role_required('admin')
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'}), 200
@app.route("/admin/questions/<int:question_id>", methods=["PUT"])
@role_required('admin')
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json

    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)

    db.session.commit()
    return jsonify({'message': 'Question updated successfully'}), 200
@app.route("/admin/questions/<int:question_id>", methods=["GET"])
@role_required('admin')
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'question_statement': question.question_statement,
        'option1': question.option1,
        'option2': question.option2,
        'option3': question.option3,
        'option4': question.option4,
        'correct_option': question.correct_option
    }), 200
@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return jsonify({
        'date_of_quiz': str(quiz.date_of_quiz),
        'time_duration': quiz.time_duration,
        'remarks': quiz.remarks
    })
@app.route("/api/quizzes/<int:quiz_id>", methods=["PUT"])
@role_required('admin')
def update_quiz(quiz_id):
    try:
        data = request.get_json()
        quiz = Quiz.query.get_or_404(quiz_id)

        quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
        quiz.time_duration = data['time_duration']
        quiz.remarks = data.get('remarks')

        db.session.commit()
        return jsonify({"message": "Quiz updated successfully"}), 200

    except Exception as e:
        print('Error updating quiz:', str(e))
        return jsonify({"error": "Failed to update quiz"}), 500

@app.route("/api/quizzes/<int:quiz_id>", methods=["DELETE"])
@role_required('admin')
def delete_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({"message": "Quiz deleted successfully"}), 200

    except Exception as e:
        print('Error deleting quiz:', str(e))
        return jsonify({"error": "Failed to delete quiz"}), 500

@app.route("/user/quizzes", methods=["GET"])
@role_required('user')
def available_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{
        'id': quiz.id,
        'chapter': quiz.chapter.name,
        'subject': quiz.chapter.subject.name,
        'date_of_quiz': quiz.date_of_quiz,
        'time_duration': quiz.time_duration
    } for quiz in quizzes]), 200


@app.route("/user/quizzes/<int:quiz_id>/attempt", methods=["POST"])
@role_required('user')
def attempt_quiz(quiz_id):
    user_id = get_jwt_identity()
    data = request.json  # {question_id: selected_option}
    quiz = Quiz.query.get_or_404(quiz_id)

    total_correct = 0
    total_possible = len(quiz.questions)

    for question in quiz.questions:
        selected_option = data.get(str(question.id))
        if selected_option and int(selected_option) == question.correct_option:
            total_correct += 1

    score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=total_correct,
        total_possible=total_possible,
        percentage=(total_correct / total_possible) * 100
    )
    db.session.add(score)
    db.session.commit()

    return jsonify(f"Quiz submitted. Your score: {total_correct}/{total_possible}"), 200
@app.route("/admin/quizzes/<int:quiz_id>/questions", methods=["GET"])
@role_required('admin')
def get_quiz_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    result = [{
        'id': q.id,
        'question_statement': q.question_statement,
        'option1': q.option1,
        'option2': q.option2,
        'option3': q.option3,
        'option4': q.option4,
        'correct_option': q.correct_option
    } for q in questions]
    return jsonify(result), 200


# @app.route("/user/scores", methods=["GET"])
# @role_required('user')
# def user_scores():
#     user_id = get_jwt_identity()
#     scores = Score.query.filter_by(user_id=user_id).all()
#     return jsonify([{
#         'quiz_id': score.quiz_id,
#         'total_scored': score.total_scored,
#         'total_possible': score.total_possible,
#         'percentage': score.percentage,
#         #'attempt_time': score.attempt_time
#     } for score in scores]), 200
@app.route('/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role
        })
    return jsonify(result)

@app.route('/admin/quizzes', methods=['GET'])
def get_quizzes():
    # Replace with actual quiz retrieval logic
    quizzes = [
 
       {"id": 1},
        {"id": 2}
    ]
    return jsonify(quizzes)
@app.route('/api/user/info')
@jwt_required()
def user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)  # fetch by ID

    if not user:
        return jsonify({"error": "User not found"}), 404

    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "role": user.role
    }

@app.route('/api/users/<int:user_id>')
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "name": user.full_name,  # or `user.name`
        "email": user.email,
        "role": user.role
    })

@app.route("/api/user/upcoming-quizzes", methods=["GET"])
@role_required('user')
def get_upcoming_quizzes():
    today = datetime.today().date()
    quizzes = Quiz.query.filter(Quiz.date_of_quiz >= today).order_by(Quiz.date_of_quiz).all()

    result = []
    for quiz in quizzes:
        result.append({
            "id": quiz.id,
            "chapter": quiz.chapter.name,
            "subject": quiz.chapter.subject.name,
            "duration": quiz.time_duration,
            "date": quiz.date_of_quiz.strftime('%Y-%m-%d')
        })
    print("Returning quizzes to frontend:", result)


    return jsonify(result), 200
@app.route("/user/quizzes/<int:quiz_id>/questions", methods=["GET"])
@role_required('user')
def get_quiz_questions_user(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    result = [{
        'id': q.id,
        'question_statement': q.question_statement,
        'option1': q.option1,
        'option2': q.option2,
        'option3': q.option3,
        'option4': q.option4,
    } for q in questions]
    return jsonify(result), 200
@app.route("/api/user/quizzes/<int:quiz_id>/questions", methods=["GET"])
@role_required('user')
def get_user_quiz_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_list = []
    for q in questions:
        question_list.append({
            'id': q.id,
            'text': q.question_statement,
            'options': [q.option1, q.option2, q.option3, q.option4],
            'correct_option': q.correct_option  # ⚠️ Only for testing. Remove this if cheating is a concern.
        })

    return jsonify({
        'questions': question_list,
        'duration': quiz.time_duration  
    }), 200
@app.route('/api/quiz/submit', methods=['POST'])
@role_required('user')  # if you want only logged-in users to submit
def submit_quiz():
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    answers = data.get('answers')  # dict: question_id -> selected option
    score = data.get('score')
    percentage = data.get('percentage')
    if not quiz_id or not answers:
        return jsonify({"error": "Missing data"}), 400

    # Optional: Save submission to DB (assuming a QuizSubmission model)
    submission = QuizSubmission(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=json.dumps(answers),
        score=score,

        percentage=percentage
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({"message": "Quiz submitted successfully"}), 200


@app.route('/admin/summary', methods=['GET'])
@jwt_required()  # or use your own admin_required decorator
def admin_summary():
    summary = []

    subjects = Subject.query.all()

    for subject in subjects:
        subject_name = subject.name
        total_attempts = 0
        top_score = 0

        # Get all quizzes under this subject (via chapters)
        quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()

        for quiz in quizzes:
            submissions = QuizSubmission.query.filter_by(quiz_id=quiz.id).all()

            for submission in submissions:
                total_attempts += 1
                if submission.score is not None:
                    top_score = max(top_score, submission.score)

        summary.append({
            "subject_name": subject_name,
            "top_score": top_score,
            "total_attempts": total_attempts
        })

    return jsonify(summary)
@app.route('/user/scores', methods=['GET'])
@jwt_required()
def user_scores():
    user_id = get_jwt_identity()
    
    submissions = QuizSubmission.query.filter_by(user_id=user_id).all()
    response = []

    for sub in submissions:
        quiz = Quiz.query.get(sub.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        total_questions = len(quiz.questions)
        percentage = round((sub.score / total_questions) * 100, 2) if total_questions > 0 else 0

       

        response.append({
            "id": quiz.id,
            "subject": subject.name,
            "chapter": chapter.name,
            "duration": quiz.time_duration,
            "date": quiz.date_of_quiz.strftime('%Y-%m-%d'),
            "score": sub.score,
            "total": total_questions,
            "percentage": percentage,
            "submitted_at": sub.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(response)
from sqlalchemy import extract, func
# @app.route('/admin/users/<int:user_id>', methods=['GET'])
# @role_required('admin')
# def get_user_by_id(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify({
#         "id": user.id,
#         "name": user.name,
#         "email": user.email,
#         "role": user.role
#     })

@app.route("/admin/question-quiz-stats", methods=["GET"])
def get_question_quiz_stats():
    # Bar chart: Number of questions per subject
    subject_question_data = (
        db.session.query(Subject.name, func.count(Question.id))
        .join(Chapter, Chapter.subject_id == Subject.id)
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(Question, Question.quiz_id == Quiz.id)
        .group_by(Subject.name)
        .all()
    )

    # Pie chart: Number of quizzes attempted per month
    quiz_attempts_by_month = (
        db.session.query(
            extract('month', QuizSubmission.submitted_at).label('month'),
            func.count(QuizSubmission.id)
        )
        .group_by('month')
        .all()
    )

    # Convert month numbers to month names
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    quiz_attempts_data = [
        {"month": months[int(month)-1], "count": count}
        for month, count in quiz_attempts_by_month
    ]

    return jsonify({
        "question_bar_chart": [
            {"subject": subject, "question_count": count}
            for subject, count in subject_question_data
        ],
        "quiz_pie_chart": quiz_attempts_data
    }), 200
from flask import send_from_directory, request
from celery.result import AsyncResult
from .tasks import (
    download_user_quiz_csv,
    monthly_html_report,
    daily_reminder_googlechat,
    admin_user_score_export
)

# 1. Trigger CSV Export for a specific user
@app.route('/api/export/user_csv/<int:user_id>')
def export_user_csv(user_id):
    task = download_user_quiz_csv.delay(user_id)
    return jsonify({
        "task_id": task.id,
        "status": "Started"
    }) 

# 2. Trigger Monthly HTML Report emails
@app.route('/api/send/monthly_report')
def send_monthly_report():
    task = monthly_html_report.delay()
    return {
        "task_id": task.id,
        "status": "Started"
    }

# 3. Trigger Daily Google Chat Reminder
@app.route('/api/send/daily_reminder')
def send_daily_reminder():
    task = daily_reminder_googlechat.delay()
    return {
        "task_id": task.id,
        "status": "Started"
    }

# 4. Trigger Admin Report (CSV of all user scores)
@app.route('/api/export/admin_csv')
def export_admin_csv():
    task = admin_user_score_export.delay()
    return {
        "task_id": task.id,
        "status": "Started"
    }

# 5. Check Celery task status and fetch result file (for both user and admin exports)
# @app.route('/api/task_result/<task_id>')
# def get_task_result(task_id):
#     res = AsyncResult(task_id)
#     if res.state == 'SUCCESS':
#         return send_from_directory('static', res.result)
#     else:
#         return {"status": res.state, "result": str(res.result)}
# from flask import after_this_request

@app.route('/api/task_result/<task_id>')
def get_task_status(task_id):
    result = AsyncResult(task_id)

    print("=== Flask: Checking task ID:", task_id)
    print("State:", result.state)
    print("Result:", result.result)

    response_data = {}

    if result.state == 'PENDING':
        response_data = {'status': 'PENDING'}
    elif result.state == 'SUCCESS':
        if isinstance(result.result, str):
            response_data = {'status': 'SUCCESS', 'result': result.result}
        else:
            response_data = {'status': 'SUCCESS', 'result': str(result.result)}
    elif result.state == 'FAILURE':
        response_data = {'status': 'FAILURE', 'result': str(result.result)}
    else:
        response_data = {'status': result.state}

    response = jsonify(response_data)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers.pop('ETag', None)
    return response
from flask import send_from_directory

@app.route('/static/<path:filename>')
def download_static_file(filename):
    return send_from_directory('static', filename, as_attachment=True)
