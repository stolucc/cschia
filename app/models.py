from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from app import app

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcid = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
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

    def __repr__(self):
        return "<User {} {}>".format(self.username, self.orcid)

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
