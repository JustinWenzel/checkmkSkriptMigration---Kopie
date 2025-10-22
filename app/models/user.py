from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import secrets
import string
from flask_mail import Message
from app.models import db, mail


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password)
    
    def check_password(self, plain_text_password):
        return check_password_hash(self.password_hash, plain_text_password)
    
    def check_email(self, email):
        return email == self.email_address

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def reset_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password_length = secrets.choice(range(8, 16))
        plain_text_password = ""

        for i in range(password_length):
            plain_text_password += secrets.choice(characters)
        
        msg = Message(
            subject="Password Reset - CheckMK Management Portal",
            recipients=[self.email_address],
            body=f"Hello {self.username},\n\nYour password has been reset.\n\nYour new password is: {plain_text_password}\n\nPlease log in and change your password immediately.\n\nIf you did not request this password reset, please contact support at JustinSven.Wenzel@gls-germany.com immediately."
        )
        
        try:
            mail.send(msg)
            self.set_password(plain_text_password)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False