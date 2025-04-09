from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from models.user import User

# Function to provide the query for QuerySelectField
def user_query():
    # Return users ordered by username, you can customize this
    return User.query.order_by(User.username)

class MeetingForm(FlaskForm):
    title = StringField('Meeting Title', validators=[DataRequired()])
    date = DateTimeField('Date and Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    location = StringField('Location')
    description = TextAreaField('Description')
    submit = SubmitField('Add Meeting')

class NotificationForm(FlaskForm):
    message = TextAreaField('Notification Message', validators=[DataRequired()])
    submit = SubmitField('Send Notification')

class AppointmentForm(FlaskForm):
    patient = QuerySelectField('Patient', query_factory=user_query, get_label='username', allow_blank=False, validators=[DataRequired()])
    appointment_time = DateTimeField('Appointment Date and Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    doctor_name = StringField('Doctor/Provider', validators=[Optional()])
    location = StringField('Clinic/Location', validators=[Optional()])
    details = TextAreaField('Details / Instructions', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Scheduled', 'Scheduled'), 
        ('Completed', 'Completed'), 
        ('Canceled', 'Canceled')
    ], default='Scheduled', validators=[DataRequired()])
    submit = SubmitField('Save Appointment') 