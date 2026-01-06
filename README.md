Full Stack Exam Preparation Platform
🧠 Project Overview

Quizziverse is a full-stack, multi-user exam preparation platform designed to simulate real exam environments across multiple subjects and chapters.
The application supports role-based access, automated evaluation, performance analytics, and background job processing, making it scalable and suitable for real-world educational use cases.

This project focuses on clean backend architecture, data modeling, and asynchronous task handling.

👥 User Roles
🔑 Admin (Quiz Master)

Root-level access (single admin)

Create & manage subjects and chapters

Create quizzes with MCQ questions

Schedule quizzes with time limits

View user performance analytics & summary charts

Trigger data exports (CSV)

👤 User

Register & login securely

Browse subjects and chapters

Attempt quizzes with a timer

View past attempts and scores

Receive reminders and reports

⚙️ Key Features

🔐 Role-Based Access Control (RBAC) for Admin and Users

⏱️ Timed quizzes with automatic evaluation

📊 Analytics dashboards for performance tracking

🗂️ Relational data modeling (Subjects → Chapters → Quizzes → Questions → Scores)

⚡ Asynchronous background jobs using Redis & Celery:

Daily quiz reminders

Monthly activity reports

CSV export of quiz results

🚀 Caching strategies to improve API performance

📱 Responsive UI using Bootstrap

🛠️ Tech Stack

Backend

Flask (REST APIs)

SQLAlchemy (ORM)

SQLite (Database)

Redis (Caching & message broker)

Celery (Async & scheduled jobs)

Frontend

Vue.js

HTML, CSS

Bootstrap

🗃️ Database Design (High Level)

User (Admin / Student)

Subject

Chapter

Quiz

Question

Score

All database tables are created programmatically (no manual DB creation).

🧩 Architecture Highlights

MVC-based backend structure

Separation of concerns between API, background jobs, and UI

Stateless APIs with structured validation

Extensible design for adding new subjects and reports

🚀 Future Enhancements

Deployment on cloud infrastructure

Enhanced analytics with ML-based performance insights

Question difficulty analysis

Scalable database migration (PostgreSQL)

👩‍💻 Author

Vaishnavi Mishra
BS in Data Science & Applications, IIT Madras
GitHub: https://github.com/Vaishnavi-0222
