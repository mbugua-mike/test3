from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.meeting import Meeting
from models.notification import Notification
from models.appointment import Appointment
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/meetings')
@login_required
def meetings():
    upcoming_meetings = Meeting.query.filter(Meeting.date >= datetime.utcnow()).order_by(Meeting.date.asc()).all()
    return render_template('meetings.html', meetings=upcoming_meetings)

@main_bp.route('/clinic-routine')
@login_required
def clinic_routine():
    user_appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.appointment_time.asc()).all()
    return render_template('clinic_routine.html', appointments=user_appointments)

@main_bp.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=user_notifications)