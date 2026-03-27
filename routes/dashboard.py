import razorpay
from flask import current_app, jsonify, request, redirect, url_for, Blueprint, render_template, session
from extensions import db
from models import SavedJob, User, Resume
from flask_login import login_required, current_user

# Define Blueprints
main_bp = Blueprint("main", __name__)
dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route('/create-order')
@login_required
def create_order():
    try:
        client = razorpay.Client(auth=(
            current_app.config['RAZORPAY_KEY_ID'],
            current_app.config['RAZORPAY_SECRET']
        ))
        order = client.order.create({
            "amount": 4900, 
            "currency": "INR",
            "payment_capture": 1
        })
        return jsonify(order)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    jobs = [
        {"title": "Python Developer", "company": "TCS", "link": "https://www.tcs.com/careers", "type": "Full-time"},
        {"title": "Data Analyst", "company": "Infosys", "link": "#", "type": "Internship"},
        {"title": "Web Developer", "company": "Wipro", "link": "#", "type": "Full-time"},
        {"title": "Backend Engineer", "company": "HCL", "link": "#", "type": "Full-time"},
    ]

    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.id.desc()).first()
    user_skills = [s.strip().lower() for s in resume.skills.split(",")] if resume and resume.skills else []

    scored_jobs = []
    for job in jobs:
        score = 0
        title = job["title"].lower()
        matched = [skill for skill in user_skills if skill in title]
        score = len(matched)
        job['match'] = min(100, score * 20)
        job['reason'] = ", ".join(matched[:3]) if matched else "General match"
        scored_jobs.append(job)

    recommended_jobs = scored_jobs if getattr(current_user, "is_premium", False) else scored_jobs[:4]

    return render_template(
        "dashboard.html",
        name=current_user.name,
        jobs=jobs,
        recommended_jobs=recommended_jobs,
        is_premium=getattr(current_user, "is_premium", False),
    )

# --- ADDED THIS BACK TO FIX YOUR ERROR ---
@dashboard_bp.route("/save-job", methods=["POST"])
@login_required
def save_job():
    job_link = request.form.get("link")
    # Check if already saved
    existing = SavedJob.query.filter_by(user_id=current_user.id, job_link=job_link).first()
    if not existing:
        new_job = SavedJob(
            user_id=current_user.id,
            job_title=request.form.get("title"),
            company=request.form.get("company"),
            job_link=job_link,
        )
        db.session.add(new_job)
        db.session.commit()
    return redirect(url_for("main.dashboard"))

@main_bp.route("/premium")
@login_required
def premium():
    return render_template("premium.html")

@main_bp.route('/premium_tips')
@login_required
def premium_tips():
    if not getattr(current_user, "is_premium", False):
        return redirect(url_for('main.premium'))
    tips = ["Use action verbs", "Add measurable achievements", "Keep ATS-friendly"]
    return render_template("premium_tips.html", tips=tips)