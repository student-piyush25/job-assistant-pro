# CareerBoost India | Job Assistant Platform

**CareerBoost India** is a modern, production-ready web application designed specifically for Indian students and freshers. The platform serves as a daily assistant to help job seekers build professional resumes, track the latest opportunities, and practice for HR interviews in one unified dashboard.

---

## 🚀 Phase-1 Completed Features

### 1. ATS-Friendly Resume Builder
* Structured forms to capture Education, Skills, Experience, and Projects.
* Instant generation of professional PDF resumes using the `fpdf2` engine.
* Optimized layout for Applicant Tracking Systems (ATS) used by top Indian IT firms.

### 2. Job Opportunity Dashboard
* Categorized job cards for **Internships**, **Fresher Jobs**, **IT Roles**, and **Remote Work**.
* Real-time UI updates for deadlines and application links.

### 3. HR Interview Practice
* Interactive text-based mock interview module.
* Curated list of common HR questions (e.g., "Tell me about yourself", "Why this company?").
* Automated feedback system to help users improve the length and quality of their responses.

### 4. Secure Authentication & Profile
* Full Register/Login/Logout flow using `Flask-Login`.
* Secure password hashing using `Werkzeug`.
* **Premium Infrastructure**: Future-ready database flags to manage "Premium" user status.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.x, Flask Framework
*   **Database:** SQLite (Relational Database)
*   **ORM:** Flask-SQLAlchemy
*   **PDF Engine:** fpdf2
*   **Frontend:** HTML5, Jinja2 Templates
*   **Styling:** Tailwind CSS (Modern Utility-first CSS)
*   **Icons:** FontAwesome 6.0

---

## 📁 Project Structure

```text
job_assistant_pro/
├── app.py              # Application Entry Point
├── models.py           # Database Schema (User, Resume)
├── routes/             # Modular Blueprint Routes
│   ├── auth.py         # Login/Signup/Testing Logic
│   ├── dashboard.py    # Main Navigation & Jobs
│   ├── resume.py       # PDF Generation & Data Handling
│   └── interview.py    # Mock Interview Logic
├── templates/          # Jinja2 HTML Files
└── static/             # CSS and JS Assets


### 💻 Local Installation & Setup
Follow these steps to get the project running on your local machine:
1. Prerequisites
Ensure you have Python 3.8+ installed on your system.
2. Install Dependencies
Open your terminal in the project root folder and run:
code
Bash
pip install -r requirements.txt
3. Initialize Database & Run
Run the application using the following command:
code
Bash
python app.py
Note: The application will automatically create a instance/database.db file on the first run.
4. Access the App
Open your browser and navigate to:
http://127.0.0.1:5000

## 🧪 Testing Premium Features
To test the "Premium Unlocked" UI states without a payment gateway:
Log in to your account.
Manually visit http://127.0.0.1:5000/make-premium in your browser.
Your account will be upgraded to Premium status for the current session.

📄 License
This project is developed for educational and professional career assistance purposes.
Developed with ❤️ for Indian Job Seekers.
code
Code

## 📌 Current Roadmap

- Phase 1: Core platform complete
- Phase 2: Premium feature foundation complete
- Phase 3: Deployment preparation in progress
- Phase 4: Real user testing and monetization

---

### 👨‍💻 Author

Built with care for Indian job seekers • Crafted by Piyush Hatwar