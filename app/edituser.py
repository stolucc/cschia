from app import app, db, admin_required
from flask import render_template, flash, redirect, url_for, request, abort
from app.models import User, Publication
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import UpgradeUser

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, \
TextAreaField, IntegerField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional, NumberRange
from app.models import User



@app.route("/admin_edit_user/", methods=["GET", "POST"])
@login_required


def admin_edit_user():
    admin_required(current_user)
    
    # print("hello1")

    def check_exists(name):
        # print("hello2")
        return User.query.filter_by(email=name).first()

    form = UpgradeUser()
    # print("form:",form)

    if form.validate_on_submit():
        emailForUser = form.email.data
        researcher = form.Researcher.data
        admin = form.Admin.data
        reviewer = form.Reviewer.data

        # print("email:",emailForUser)
        # print("admin:",admin)
        # print("hostI:",hostI)
        # print("reviewer:",reviewer)


        user = User.query.filter_by(email=form.email.data).first()
        # print(user)
        if researcher == True:
            admin = 0
            reviewer = 0

        user.is_admin = admin
        user.is_reviewer = reviewer
        db.session.add(user)
        db.session.commit()
        flash("The user has been updated!")
        return redirect(url_for("admin_edit_user"))
        
        

    return render_template("admin_edit_user.html", title="Change account type of user", form=form)
    


#need to have search box
#seach by email
#display acccount with that email
#have edit box on that
#then bring to page with form with info filled in
