from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    email = db.Column(db.String(64), unique = True)
    pwdhash = db.Column(db.String(54))
    registered_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    courses = db.relationship('Course', backref = 'author', lazy = 'dynamic')

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_registration_date(self, datetime):
        self.registered_on = datetime

    def set_last_login(self, datetime):
        self.last_login = datetime

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime)
    #created_on = db.Column(db.DateTime)
    #last_update = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, user_id):
        self.title = title.title()
        self.user_id = user_id

    def __repr__(self):
        return '<Course %r>' % (self.title)