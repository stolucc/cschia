from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.models import User, Publication
from flask_login import current_user, login_user, logout_user, login_required

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, \
TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional, NumberRange
from app.models import User

@app.route("/publication/new", methods=["GET", "POST"])
@login_required
def new_publication():
    form = PublicationForm()
    if form.validate_on_submit():
        publication = Publication(title=form.title.data, doi=form.doi.data, year=form.year.data, journal=form.journal.data, type=form.type.data, status=form.status.data, primary_user=current_user.id)
        db.session.add(publication)
        db.session.commit()
        return redirect(url_for("view_publication", id=publication.id))
    return render_template("publication.html", form=form)

@app.route("/publication/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_publication(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    form = PublicationForm(obj=publication)
    if form.validate_on_submit():
        publication.title = form.title.data
        publication.doi = form.doi.data
        publication.year = form.year.data
        publication.type = form.type.data
        publication.journal = form.journal.data
        publication.status = form.status.data
        db.session.commit()
        return redirect(url_for("view_publication", id=publication.id))
    return render_template("publication.html", form=form)

@app.route("/publications", defaults={"id": None})
@app.route("/publications/by/<int:id>")
@login_required
def list_publications(id):
    if id is None:
        user = None
        publications = Publication.query.all()
    else:
        user = User.query.filter_by(id=id).first_or_404()
        publications = Publication.query.filter_by(primary_user=id).all()

    return render_template("publications.html", user=user, publications=publications)

@app.route("/publications/<int:id>")
@login_required
def view_publication(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    author = User.query.filter_by(id=publication.primary_user).first_or_404()
    return render_template("view_publication.html", publication=publication, author=author)

class PublicationForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    doi = StringField("DOI")
    year = IntegerField("Year of Publication", validators=[DataRequired()])
    journal = StringField("Journal / Conference", validators=[DataRequired()])
    type = SelectField("Publication type", validators=[DataRequired()], choices=[(x,x) for x in [
        "Refereed original article",
        "Refereed review article",
        "Refereed conference paper",
        "Book",
        "Technical report"]])
    status = SelectField("Publication status", validators=[DataRequired()], choices=[(x,x) for x in [
        "Published",
        "In press"]])
    submit = SubmitField("Submit")
