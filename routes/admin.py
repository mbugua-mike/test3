from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models.user import User
from models.meeting import Meeting
from models.notification import Notification
from models.appointment import Appointment
from extensions import db
from forms.admin import MeetingForm, NotificationForm, AppointmentForm

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    user_count = User.query.count()
    meeting_count = Meeting.query.count()
    appointment_count = Appointment.query.count()
    return render_template('admin/dashboard.html', user_count=user_count, meeting_count=meeting_count, appointment_count=appointment_count)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/meetings', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_meetings():
    form = MeetingForm()
    if form.validate_on_submit():
        new_meeting = Meeting(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(new_meeting)
        db.session.commit()
        flash('New meeting added successfully!')
        return redirect(url_for('admin.manage_meetings'))
        
    meetings = Meeting.query.order_by(Meeting.date.desc()).all()
    return render_template('admin/meetings.html', form=form, meetings=meetings)

@admin_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_notifications():
    form = NotificationForm()
    if form.validate_on_submit():
        message_text = form.message.data
        users = User.query.all()
        notification_count = 0
        for user in users:
            notification = Notification(user_id=user.id, message=message_text)
            db.session.add(notification)
            notification_count += 1
        db.session.commit()
        flash(f'Notification sent to {notification_count} users.')
        return redirect(url_for('admin.manage_notifications'))
        
    return render_template('admin/notifications.html', form=form)

@admin_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_appointments():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient.data.id,
            appointment_time=form.appointment_time.data,
            doctor_name=form.doctor_name.data,
            location=form.location.data,
            details=form.details.data,
            status=form.status.data,
            created_by_id=current_user.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash(f'Appointment scheduled for {form.patient.data.username}.')
        return redirect(url_for('admin.manage_appointments'))
        
    appointments = db.session.query(Appointment, User).join(User, Appointment.patient_id == User.id).order_by(Appointment.appointment_time.desc()).all()
    
    return render_template('admin/appointments.html', form=form, appointments_with_users=appointments)

# Add routes for editing/deleting meetings/users if needed 