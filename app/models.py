from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
import json
from app import app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcid = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_reviewer = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    groups = db.relationship("GroupMembership", back_populates="user")

    general_information = db.relationship("GeneralInformation", uselist=False)
    education_information = db.relationship("EducationInformation")
    employment_information = db.relationship("EmploymentInformation")
    societies_information = db.relationship("SocietiesInformation")
    awards_information = db.relationship("AwardsInformation")
    funding_diversification = db.relationship("FundingDiversification")
    impacts = db.relationship("Impacts")
    innovation_and_commercialisation = db.relationship("InnovationAndCommercialisation")
    presentations = db.relationship("Presentations")
    academic_collaborations = db.relationship("AcademicCollaborations")
    non_academic_collaborations = db.relationship("NonAcademicCollaborations")
    events = db.relationship("Events")
    communications_overview = db.relationship("CommunicationsOverview")
    sfi_funding_ratio = db.relationship("SfiFundingRatio")
    education_public_engagement = db.relationship("EducationPublicEngagement")
    annual_report = db.relationship("AnnualReport")

    #grant_applications = db.relationship("GrantApplications", backref="applicant", lazy="dynamic")

    def __repr__(self):
        return "<User {} {} {} {} {}>".format(self.username, self.orcid, self.is_admin, self.is_reviewer, self.password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://wwww.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class FundingCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rolling = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime)
    # award amount in cents, Euro
    award_amount = db.Column(db.Integer)
    duration = db.Column(db.String(64))

    title = db.Column(db.String(128))
    blurb = db.Column(db.String(1024))
    body = db.Column(db.Text)

    attachments = db.relationship("FundingCallAttachment")
    applications = db.relationship("GrantApplications")
    grants = db.relationship("Grants")


class FundingCallAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey("funding_call.id"))
    name = db.Column(db.String(128))
    path = db.Column(db.String(128))


class GeneralInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="general_information")
    data = db.Column(db.Text)

    def __repr__(self):
        return "<General Information {}>".format(self.id)


class EducationInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<EducationInformation {}>".format(self.data, self.id)

class EmploymentInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<EmploymentInformation {}>".format(self.data, self.id)

class SocietiesInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<SocietiesInformation {}>".format(self.data, self.id)

class AwardsInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<AwardsInformation {}>".format(self.data, self.id)

class FundingDiversification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<FundingDiversification {}>".format(self.data, self.id)

class Impacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<Impacts {}>".format(self.data, self.id)

class InnovationAndCommercialisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<InnovationAndCommercialisation {}>".format(self.data, self.id)

class Presentations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<Presentations {}>".format(self.data, self.id)

class AcademicCollaborations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<AcademicCollaborations {}>".format(self.data, self.id)

class NonAcademicCollaborations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<NonAcademicCollaborations {}>".format(self.data, self.id)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<Events {}>".format(self.data, self.id)

class CommunicationsOverview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<CommunicationsOverview {}>".format(self.data, self.id)


class SfiFundingRatio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<SfiFundingRatio {}>".format(self.data, self.id)

class SfiProposalCalls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #data = db.Column(db.Text)
    title = db.Column(db.Text)
    deadline = db.Column(db.Date)
    contact = db.Column(db.Text)
    overview = db.Column(db.Text)
    funding = db.Column(db.Text)
    key_dates = db.Column(db.Text)
    upload_data = db.Column(db.Text)

    def __repr__(self):
        return "<SfiProposalCalls {}>".format(self.deadline, self.id)

class GrantApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    call_id = db.Column(db.Integer, db.ForeignKey("funding_call.id"))
    title = db.Column(db.Text)
    duration = db.Column(db.Text)
    nrp = db.Column(db.Text)
    ethical_q1 = db.Column(db.Boolean)
    ethical_q2 = db.Column(db.Boolean)
    country = db.Column(db.Text)
    coapps = db.Column(db.Text)
    collabs = db.Column(db.Text)
    legal_align = db.Column(db.Text)
    sci_abstract = db.Column(db.Text)
    lay_abstract = db.Column(db.Text)
    is_draft = db.Column(db.Boolean)
    is_pending = db.Column(db.Boolean)
    is_awarded = db.Column(db.Boolean)

    attachment = db.relationship("GrantApplicationAttachment")

    def __repr__(self):
        return "<GrantApplications {} {} {}>".format(self.id, self.title, self.call_id)


class GrantApplicationAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grant_id = db.Column(db.Integer, db.ForeignKey("grant_applications.id"))
    name = db.Column(db.String(128))
    path = db.Column(db.String(128))


class EducationPublicEngagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data = db.Column(db.Text)

    def __repr__(self):
        return "<EducationPublicEngagement {}>".format(self.data, self.id)


class ResearchGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    users = db.relationship("GroupMembership", back_populates="group")


class GroupMembership(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("research_group.id"), primary_key=True)

    user = db.relationship("User", back_populates="groups")
    group = db.relationship("ResearchGroup", back_populates="users")

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    year = db.Column(db.Integer)
    type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    doi = db.Column(db.String(64))
    title = db.Column(db.Text)
    journal = db.Column(db.Text)

class AnnualReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_submit = db.Column(db.Boolean, default=False)
    date = db.Column(db.String, default=str(datetime.now().year))
    publications_data = db.Column(db.Text)
    edu_pub_engagement = db.Column(db.Text)
    academic_collab = db.Column(db.Text)
    nonacademic_collab = db.Column(db.Text)
    commerc = db.Column(db.Text)
    impact = db.Column(db.Text)
    deviations = db.Column(db.Text)
    highlights = db.Column(db.Text)
    challenges = db.Column(db.Text)
    activities = db.Column(db.Text)

    def __repr__(self):
        return "<AnnualReport {} {} {} {} {} {} {} {} {} {} {} {} {} {}>". \
            format(self.id, self.user_id, self.is_submit, self.date, self.publications_data, self.edu_pub_engagement, self.academic_collab, \
                    self.nonacademic_collab, self.commerc, self.impact, self.deviations, self.highlights, self.challenges, self.activities)
"""
def check_exists(name):
    return User.query.filter_by(username=name).first()

def delete(table, value):
    table.query.filter_by(user_id=value).delete()

def make_general(user_id, first, last, job, pref, suf, phonePref, phone, email, orcid):
    dataJson = {
            "firstName": first,
            "lastName": last,
            "jobTitle": job,
            "prefix": pref,
            "suffix": suf,
            "phoneNumPrefix": phonePref,
            "phoneNum": phone,
            "email": email,
            "orcid": orcid
            }
    data = json.dumps(dataJson)
    r = GeneralInformation(user_id=user_id, data=data)
    db.session.add(r)
    db.session.commit()

def make_education(user_id, degree, fieldOfStudy, institution, location, yearOfDegreeAward):
    dataJson = {
            "degree": degree,
            "fieldOfStudy": fieldOfStudy,
            "institution": institution,
            "location": location,
            "yearOfDegreeAward": yearOfDegreeAward
            }
    data = json.dumps(dataJson)
    r = EducationInformation(user_id=user_id, data=data)
    db.session.add(r)
    db.session.commit()

def make_employment(user_id, company, location, years):
    dataJson = {
            "company": company,
            "location": location,
            "years":  years
            }
    data = json.dumps(dataJson)
    r = EmploymentInformation(user_id=user_id, data=data)
    db.session.add(r)
    db.session.commit()

def make_edupubeng(user_id, nameOfProject, startDate, endDate, activityType, otherType, projectTopic, otherTopic, target, localCountry):
    dataJson = {
            "nameOfProject": nameOfProject,
            "startDate": startDate,
            "endDate": endDate,
            "activityType": activityType,
            "otherType": otherType,
            "projectTopic": projectTopic,
            "otherTopic": otherTopic,
            "target": target,
            "localCountry": localCountry
            }
    data = json.dumps(dataJson)
    r = EducationPublicEngagement(user_id=user_id, data=data)
    db.session.add(r)
    db.session.commit()

def make_user(name, orcid, email, password):
    if check_exists(name):
        q = User.query.filter_by(username=name).delete()
        db.session.commit()
    row = User(orcid=orcid, username=name, email=email)
    row.set_password(password)
    db.session.add(row)
    db.session.commit()

    if GeneralInformation.query.filter_by(user_id=row.id).first() is not None:
        delete(GeneralInformation, row.id)
    make_general(row.id, "Iain", "Felming", "Lecturer", "Dr", "Jr", "+353", "0851111213", "IainFleming@email.com", row.orcid)

    if EducationInformation.query.filter_by(user_id=row.id).first() is not None:
        delete(GeneralInformation, row.id)
    make_education(row.id, "Phd Computer Science", "Artificial Intelligence", "University College Cork", "Cork, Ireland", "2000")

    if EmploymentInformation.query.filter_by(user_id=row.id).first() is not None:
        delete(EmploymentInformation, row.id)
    make_employment(row.id, "University College Cork", "Cork, Ireland", "10")

    if EducationPublicEngagement.query.filter_by(user_id=row.id).first() is not None:
        delete(EducationPublicEngagement, row.id)
    make_edupubeng(row.id, "Artificial Intelligence presentation", "2019-01-01", "2019-01-01", "In-class activities", " ", "Science", " ", "National", "Cork")

if check_exists("admin") is None:
    password = "admin"
    admin = User(id=-1, orcid="0", username="admin", email="admin@admin.com", is_admin=True)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

if check_exists("reviewer") is None:
    password = "reviewer"
    admin = User(id=-2, orcid="-2", username="reviewer", email="reviewer@reviewer.com", is_reviewer=True)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

make_user("IainFelming", "0000-0000-0000-0001", "IainFelming@gmail.com", "test")
make_user("MaryamHines", "0000-0000-0000-0002", "MaryamHines@gmail.com", "test")
make_user("AshantiCresswell", "0000-0000-0000-0003", "AshantiCresswell@gmail.com", "test")
make_user("AprilCooper", "0000-0000-0000-0004", "AprilCooper@gmail.com", "test")
"""
class FundingCallReviewers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey("funding_call.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey("funding_call.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    desc = db.Column(db.Text())
    rating = db.Column(db.Integer)

class Grants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey("funding_call.id"))
    application_id = db.Column(db.Integer, db.ForeignKey("grant_applications.id"))
    title = db.Column(db.Text)
    duration = db.Column(db.Text)

class Collaborators(db.Model):
    grant_id = db.Column(db.Integer, db.ForeignKey("grants.id"), primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"),  primary_key=True)
    is_pi = db.Column(db.Boolean, default=False)
