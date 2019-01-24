from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, GeneralInformationForm
from app.models import User, UserGeneralInformation
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {"username": "Miguel"}
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!"
        },
        {
            "author" : {"username" : "Susan"},
            "body" : "The avengers movie was so cool!"
        }
        
        ]
    return render_template("index.html", title="Home ", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"}
    ]
    return render_template("user.html", user=user, posts=posts)

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form) 

@app.route("/general_information", methods=["GET", "POST"])
@login_required
def edit_general_information():

    form = GeneralInformationForm()
    check_if_exists = UserGeneralInformation.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        if check_if_exists is None:
            user = UserGeneralInformation(user_id=current_user.id)
            db.session.add(user)
            user.firstName = form.firstName.data
            user.lastName = form.lastName.data
            user.jobTitle = form.jobTitle.data
            user.suffix = form.suffix.data
            # user.phoneNum = form.phoneNum.data
            user.email = form.email.data
            user.orcid = form.orcid.data
            db.session.commit()
        else:
            check_if_exists.firstName = form.firstName.data
            check_if_exists.lastName = form.lastName.data
            check_if_exists.jobTitle = form.jobTitle.data
            check_if_exists.suffix = form.suffix.data
            # check_if_exists.phoneNUm = form.phoneNum.data
            check_if_exists.email = form.email.data
            check_if_exists.orcid = form.orcid.data
            db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_general_information"))

    elif request.method == "GET" and check_if_exists is not None:
        form.firstName.data = check_if_exists.firstName
        form.lastName.data = check_if_exists.lastName
        form.jobTitle.data = check_if_exists.jobTitle
        form.suffix.data = check_if_exists.suffix
        # form.phoneNum.data = check_if_exists.phoneNum
        form.email.data = check_if_exists.email
        form.orcid.data = check_if_exists.orcid 

    return render_template("general_information.html", title="Edit general info", form=form)

