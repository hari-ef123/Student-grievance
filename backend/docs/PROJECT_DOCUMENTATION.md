# Student Grievance Redressal System - Complete Documentation

## 1. Project Abstract
The **Student Grievance Redressal System** is a digital transformation project designed to simplify the process of lodging and resolving student complaints within an educational institution. It replaces the slow, manual, and opaque paper-based systems with a modern, transparent, and secure web application.

---

## 2. System Analysis

### 2.1 Problem Definition
Traditional grievance systems are often:
- **Paper-heavy**: Hard to store and retrieve.
- **Vague**: Students don't know who is handling their issue.
- **Slow**: Physical routing of complaints takes days.
- **Lacking Anonymity**: Reluctance to report sensitive issues.

### 2.2 Proposed Solution
A centralized web portal that allows:
- **Students**: To submit, track, and manage grievances.
- **Admins**: To review, comment, and resolve issues systematically.
- **Technology**: Real-time status updates via a high-performance backend.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript | Modern UI with Glassmorphism aesthetic. |
| **Backend** | FastAPI (Python) | High-performance, asynchronous REST API. |
| **Database** | SQLite + SQLAlchemy | Efficient relational data storage. |
| **Security** | JWT, Argon2/Bcrypt | Industry-standard authentication and hashing. |

---

## 4. System Design & Architecture

### 4.1 Architecture Diagram
The system follows a **Decoupled Architecture**:
1.  **Client Side**: Standard web browsers making AJAX/Fetch requests.
2.  **Server Side**: FastAPI handling logic, authentication, and database transactions.
3.  **Data Persistence**: SQLite database file storing persistent records.

### 4.2 Database Schema (Entity Relationship)
- **Users Table**: `id`, `name`, `email`, `hashed_password`, `role` (student/admin).
- **Complaints Table**: `id`, `student_id` (FK), `category`, `description`, `is_anonymous`, `status`, `admin_remark`, `created_at`.

---

## 5. Module Breakdown

### 5.1 Student Module
- **Registration & Login**: Secure credential-based access.
- **Dashboard**: Visual tracking of active complaints.
- **Grievance Submission**: Simplified form with category selection.
- **Anonymous Reporting**: Privacy-first feature for sensitive complaints.

### 5.2 Admin Module
- **Master Dashboard**: View of all grievances across the institution.
- **Response System**: Ability to provide official remarks and justifications.
- **Status Control**: Updating complaint state from "Pending" to "Resolved".

---

## 6. Security Implementation
- **Data Protection**: All passwords are salted and hashed before storage.
- **Stateless Auth**: JWT tokens prevent session hijacking and improve scalability.
- **Input Validation**: Pydantic schemas ensure no malformed data enters the backend.

---

## 7. Future Scope
- **AI Classification**: Auto-routing complaints to departments using NLP.
- **Email Notifications**: Real-time alerts when a complaint is resolved.
- **Mobile Integration**: Native apps for Android and iOS.

---

## 8. Final Asset Links
- [📊 Project Presentation (.pptx)](file:///C:/Users/Lenovo/.gemini/antigravity/brain/1c7708c7-5f76-43a6-901c-7650e8c3b1d3/Student_Grievance_Redressal_System.pptx)
- [📄 Project Report (.docx)](file:///C:/Users/Lenovo/.gemini/antigravity/brain/1c7708c7-5f76-43a6-901c-7650e8c3b1d3/Student_Grievance_Project_Report.docx)
