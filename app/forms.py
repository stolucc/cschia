from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, \
TextAreaField, IntegerField, SelectField, DateField, FieldList, FormField, MultipleFileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, \
Optional
from app.models import User

#Account forms
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    orcid = StringField("Orcid number", validators=[DataRequired() ])
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

    def validate_orcid(self, orcid):
        user = User.query.filter_by(orcid=orcid.data).first()
        if user is not None:
            raise ValidationError("An account with this orcid number already exists.")

class UpgradeUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    Admin = BooleanField("Admin")
    Reviewer = BooleanField("Reviewer")
    HostI = BooleanField("Host Institution")
    
    submit = SubmitField("Change Account Type")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email doesnt exist.")


class RegistrationFormAdmin(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    orcid = StringField("Orcid number", validators=[DataRequired() ])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), \
    EqualTo("password")])
    prefix = SelectField(u"Account Type", choices=\
    [("SFI ADMIN", "SFI ADMIN"), ("Reviewer", "Reviewer"), ("Researcher", "Researcher")], \
    validators=[DataRequired() ])

    submit = SubmitField("Register")

    def validate_usernameAdmin(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_emailAdmin(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")

    def validate_orcidAdmin(self, orcid):
        user = User.query.filter_by(orcid=orcid.data).first()
        if user is not None:
            raise ValidationError("An account with this orcid number already exists.")

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired() ])
    about_me = TextAreaField("About me", validators = [Length(min=0, max=140) ])
    submit = SubmitField("Submit")

class ChangePassword(FlaskForm):
    # oldPassword = StringField("Old password", validators=[DataRequired() ])
    newPassword1 = PasswordField("New password", validators=[DataRequired() ])
    newPassword2 = PasswordField("Repeat new password", validators=[DataRequired(), EqualTo("newPassword1") ])
    passSubmit = SubmitField("Change password")

class ChangeEmail(FlaskForm):
    # oldEmail = StringField("Old email", validators=[DataRequired(), Email()])
    newEmail1 = StringField("New email", validators=[DataRequired() ])
    newEmail2 = StringField("Repeat new email", validators=[DataRequired(), EqualTo("newEmail1")])
    emailSubmit = SubmitField("Change email")

    """
    def validate_newEmail1(self, newEmail1):
        user = User.query.filter_by(email=newEmail1.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")

    def validate_newEmail2(self, newEmail2):
        user = User.query.filter_by(email=newEmail2.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")
    """

# Edit profile forms

class GeneralInformationForm(FlaskForm):
    firstName = StringField("First name", validators=[DataRequired()])
    lastName = StringField("Last name", validators=[DataRequired() ])
    jobTitle = StringField("Job title", validators=[DataRequired() ])
    prefix = SelectField(u"Prefix", choices=\
    [("Dr", "Dr"), ("Prof", "Prof"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Ms", "Ms")], \
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
    yearOfDegreeAward = StringField("Year of degree award", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    eduSubmit = SubmitField("Add new")
    eduEdit = SubmitField("Update")

class EmploymentInformationForm(FlaskForm):
    company = StringField("Institution/Company", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    years = StringField("Years", validators=[DataRequired() ])
    employSubmit = SubmitField("Add new")
    employEdit = SubmitField("Update")

class SocietiesInformationForm(FlaskForm):
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[Optional() ], render_kw={"placeholder": "YYYY-MM-DD"})
    nameOfSociety = StringField("Name of society", validators=[DataRequired() ])
    typeOfMembership = StringField("Type of membership", validators=[DataRequired() ])
    #This field will depend on the date - grey out it end date entered
    status = SelectField(u"Status(if active)", choices=\
    [("Yes", "Yes"), ("No", "No")], validators=[DataRequired() ])
    socSubmit = SubmitField("Add new")
    socEdit = SubmitField("Update")

class AwardsInformationForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    awardingBody = StringField("Awarding body", validators=[DataRequired() ])
    details = TextAreaField("Details of award", validators = [Length(min=0, max=140), \
    DataRequired() ])
    teamMemberName = StringField("Team member name", validators=[Optional() ])
    awardsSubmit = SubmitField("Add new")
    awardsEdit = SubmitField("Update")

class FundingDiversificationForm(FlaskForm):
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[Optional() ], render_kw={"placeholder": "YYYY-MM-DD"})
    amount = StringField("Amount of funding", validators=[DataRequired() ])
    fundingBody = StringField("Funding Body", validators=[DataRequired() ])
    fundingProgramme = StringField("Funding programme", validators=[DataRequired() ])
    status = SelectField(u"Status(if active or expired)", choices=\
    #This field will depend on the date - grey out it end date entered or set to yes
    [("Yes", "Yes"), ("No", "No")], validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number to which funding is linked)", \
    validators=[DataRequired() ])
    fundingDivSubmit = SubmitField("Add new")
    fundingDivEdit = SubmitField("Update")

class TeamMembersForm(FlaskForm):
    startDate = StringField("Start date with team", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    departureDate = StringField("Departure date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    name = StringField("Name", validators=[DataRequired() ])
    position = StringField("Position within the team", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution(grant number)", \
    validators=[DataRequired() ])
    teamMemSubmit = SubmitField("Add new")
    teamMemEdit = SubmitField("Update")

class ImpactsForm(FlaskForm):
    title = StringField("Impact title", validators=[DataRequired() ])
    category = StringField("Impact category", validators=[DataRequired() ])
    primaryBeneficiary = StringField("Primary beneficiary", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    impactsSubmit = SubmitField("Add new")
    impactsEdit = SubmitField("Update")

class InnovationAndCommercialisationForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    type = StringField("Type", validators=[DataRequired() ])
    title = StringField("Title", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    innovSubmit = SubmitField("Add new")
    innovEdit = SubmitField("Update")

class PublicationsForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    type = SelectField(u"Type", choices=\
    [("Refereed original article", "Refereed original article"), \
    ("Refereed review article", "Refereed review article"), \
    ("Refereed conference paper", "Refereed conference paper"), \
    ("Book", "Book"), ("Technical report", "Technical report")], \
    validators=[DataRequired() ])
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    name = TextAreaField("Journal / Conference name", \
    validators = [Length(min=0, max=140) ])
    publicationStatus = SelectField(u"Publication status", \
    choices=[("Published", "Published"), ("In press", "In press")], \
    validators=[DataRequired() ])
    doi = StringField("DOI", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    pubSubmit = SubmitField("Add new")
    pubEdit = SubmitField("Update")

class PresentationsForm(FlaskForm):
    year = StringField("Year", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    eventType = SelectField(u"Event Type", choices=\
    [("Conference", "Conference"), ("Invited seminar", "Invited seminar"), \
    ("Keynote", "Keynote")], validators=[DataRequired() ])
    organisingBody = StringField("Organising Body", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    presSubmit = SubmitField("Add new")
    presEdit = SubmitField("Update")

class AcademicCollaborationsForm(FlaskForm):
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    nameOfInstitution = StringField("Name of institution", validators=[DataRequired() ])
    department =  StringField("Department within institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    nameOfCollaborator = StringField("Name of collaborator", validators=[DataRequired() ])
    goal = SelectField(u"Primary goal of collaboration", choices=\
    [("Access to software/data/material/equipment", "Access to software/data/material/equipment"), \
    ("Training and career development", "Training and career development"), \
    ("Joint publication", "Joint publication"), ("Startup development", "Startup development"), \
    ("License development", "License development"), \
    ("Building networks & relationships", "Building networks & relationships")], validators=[DataRequired() ])
    frequency = StringField("Frequency of interaction", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    academicCollabsSubmit = SubmitField("Add new")
    academicCollabsEdit = SubmitField("Update")

class NonAcademicCollaborationsForm(FlaskForm):
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    nameOfInstitution = StringField("Name of institution", validators=[DataRequired() ])
    department =  StringField("Department within institution", validators=[DataRequired() ])
    location = StringField("Location", validators=[DataRequired() ])
    nameOfCollaborator = StringField("Name of collaborator", validators=[DataRequired() ])
    goal = SelectField(u"Primary goal of collaboration", choices=\
    [("Access to software/data/material/equipment", "Access to software/data/material/equipment"), \
    ("Training and career development", "Training and career development"), \
    ("Joint publication", "Joint publication"), ("Startup development", "Startup development"), \
    ("License development", "License development"), \
    ("Building networks & relationships", "Building networks & relationships")], validators=[DataRequired() ])
    frequency = StringField("Frequency of interaction", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    nonAcademicCollabsSubmit = SubmitField("Add new")
    nonAcademicCollabsEdit = SubmitField("Update")

class EventsForms(FlaskForm):
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    title = TextAreaField("Title", validators = [Length(min=0, max=140) ])
    eventType = SelectField(u"Event Type", choices=\
    [("Conference", "Conference"), ("Workshop", "Workshop"), \
    ("Seminar", "Seminar")], validators=[DataRequired() ])
    role = StringField("Role",validators=[DataRequired() ])
    location = StringField("Location of event", validators=[DataRequired() ])
    primaryAttribution = StringField("Primary attribution", validators=[DataRequired() ])
    eventsSubmit = SubmitField("Add new")
    eventsEdit = SubmitField("Update")

class CommunicationsOverviewForm(FlaskForm):
    #total interaction per year
    year = StringField("Year", validators=[DataRequired() ], render_kw={"placeholder": "YYYY"})
    numberOfLectures = StringField("Number of public lectures/demonstrations", validators=[DataRequired() ])
    numberOfVisits = StringField("Number of visits", validators=[DataRequired() ])
    numberOfMediaInteracations = StringField("Number of media interactions", validators=[DataRequired() ])
    commSubmit = SubmitField("Add new")
    commEdit = SubmitField("Update")

class SfiFundingRatioForm(FlaskForm):
    #once per year
    year = StringField("Year", validators=[DataRequired() ])
    # @TODO: should this be a dropdown of 0,20,40 etc.?
    percentage = StringField("Indicates percentage of time spent on SFI-funded projects, in steps of 20%", \
    validators=[DataRequired() ])
    sfiFundingRatioSubmit = SubmitField("Add new")
    sfiFundingRatioEdit = SubmitField("Update")

class ProposalForm(FlaskForm):
    deadline = DateField("Deadline", render_kw={"placeholder": "YYYY-MM-DD"})
    contact = StringField("Contact")
    title = TextAreaField("Title", validators = [Length(min=0,max=128)])
    overview = TextAreaField("Overview", validators = [Length(min=0,max=1500)])
    funding = TextAreaField("Funding", validators = [Length(min=0,max=1500)])
    key_dates = TextAreaField("Key Dates", validators = [Length(min=0,max=1500)])
    file_upload = FileField("Key Files")
    submit = SubmitField("Submit")



class EditProposalForm(FlaskForm):
    deadline = DateField("Deadline", render_kw={"placeholder": "YYYY-MM-DD"})
    contact = StringField("Contact")
    title = TextAreaField("Title", validators = [Length(min=0,max=128)])
    overview = TextAreaField("Overview", validators = [Length(min=0,max=1500)])
    funding = TextAreaField("Funding", validators = [Length(min=0,max=1500)])
    key_dates = TextAreaField("Key Dates", validators = [Length(min=0,max=1500)])
    file_upload = FileField("Key Files")
    submit = SubmitField("Edit")

class EducationAndPublicEngagementForm(FlaskForm):
    nameOfProject = TextAreaField("Name of project", \
    validators = [Length(min=0, max=140) ])
    startDate = StringField("Start date", validators=[DataRequired() ], render_kw={"placeholder": "YYYY-MM-DD"})
    endDate = StringField("End date", validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    activityType = SelectField(u"Activity type", choices=\
    [("Public event", "Public event"), ("In-class activities", "In-class activities"), \
    ("Career experience programme", "Career experience programme"), ("Other (please specify)", "Other (please specify)")], \
    validators=[DataRequired() ])
    otherType = StringField("If other selected", validators=[Optional() ])
    projectTopic = SelectField(u"Project topic", choices=\
    [("Science", "Science"), ("Math", "Math"), \
    ("Engineering", "Engineering"), ("Technology", "Technology"), \
    ("Space related", "Space related"), ("Other (please specify)", "Other (please specify)")], \
    validators=[DataRequired() ])
    otherTopic = StringField("If other selected", validators=[Optional() ])
    target = SelectField(u"Target geographical area", choices=\
    [("Local (a specific county in Ireland)", "Local (a specific county in Ireland)"), ("National", "National"), \
    ("International", "International")], \
    validators=[DataRequired() ])
    localCountry = StringField("If local (a specific county in Ireland)", validators=[Optional() ])
    pubEngageSubmit = SubmitField("Add new")
    pubEngageEdit = SubmitField("Update")

class FreeTextForm(FlaskForm):
    deviations = TextAreaField("Please indicate any deviations of the originally \
        approved research plan", validators = [Length(min=0,max=1000)])
    highlight1 = TextAreaField("Please bullet point one of the most important \
        research highlights from the reporting period", \
        validators = [Length(min=0,max=200)])
    highlight2 = TextAreaField("Please bullet point one of the most important \
        research highlights from the reporting period", \
         validators = [Length(min=0,max=200)])
    highlight3 = TextAreaField("Please bullet point one of the most important research \
        highlights from the reporting period", validators = [Length(min=0,max=200)])
    challenges = TextAreaField("Please bullet point any challenges encountered \
        during the reporting period", validators = [Length(min=0,max=200)])
    activities = TextAreaField("Please bullet point the planned activities for \
        the coming year (200 word limit)", validators = [Length(min=0,max=200)])
    #freeTextDraft = SubmitField("Save draft")
    #freeTextEdit = SubmitField("Edit")
    #freeTextPreview = SubmitField("Preview")
    freeTextSubmit = SubmitField("Add new")

class ReviewProposalForm(FlaskForm):
    description = TextAreaField("Description", validators = [Length(min=0,max=1500)])
    rating = SelectField(u"Rating", choices=\
    [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")], \
    validators=[DataRequired() ])
    submit = SubmitField("Submit")

class AddReviewerForm(FlaskForm):
    reviewer_username = StringField("Reviewer Email", validators=[DataRequired() ])
    submit = SubmitField("Add")

class CollaboratorForm(FlaskForm):
    name = StringField("Name")
    org = StringField("Organization")
    email = StringField("Email")

class GrantApplicationForm(FlaskForm):
    title = StringField("Proposal Title")
    duration = StringField("Duration of award")
    nrp = SelectField(u"National Research Priority", choices=\
            [("PAA","Priority Area A - Future Networks & Communications"), \
            ("PAB","Priority Area B - DataAnalytics, Management, Security & Privacy"), \
            ("PAC","Priority Area C - Digital Platforms, Content & Applications"), \
            ("PAD","Priority Area D - Connected Health and Independent Living"), \
            ("PAE","Priority Area E - Medical Devices"),("PAF","Priority Area F - Diagnostics"), \
            ("PAG","Priority Area G - Therapeutics: Synthesis, Formulation, Processsing and Drug Delivery"), \
            ("PAH","Priority Area H - Food for Health"), \
            ("PAI","Priority Level I - Sustainable Food Production and Processing"), \
            ("PAJ","Priority Area J - Marine Renewable Energy"), \
            ("PAK","Priority Area K - Smart Grids & Smart Cities"), \
            ("PAL","Priority Area L - Manufacturing Competitiveness"), \
            ("PAM","Priority Area M - Processing Technologies and Novel Materials"), \
            ("PAN","Priority Area N - Innovation in Services and Business Processes"),\
            ("Software","Software"),("Other","Other")])
    legal_align = TextAreaField("Please describe how your proposal is aligned with SFI's legal remit (max 250 words)", validators = [Length(min=0,max=250)])
    ethical_q1 = SelectField(u"Does the research involve the use of animals?", choices=[("No","No"),("Yes","Yes")])
    ethical_q2 = SelectField(u"Does the research involve human participants, human biological material, or identifiable data?", choices=[("No","No"),("Yes","Yes")])
    country = StringField("Country of applicant")
    coapps = TextAreaField("Coapplicants(eg. applicant1@email.com, applicant2@email.com)", validators=[Length(min=0,max=200)])
    # collabs = FieldList(FormField(CollaboratorForm), min_entries=2)
    sci_abstract = TextAreaField("Scientific Abstract", validators=[Length(min=0,max=200)])
    lay_abstract = TextAreaField("Lay Abstract", validators=[Length(min=0,max=200)])
    doc_uplaod = MultipleFileField("Programme Documents")
    declare = BooleanField()
    submit = SubmitField("Submit")
    draft = SubmitField("Save Draft")

class AddCollaboratorForm(FlaskForm):
    email = StringField("Researcher's email", validators=[DataRequired() ])
    is_pi = SelectField(u"PI", choices=[("no","No"),("yes","Yes")])
    submit = SubmitField("Add collaborator")

class PublicationForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    doi = StringField("DOI")
    year = IntegerField("Year of Publication", validators=[DataRequired()], render_kw={"placeholder": "YYYY"})
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
    pubsubmit = SubmitField("Submit")

class BibtexPublicationForm(FlaskForm):
    parse = TextAreaField("BIBTex format", validators=[DataRequired(), Length(min=0,max=800)], \
        render_kw={"placeholder": """@(Refereed original article|Refereed review article|Refereed conference paper|Book|Technical report)Refereed original article { 
                        title = {The ABC of Software Engineering Research},
                        doi = {10.1145/3241743},
                        year = {2018},
                        journal =  {ACM Transactions on Software Engineering and Methodology},
                        status(Published|In-press) = {Published}
                    }"""})
    submitBib = SubmitField("Submit")

class FullSearchForm(FlaskForm):
    choices=[('Proposal','Proposal'),
             ('User','User'),
             ('Orcid','Orcid')]
    select=SelectField('What you want search?', choices=choices)
    search=StringField('')