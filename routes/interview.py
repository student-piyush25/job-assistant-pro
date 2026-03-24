# Interview pratice logic
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required
from extensions import db

interview_bp = Blueprint('interview', __name__)

# A list of common HR Interview questions used in Indian IT and Corporate sectors
QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want to join our company?",
    "What are your greatest strengths and weaknesses?",
    "Where do you see yourself in five years?",
    "Why should we hire you?",
    "Tell me about a challenge you faced and how you handled it."
]

@interview_bp.route('/interview', methods=['GET', 'POST'])
@login_required
def practice():
    # Initialize question index in user session if not present
    if 'q_index' not in session:
        session['q_index'] = 0

    current_idx = session['q_index']
    feedback = None
    user_answer = None

    if request.method == 'POST':
        # Check if user wants to reset the practice
        if 'reset' in request.form:
            session['q_index'] = 0
            return redirect(url_for('interview.practice'))
        
        # Check if user wants to go to the next question
        if 'next' in request.form:
            session['q_index'] = (current_idx + 1) % len(QUESTIONS)
            return redirect(url_for('interview.practice'))

        # Get the user's answer from the form
        user_answer = request.form.get('answer', '')

        # Simple Phase-1 Feedback Logic
        if len(user_answer.strip()) < 30:
            feedback = "Tip: Your answer is a bit short. Try to elaborate more on your experiences and provide specific examples."
        else:
            feedback = "Good effort! Remember to keep your tone professional, stay confident, and align your answer with the job role."

    return render_template(
        'interview.html', 
        question=QUESTIONS[current_idx], 
        index=current_idx + 1, 
        total=len(QUESTIONS),
        feedback=feedback,
        user_answer=user_answer
    )

@interview_bp.route('/interview/reset')
@login_required
def reset_interview():
    session['q_index'] = 0
    return redirect(url_for('interview.practice'))