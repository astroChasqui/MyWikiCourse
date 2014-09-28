from flask import render_template, flash, redirect, g, session, request,\
                  url_for
from flask.ext.login import login_required, current_user, login_user,\
                            logout_user
from app import app, lm, db
from forms import LoginForm, SignupForm, CreateCourseForm, EditCourseForm
from models import User, Course
import datetime


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    courses = [
               {
                "author": {"name": "Ivan Ramirez"},
                "title": "Solar System"
               },
               {
                "author": {"name": "Someone Else"},
                "title": "Stellar Astronomy"
               }
              ]
    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           courses = courses)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', title="Log In", form=form)
        else:
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                if 'remember_me' in request.form:
                    remember_me = True
                else:
                    remember_me = False
                user.set_last_login(datetime.datetime.now())
                db.session.commit()
                login_user(user, remember = remember_me)
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', title="Log In", form=form)
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data,
                           form.email.data, form.password.data)
            newuser.set_registration_date(datetime.datetime.now())
            db.session.add(newuser)
            db.session.commit()
            flash("Sign up successful. Please sign in.")
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/profile')
@login_required
def profile():
    user = g.user
    courses = Course.query.filter_by(user_id = user.id).all()
    return render_template('profile.html',
                           title = 'Profile',
                           user = user,
                           courses = courses)


@app.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    user = g.user
    form = CreateCourseForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('create_course.html',
                                   title = 'Create course',
                                   user = user, form=form)
        else:
            newcourse = Course(form.title.data, user.get_id())
            db.session.add(newcourse)
            db.session.commit()
            flash("Course created.")
            return redirect(url_for('profile'))            
    elif request.method == 'GET':
        return render_template('create_course.html',
                               title = 'Create course',
                               user = user, form=form)


@app.route('/edit_course/<id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    user = g.user
    course = Course.query.filter_by(id = id).first()
    form = EditCourseForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('edit_course.html',
                                   title = 'Edit course',
                                   user = user, form = form, course = course)
        else:
            #newcourse = Course(form.title.data, user.get_id())
            #db.session.add(newcourse)
            #db.session.commit()
            flash("Course edited.")
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        return render_template('edit_course.html',
                               title = 'Edit course',
                               user = user, form = form, course = course)


from collections import OrderedDict
import wikipedia

@app.route('/<id>')
def course(id):
    course = Course.query.filter_by(id = id).first()

    sects = OrderedDict()
    sects["Meh! Mercury"] = ["Mercury_(planet)", "Naked-eye viewing"]
    sects["*Venus"] = ["Venus", ""]
    sects["Earth: out planet"] = ["Earth", ""]
    sects["Mars"] = ["Mars", ""]
    sects["Gas giant Jupiter"] = ["Jupiter", "Atmosphere"]
    sects["Pluto: no longer a planet!"] = ["Pluto", "Classification"]

    sects_text = {}
    for sect in sects.keys():
        sects_text[sect] = getwikitext(sects[sect][0], sects[sect][1])

    return render_template("course.html",
                           course = course, sects=sects, sects_text=sects_text
                          )

def getwikitext(page, section):
    wp = wikipedia.page(page)
    if section != "":
        return wp.section(section).split("\n")
    else:
        return wp.summary.split("\n")
