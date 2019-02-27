from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.models import User, Publication
from flask_login import current_user, login_user, logout_user, login_required

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
    form = UpgradeUser()


    keyword = request.args.get('keyword')
        result = User.query.filter(User.email.contains(keyword)).order_by(
            User.email.contains(keyword)).first()
        if result:
            return render_template('user_result.html', user=result)
        else:
            return render_template('search_result.html')
    


#need to have search box
#seach by email
#display acccount with that email
#have edit box on that
#then bring to page with form with info filled in
