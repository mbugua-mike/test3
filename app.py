from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, mail, migrate
from models.user import User
# Import other models to ensure SQLAlchemy can find them
from models.appointment import Appointment
from models.notification import Notification
from models.meeting import Meeting
import click
from markupsafe import Markup # Import Markup
import re # Import re for regex

# Define the nl2br filter function
def nl2br(value):
    if value is None:
        return ''
    # Replace newline characters with <br> tags
    # Use Markup to mark the string as safe HTML
    return Markup(re.sub(r'\r\n|\r|\n', '<br>\n', str(value)))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register the custom filter with Jinja
    app.jinja_env.filters['nl2br'] = nl2br
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Import models within the app context after extensions are initialized
    # This ensures SQLAlchemy knows about them when creating relationships.
    with app.app_context():
        from models import user, appointment, notification, meeting

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Add CLI command
    @app.cli.command("set-admin")
    @click.argument("email")
    def set_admin(email):
        """Promotes an existing user to admin."""
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f'Error: User with email {email} not found.')
            return
        
        if user.is_admin: # Check if already admin
            print(f'User {email} is already an admin.')
            return

        user.is_admin = True
        db.session.add(user) # Add to session even for updates
        db.session.commit()
        print(f'User {email} has been promoted to admin successfully.')

    # Add DB Reset command
    @app.cli.command("reset-db")
    def reset_db_command():
        """Drop all database tables and recreate them (Deletes all data!)."""
        if click.confirm("This will delete all data in the database. Are you sure?", abort=True):
            with app.app_context():
                print("Dropping all database tables...")
                db.drop_all()
                print("Creating all database tables...")
                db.create_all()
                print("Database has been reset.")

    return app

app = create_app()

@app.route('/')
def index():
    about_text = (
        "NYANDARUA CANCER AND SUPPORT GROUP..\n"
        "It was launched on February 22 2019\n"
        "By His Excellency The Former Governor Francis Kimemia of Nyandarua County "
        "and the first Lady Ann Kimemia who was the patron then.\n"
        "It is a community based organisation that deals with creating cancer awareness..\n"
        "It has over 300 members who are cancer patients/survivors.\n"
        "The members meet once in every month at JM KARIUKI HOSPITAL.\n"
        "The group is governed by 5 committee members\n"
        "1. Chairperson\n"
        "2. Secretary\n"
        "3. Ass Secretary\n"
        "4. Treasurer\n"
        "5. Palliative Nurse."
    )
    return render_template('index.html', about_text=about_text)

if __name__ == '__main__':
    app.run(debug=False) 
