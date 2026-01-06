# Quizziverse 🎯
### Full Stack Exam Preparation Platform

## 🧠 Overview
**Quizziverse** is a full-stack, multi-user exam preparation platform designed to simulate real exam environments across multiple subjects and chapters.  
The platform focuses on **role-based access**, **automated evaluation**, **performance analytics**, and **asynchronous background processing**, making it suitable for real-world educational use cases.

This project emphasizes clean backend architecture, proper data modeling, and scalable system design.

---

## 👥 User Roles

### 🔑 Admin (Quiz Master)
- Root-level access (single admin)
- Create and manage subjects and chapters
- Create quizzes with MCQ-based questions
- Schedule quizzes with time limits
- View user performance analytics and summary charts
- Trigger data exports (CSV)

### 👤 User
- Register and log in securely
- Browse available subjects and chapters
- Attempt quizzes with a timer
- View previous attempts and scores
- Receive reminders and activity reports

---

## ⚙️ Key Features
- 🔐 Role-Based Access Control (RBAC)
- ⏱️ Timed quizzes with automatic evaluation
- 📊 Analytics dashboards for performance tracking
- 🗂️ Relational data modeling  
  *(Subjects → Chapters → Quizzes → Questions → Scores)*
- ⚡ Asynchronous background jobs using **Redis & Celery**:
  - Daily reminders
  - Monthly activity reports
  - CSV exports
- 🚀 Caching to improve API performance
- 📱 Responsive UI using Bootstrap

---

## 🛠️ Tech Stack

### Backend
- Flask (REST APIs)
- SQLAlchemy (ORM)
- SQLite (Database)
- Redis (Caching & message broker)
- Celery (Async & scheduled jobs)

### Frontend
- Vue.js
- HTML, CSS
- Bootstrap

---

## 🗃️ Database Design (High-Level)
- User (Admin / Student)
- Subject
- Chapter
- Quiz
- Question
- Score

> All database tables are created programmatically. No manual database creation is used.

---

## 🧩 Architecture Highlights
- MVC-based backend structure
- Separation of concerns between API, background jobs, and UI
- Stateless APIs with validation
- Extensible design for adding new subjects and reports

---

## 🚀 Future Enhancements
- Cloud deployment
- Advanced analytics using ML
- Question difficulty analysis
- Migration to scalable databases (PostgreSQL)

---

## 👩‍💻 Author
**Vaishnavi Mishra**  
BS in Data Science & Applications, IIT Madras  
GitHub: https://github.com/Vaishnavi-0222
