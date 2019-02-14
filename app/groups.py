from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.models import User, ResearchGroup, GroupMembership
from flask_login import current_user, login_user, logout_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional


@app.route("/groups")
@login_required
def show_groups():
    groups = [m.group for m in current_user.groups]
    return render_template("list_groups.html", groups=groups)


@app.route("/groups/create", methods=["GET", "POST"])
@login_required
def create_group():
    form = CreateGroupForm()
    if form.validate_on_submit():
        group = ResearchGroup(name=form.name.data)
        db.session.add(group)
        membership = GroupMembership(user=current_user, group=group)
        db.session.add(membership)
        db.session.commit()
        return redirect(url_for("show_groups"))
    return render_template("create_group.html", form=form)


@app.route("/groups/<group_id>", methods=["GET", "POST"])
@login_required
def view_group(group_id):
    group = ResearchGroup.query.filter_by(id=group_id).first_or_404()
    form = GroupAddUserForm(group_id)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        membership = GroupMembership(user=user, group=group)
        db.session.add(membership)
        db.session.commit()
    return render_template("view_group.html", form=form, group=group)


class CreateGroupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Register")


class GroupAddUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def __init__(self, group_id):
        self.group_id = group_id
        super().__init__()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        group = ResearchGroup.query.filter_by(id=self.group_id).first()
        if user is None:
            raise ValidationError("Please choose an existing user.")
        for membership in user.groups:
            if membership.group == group:
                raise ValidationError("User is already in group.")
