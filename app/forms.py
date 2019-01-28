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
    submit = SubmitField("Save")

class EducationInformationForm(FlaskForm):
    degree = StringField("Degree", validators=[DataRequired() ])
    fieldOfStudy = StringField("Field of study", validators=[DataRequired() ])
    institution = StringField("Institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    yearOfDegreeAward = DateField("Year of degree award", validators=[DataRequired() ])
    submit = SubmitField("Save")

class EmploymentInformationForm(FlaskForm):
    compnay = StringField("Institution/Company", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    years = StringField("Years", validators=[DataRequired() ])
    submit = SubmitField("Save")

class SocietiesInformationForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    ednDate = DateField("End date", validators=[Optional() ])
    nameOfSociety = StringField("Name of society", validators=[DataRequired() ])
    typeOfMembership = StringField("Type of membership", validators=[DataRequired() ])
    #This field will depend on the date - grey out it end date entered 
    status = SelectField(u"Status(if active)", choices=\
    [("yes", "Yes"), ("no", "No")], validators=[DataRequired() ])
    submit = SubmitField("Save")

class AwardsInformationForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ])
    awardingBody = StringField("Awarding body", validators=[DataRequired() ])
    details = TextAreaField("Details of award", validators = [Length(min=0, max=140), \
    DataRequired() ])
    teamMemberName = StringField("Team member name", validators=[Optional() ])
    submit = SubmitField("Save")

class FundingDiversificationForm(FlaskForm):
    startDate = DateField("Start date", validators=[DataRequired() ])
    ednDate = DateField("End date", validators=[Optional() ])
    amount = StringField("Amount of funding", validators=[DataRequired() ])
    fundingBody = StringField("Funding Body", validators=[DataRequired() ])
    fundingProgramme = StringField("Funding programme", validators=[DataRequired() ])
    status = SelectField(u"Status(if active or expired)", choices=\
    #This field will depend on the date - grey out it end date entered or set to yes
    [("yes", "Yes"), ("no", "No")], validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number to which funding is linked)", \
    validators=[DataRequired() ])

class TeamMembersForm(FlaskForm):
    startDate = DateField("Start date with team", validators=[DataRequired() ])
    departureDate = DateField("Departure date", validators=[DataRequired() ])
    name = StringField("Name", validators=[DataRequired() ])
    position = StringField("Position within the team", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number)", \
    validators=[DataRequired() ])
