from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), \
    EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")
        
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired() ])
    about_me = TextAreaField("About me", validators = [Length(min=0, max=140) ])
    submit = SubmitField("Submit")


class GeneralInformationForm(FlaskForm):
    firstName = StringField("First name", validators=[DataRequired() ])
    lastName = StringField("Last name", validators=[DataRequired() ])
    jobTitle = StringField("Job title", validators=[DataRequired() ])
    prefix = SelectField(u"Prefix", choices=\
    [("dr", "Dr"), ("prof", "Prof"), ("mr", "Mr"), ("mrs", "Mrs"), ("ms", "Ms")], \
    validators=[DataRequired() ])
    suffix = StringField("Suffix", validators=[Optional() ])
    phoneNumPrefix = StringField("Phone prefix", validators=[Optional() ])
    phoneNum = StringField("Phone number", validators=[Optional() ])
    email = StringField("Email address", validators=[DataRequired(), Email() ])
    orcid = StringField("ORCID number", validators=[Optional() ])
    genSubmit = SubmitField("Save")

class EducationInformationForm(FlaskForm):
    degree = StringField("Degree", validators=[DataRequired() ])
    fieldOfStudy = StringField("Field of study", validators=[DataRequired() ])
    institution = StringField("Institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    yearOfDegreeAward = StringField("Year of degree award", validators=[DataRequired() ])
    eduSubmit = SubmitField("Save")

class EmploymentInformationForm(FlaskForm):
    company = StringField("Institution/Company", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    years = StringField("Years", validators=[DataRequired() ])
    employSubmit = SubmitField("Save")

class SocietiesInformationForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[Optional() ])
    nameOfSociety = StringField("Name of society", validators=[DataRequired() ])
    typeOfMembership = StringField("Type of membership", validators=[DataRequired() ])
    #This field will depend on the date - grey out it end date entered 
    status = SelectField(u"Status(if active)", choices=\
    [("yes", "Yes"), ("no", "No")], validators=[DataRequired() ])
    socSubmit = SubmitField("Save")
    
class AwardsInformationForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ])
    awardingBody = StringField("Awarding body", validators=[DataRequired() ])
    details = TextAreaField("Details of award", validators = [Length(min=0, max=140), \
    DataRequired() ])
    teamMemberName = StringField("Team member name", validators=[Optional() ])
    awardsSubmit = SubmitField("Save")

class FundingDiversificationForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[Optional() ])
    amount = StringField("Amount of funding", validators=[DataRequired() ])
    fundingBody = StringField("Funding Body", validators=[DataRequired() ])
    fundingProgramme = StringField("Funding programme", validators=[DataRequired() ])
    status = SelectField(u"Status(if active or expired)", choices=\
    #This field will depend on the date - grey out it end date entered or set to yes
    [("yes", "Yes"), ("no", "No")], validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number to which funding is linked)", \
    validators=[DataRequired() ])
    fundingDivSubmit = SubmitField("Save")

class TeamMembersForm(FlaskForm):
    startDate = DateField("Start date with team", validators=[DataRequired() ])
    departureDate = DateField("Departure date", validators=[DataRequired() ])
    name = StringField("Name", validators=[DataRequired() ])
    position = StringField("Position within the team", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number)", \
    validators=[DataRequired() ])
    teamMemSubmit = SubmitField("Save")

class ImpactsForm(FlaskForm):
    title = StringField("Impact title", validators=[DataRequired() ])
    category = StringField("Impact category", validators=[DataRequired() ])
    primaryBeneficiary = StringField("Primary beneficiary", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    impactsSubmit = SubmitField("Save")

class InnovationAndCommercialisationForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ])
    type = StringField("Type", validators=[DataRequired() ])
    title = StringField("Title", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    innovSubmit = SubmitField("Save")

class PublicationsForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ])
    type = SelectField(u"Type", choices=\
    [("originalArticle", "Refereed original article"), \
    ("reviewArticle", "Refereed review article"), \
    ("conferencePaper", "Refereed conference paper"), \
    ("book", "Book"), ("technicalReport", "Technical report")], \
    validators=[DataRequired() ])
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    name = TextAreaField("Journal / Conference name", \
    validators = [Length(min=0, max=140) ])
    publicationStatus = SelectField(u"Publication status", \
    choices=[("published", "Published"), ("inPress", "In press")], \
    validators=[DataRequired() ])
    doi = StringField("DOI", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    pubSubmit = SubmitField("Save")

class PresentationsForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ])
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    eventType = SelectField(u"Event Type", choices=\
    [("conference", "Conference"), ("seminar", "Invited seminar"), \
    ("keynote", "Keynote")], validators=[DataRequired() ])
    organisingBody = StringField("Organising Body", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    presSubmit = SubmitField("Save")

class AcademicCollaborationsForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[DataRequired()])
    nameOfInstitution = StringField("Name of institution", validators=[DataRequired() ])
    department =  StringField("Department within institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    nameOfCollaborator = StringField("Name of collaborator", validators=[DataRequired() ])
    goal = SelectField(u"Primary goal of collaboration", choices=\
    [("access", "Access to software/data/material/equipment"), \
    ("training", "Training and career development"), \
    ("publication", "Joint publication"), ("startup", "Startup development"), \
    ("license", "License development"), \
    ("building", "Building networks & relationships")], validators=[DataRequired() ])
    frequency = StringField("Frequency of interaction", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    academicCollabsSubmit = SubmitField("Save")

class NonAcademicCollaborationsForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[DataRequired()])
    nameOfInstitution = StringField("Name of institution", validators=[DataRequired() ])
    department =  StringField("Department within institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    nameOfCollaborator = StringField("Name of collaborator", validators=[DataRequired() ])
    goal = SelectField(u"Primary goal of collaboration", choices=\
    [("access", "Access to software/data/material/equipment"), \
    ("training", "Training and career development"), \
    ("publication", "Joint publication"), ("startup", "Startup development"), \
    ("license", "License development"), \
    ("building", "Building networks & relationships")], validators=[DataRequired() ])
    frequency = StringField("Frequency of interaction", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    nonAcademicCollabsSubmit = SubmitField("Save")

class EventsForms(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[DataRequired() ])
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    eventType = SelectField(u"Event Type", choices=\
    [("conference", "Conference"), ("workshop", "Workshop"), \
    ("seminar", "Seminar")], validators=[DataRequired() ])
    role = StringField("Role",validators=[DataRequired() ])
    location = StringField("Location of event", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    eventsSubmit = SubmitField("Save")

class CommunicationsOverviewForm(FlaskForm):
    #total interaction per year
    year = StringField("Year", validators=[DataRequired() ])
    numberOfLectures = StringField("Number of public lectures/demonstrations", validators=[DataRequired() ])
    numberOfVisits = StringField("Number of visits", validators=[DataRequired() ])
    numberOfMediaInteracations = StringField("Number of media interactions", validators=[DataRequired() ])
    commSubmit = SubmitField("Save")

class SfiFundingRatioForm(FlaskForm):
    #once per year
    year = StringField("Year", validators=[DataRequired() ])
    # @TODO: should this be a dropdown of 0,20,40 etc.?
    percentage = StringField("Indicates percentage of time spent on SFI-funded projects, in steps of 20%", \
    validators=[DataRequired() ])
    sfiFundingRatioSubmit = SubmitField("Save")

class EducationAndPublicEngagementForm(FlaskForm):
    nameOfProject = TextAreaField("Name of project", \
    validators = [Length(min=0, max=140) ])
    startDate = DateField("Start date", validators=[DataRequired() ])
    endDate = DateField("End date", validators=[DataRequired()])
    activityType = SelectField(u"Activity type", choices=\
    [("event", "Public event"), ("class", "In-class activities"), \
    ("programme", "Career experience programme"), ("other", "Other(please specify")], \
    validators=[DataRequired() ])
    otherType = StringField("If other selected", validators=[Optional() ])
    projectTopic = SelectField(u"Project topic", choices=\
    [("science", "Science"), ("math", "Math"), \
    ("engineering", "Engineering"), ("technology", "Technology"), \
    ("space", "Space related"), ("other", "Other(please specify")], \
    validators=[DataRequired() ])
    otherTopic = StringField("If other selected", validators=[Optional() ])
    target = SelectField(u"Target geographical area", choices=\
    [("local", "Local (a specific county in Ireland)"), ("national", "National"), \
    ("international", "International")], \
    validators=[DataRequired() ])
    localCountry = StringField("If local (a specific county in Ireland)", validators=[Optional() ])
    pubEngageSubmit = SubmitField("Save")

