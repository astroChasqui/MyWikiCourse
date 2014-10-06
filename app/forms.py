from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SubmitField, \
                    SelectField
from wtforms.validators import Required, Email
from models import User

class LoginForm(Form):
    email = TextField("Email", validators= [Required(), Email()])
    password = PasswordField("Password", validators = [Required()])
    remember_me = BooleanField("remember_me", default = True)
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class SignupForm(Form):
    firstname = TextField("First name", validators = [Required()])
    lastname = TextField("Last name", validators = [Required()])
    email = TextField("Email", validators= [Required(), Email()])
    password = PasswordField('Password', validators = [Required()])
    submit = SubmitField("Create account")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
   
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("This email address is already "+\
                                      "associated with a MyWikiCourse "+\
                                      "account.")
            return False
        else:
            return True

class CreateCourseForm(Form):
    title = TextField("Title", validators = [Required()])
    submit = SubmitField("Create course")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
   
    def validate(self):
        if not Form.validate(self):
            return False

class EditCourseForm(Form):
    title = TextField("Title", validators = [Required()])
    new_section_title = TextField("Title", validators = [Required()])
    new_section_wiki_title = TextField("Title in Wikipedia",
                                       validators = [Required()])
    new_section_wiki_section = TextField("Section title in Wikipedia",
                                         validators = [Required()])
    submit = SubmitField("Update")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
   
    def validate(self):
        if not Form.validate(self):
            return False

class CourseTitleForm(Form):
    title = TextField("Title", validators = [Required()])
    submit = SubmitField("Update")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
   
    def validate(self):
        if not Form.validate(self):
            return False

class NewSectionForm(Form):
    title = TextField("Title")
    wiki_title = TextField("Title in Wikipedia", validators = [Required()])
    wiki_section = TextField("Section title in Wikipedia")
    chapter = SelectField("Chapter", choices=[('uno', '1'), ('dos', '2')])
    section = SelectField("Section", choices=[('uno', '1'), ('dos', '2')])
    subsection = SelectField("Subsection",
                              choices=[('uno', '1'), ('dos', '2')])
    subsubsection = SelectField("Subsubsection",
                              choices=[('uno', '1'), ('dos', '2')])
    submit = SubmitField("Add new section")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
   
    def validate(self):
        if not Form.validate(self):
            return False
