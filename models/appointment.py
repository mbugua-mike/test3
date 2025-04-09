from datetime import datetime
from extensions import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    doctor_name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    details = db.Column(db.Text) # e.g., purpose of visit, instructions
    status = db.Column(db.String(50), default='Scheduled') # e.g., Scheduled, Completed, Canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Who created the appointment

    # Relationship to access the user who created the appointment
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def __repr__(self):
        return f'<Appointment {self.id} for User {self.patient_id} on {self.appointment_time}>' 