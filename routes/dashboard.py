from extensions import db
from models import SavedJob
from flask import request, redirect, url_for, Blueprint, render_template
from flask_login import login_required, current_user
from models import Resume

# Define the blueprint for main application navigation
main_bp = Blueprint("main", __name__)
dashboard_bp = Blueprint("dashboard", __name__)


@main_bp.route("/")
def index():
    """
    Public landing page accessible to everyone.
    """
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():

    jobs = [
        {"title": "Python Developer", "company": "TCS", "link": "#", "type": "Full-time", "deadline": "Apply Soon"},
        {"title": "Data Analyst", "company": "Infosys", "link": "#", "type": "Internship", "deadline": "Apply Soon"},
        {"title": "Web Developer", "company": "Wipro", "link": "#", "type": "Full-time", "deadline": "Apply Soon"},
        {"title": "Backend Engineer", "company": "HCL", "link": "#", "type": "Full-time", "deadline": "Apply Soon"},
        {"title": "Full Stack Intern", "company": "Tech Mahindra (Sample)", "type": "Internship", "link": "https://www.techmahindra.com/en-in/careers/", "deadline": "Oct 30, 2024"},
        {"title": "Junior Python Developer", "company": "Zomato (Sample)", "type": "Fresher Job", "link": "https://www.zomato.com/careers", "deadline": "Nov 05, 2024"},
        {"title": "Cloud Support Associate", "company": "Amazon India (Sample)", "type": "IT Job", "link": "https://www.amazon.jobs/en/locations/india", "deadline": "Nov 12, 2024"},
        {"title": "Backend Developer", "company": "Remote Tech Corp", "type": "Remote Job", "link": "#", "deadline": "Nov 15, 2024"},
    ]

    recommended_jobs = []

    resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.id.desc()).first()

    user_skills = []

    if resume and resume.skills:
        user_skills = [skill.strip().lower() for skill in resume.skills.split(",")]

    scored_jobs = []

    for job in jobs:
        score = 0
        title = job["title"].lower()
        company = job["company"].lower()

    matched_skills = []

    for skill in user_skills:
        if skill in title:
            score += 2
            matched_skills.append(skill)
        elif skill in company:
            score += 1
            matched_skills.append(skill)

    if score > 0:
        match_percent = min(100, score * 20)
        job['match'] = match_percent
        job['reason'] = ", ".join(matched_skills[:3])
        scored_jobs.append((job, score))

# ✅ NOW sort (after building list)
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

# ✅ THEN assign recommended jobs
    if getattr(current_user, "is_premium", False):
        recommended_jobs = [job for job, score in scored_jobs]
    else:
        recommended_jobs = [job for job, score in scored_jobs[:4]]
        
        
    print("IS PREMIUM:", getattr(current_user, "is_premium", False))

    # ✅ ALWAYS return (outside if/else)
    return render_template(
        "dashboard.html",
        name=current_user.name,
        jobs=jobs,
        recommended_jobs=recommended_jobs,
        is_premium=getattr(current_user, "is_premium", False),
    )


@dashboard_bp.route("/save-job", methods=["POST"])
@login_required
def save_job():
    job_title = request.form.get("title")
    company = request.form.get("company")
    job_link = request.form.get("link")

    # check if already saved
    existing = SavedJob.query.filter_by(
        user_id=current_user.id, job_link=job_link
    ).first()

    if not existing:
        new_job = SavedJob(
            user_id=current_user.id,
            job_title=job_title,
            company=company,
            job_link=job_link,
        )
        db.session.add(new_job)
        db.session.commit()

    return redirect(url_for("dashboard.dashboard"))


# New premimum Route
@main_bp.route("/premium")
@login_required
def premium():
    return render_template("premium.html")
