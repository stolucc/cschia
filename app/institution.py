from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.models import User, ResearchGroup, GroupMembership
from flask_login import current_user, login_user, logout_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional


def validate_institution(current_user, id):
    for aff in current_user.institution_affilations:
        if aff.institution.id == id:
            return aff.institution
    abort(403)


@app.route("/institution")
@login_required
def institution_select():
    institutions = [i.institution for i in current_user.institution_affilations]
    if len(institutions) == 0:
        abort(403)
    elif len(institutions) == 1:
        return redirect(url_for("institution_dashboard", id=institutions[0].id))
    else:
        return render_template("institution_select.html", title="Institution Dashboard", institutions=institutions)


@app.route("/institution/<int:id>")
@login_required
def institution_dashboard(id):
    institution = validate_institution(current_user, id)
    return render_template("institution_dashboard.html", title="Institution Dashboard - {}".format(institution.name), institution=institution)

