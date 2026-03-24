from extensions import db
from models import SavedJob
from flask import request, redirect, url_for, Blueprint, render_template
from flask_login import login_required, current_user

# Define the blueprint for main application navigation
main_bp = Blueprint('main', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

@main_bp.route('/')
def index():
    """
    Public landing page accessible to everyone.
    """
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard accessible only after login.
    Displays categorized sample jobs for Indian job seekers.
    """
    # Sample job data for Phase-1 (Production-ready placeholder)
    # In a real app, these could eventually come from a database or API
    jobs = [
        {
            'title': 'Full Stack Intern',
            'company': 'Tech Mahindra (Sample)',
            'type': 'Internship',
            'link': 'https://www.techmahindra.com/en-in/careers/',
            'deadline': 'Oct 30, 2024'
        },
        {
            'title': 'Junior Python Developer',
            'company': 'Zomato (Sample)',
            'type': 'Fresher Job',
            'link': 'https://www.zomato.com/careers',
            'deadline': 'Nov 05, 2024'
        },
        {
            'title': 'Cloud Support Associate',
            'company': 'Amazon India (Sample)',
            'type': 'IT Job',
            'link': 'https://www.amazon.jobs/en/locations/india',
            'deadline': 'Nov 12, 2024'
        },
        {
            'title': 'Backend Developer',
            'company': 'Remote Tech Corp',
            'type': 'Remote Job',
            'link': '#',
            'deadline': 'Nov 15, 2024'
        }
    ]

    # Pass the user's name and the job list to the template
    return render_template(
        'dashboard.html',
        name=current_user.name,
        jobs=jobs,
        is_premium=getattr(current_user, "is_premium", False)
    )

@dashboard_bp.route('/save-job', methods=['POST'])
@login_required
def save_job():
    job_title = request.form.get('title')
    company = request.form.get('company')
    job_link = request.form.get('link')

    # check if already saved
    existing = SavedJob.query.filter_by(
        user_id=current_user.id,
        job_link=job_link
    ).first()

    if not existing:
        new_job = SavedJob(
            user_id=current_user.id,
            job_title=job_title,
            company=company,
            job_link=job_link
        )
        db.session.add(new_job)
        db.session.commit()

    return redirect(url_for('dashboard.dashboard'))

# New premimum Route
@main_bp.route('/premium')
@login_required
def premium():
    return render_template('premium.html')