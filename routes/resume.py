from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models import db, Resume
from fpdf import FPDF
import io

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume', methods=['GET', 'POST'])
@login_required
def build_resume():


    resume = Resume.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        # Collect data from form
        form_data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'education': request.form.get('education'),
            'skills': request.form.get('skills'),
            'experience': request.form.get('experience'),
            'projects': request.form.get('projects')
        }

        if not resume:
            # Create a new record linked to current_user if none exists
            resume = Resume(user_id=current_user.id, **form_data)
            db.session.add(resume)
        else:
            # Update existing record fields
            for key, value in form_data.items():
                setattr(resume, key, value)
        
        db.session.commit()
        flash('Resume details saved successfully!', 'success')
        return redirect(url_for('resume.build_resume'))

    return render_template('resume_form.html', resume=resume)

@resume_bp.route('/resume/download')
@login_required
def download_resume():
    # Fetch only the resume belonging to the logged-in user
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    
    if not resume:
        flash('Please fill out the form and save before downloading.', 'warning')
        return redirect(url_for('resume.build_resume'))

    # Initialize PDF (fpdf2)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header: Name (Bold & Large)
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 15, resume.full_name, ln=True, align='C')
    
    # Header: Contact Info
    pdf.set_font("Helvetica", size=10)
    contact_text = f"Email: {resume.email} | Phone: {resume.phone}"
    pdf.cell(0, 5, contact_text, ln=True, align='C')
    pdf.ln(10)

    # Helper function to create professional sections
    def add_section(title, content):
        # Section Title Bar
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_fill_color(240, 240, 240)  # Light Gray background for ATS readability
        pdf.cell(0, 8, f"  {title.upper()}", ln=True, fill=True)
        pdf.ln(2)
        # Section Content
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)

    # Add content sections
    if resume.education: add_section("Education", resume.education)
    if resume.skills: add_section("Technical Skills", resume.skills)
    if resume.experience: add_section("Experience & Internships", resume.experience)
    if resume.projects: add_section("Key Projects", resume.projects)

    # Generate the PDF to memory (Bytes)
    # fpdf2 returns a bytearray/bytes when destination is not specified
    pdf_output = pdf.output()
    
    # Create a file-like buffer for Flask to send
    buffer = io.BytesIO(pdf_output)
    buffer.seek(0)

    # Professional filename formatting
    safe_filename = f"{resume.full_name.replace(' ', '_')}_Resume.pdf"

    return send_file(
        buffer, 
        mimetype='application/pdf', 
        as_attachment=True, 
        download_name=safe_filename
    )