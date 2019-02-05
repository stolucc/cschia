from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, GeneralInformationForm, \
EducationInformationForm, EmploymentInformationForm, \
SocietiesInformationForm, AwardsInformationForm, \
FundingDiversificationForm, TeamMembersForm, ImpactsForm, \
InnovationAndCommercialisationForm, PublicationsForm, \
PresentationsForm, AcademicCollaborationsForm, NonAcademicCollaborationsForm, \
EventsForms, CommunicationsOverviewForm, SfiFundingRatioForm, EducationAndPublicEngagementForm
from app.models import User, GeneralInformation, EducationInformation, EmploymentInformation, \
SocietiesInformation, AwardsInformation, FundingDiversification, Impacts, InnovationAndCommercialisation, \
Publications, Presentations, AcademicCollaborations, NonAcademicCollaborations, Events, \
CommunicationsOverview, SfiFundingRatio, EducationPublicEngagement
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import json

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

#not needed
#@app.route("/")
@app.route("/index")
@login_required

def index():
    user = {"username": "Miguel"}
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!"
        },
        {
            "author" : {"username" : "Susan"},
            "body" : "The avengers movie was so cool!"
        }
        
        ]
    return render_template("index.html", title="Home ", posts=posts)

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

#not needed
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/admin_register_user", methods=["GET", "POST"])
def admin_register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, You Have Now Registered a User!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

#not needed
@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"}
    ]
    return render_template("user.html", user=user, posts=posts)

@app.route("/profile", methods=["GET"])
@login_required
def show_profile():
    check_if_exists = GeneralInformation.query.filter_by(user_id=current_user.id).first()

    return render_template("profile.html", title="View Profile", info=check_if_exists)

def get_list(q):
    lst = []
    for item in q:
        lst.append(json.loads(item.data))
    return lst

@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    genInfoForm = GeneralInformationForm()
    eduForm = EducationInformationForm()
    employForm = EmploymentInformationForm()
    socForm = SocietiesInformationForm()
    awardsForm = AwardsInformationForm()
    fundingDivForm = FundingDiversificationForm()
    teamMemForm = TeamMembersForm()
    impactsForm = ImpactsForm()
    innovForm = InnovationAndCommercialisationForm()
    pubForm = PublicationsForm()
    presForm = PresentationsForm()
    academicCollabsForm = AcademicCollaborationsForm()
    nonAcademicCollabsForm = NonAcademicCollaborationsForm()
    eventsForm = EventsForms()
    commForm = CommunicationsOverviewForm()
    fundRatioForm = SfiFundingRatioForm()
    pubEngageForm = EducationAndPublicEngagementForm()

    jsonGenInfo = GeneralInformation.query.filter_by(user_id=current_user.id).first()
    if jsonGenInfo is not None:
        getGenInfo = json.loads(jsonGenInfo.data)
    else:
        getGenInfo = ""

    jsonEduInfo = EducationInformation.query.filter_by(user_id=current_user.id).all()
    getEduInfo = get_list(jsonEduInfo)
    
    jsonEmployInfo = EmploymentInformation.query.filter_by(user_id=current_user.id).all()
    getEmployInfo = get_list(jsonEmployInfo)

    jsonSocInfo = SocietiesInformation.query.filter_by(user_id=current_user.id).all()
    getSocInfo = get_list(jsonSocInfo)

    jsonAwardInfo = AwardsInformation.query.filter_by(user_id=current_user.id).all()
    getAwardInfo = get_list(jsonAwardInfo)

    jsonFundInfo = FundingDiversification.query.filter_by(user_id=current_user.id).all()
    getFundInfo = get_list(jsonFundInfo)
    
    jsonImpInfo = Impacts.query.filter_by(user_id=current_user.id).all()
    getImpInfo = get_list(jsonImpInfo)

    jsonInnInfo = InnovationAndCommercialisation.query.filter_by(user_id=current_user.id).all()
    getInnInfo = get_list(jsonInnInfo)

    jsonPubInfo = Publications.query.filter_by(user_id=current_user.id).all()
    getPubInfo = get_list(jsonPubInfo)

    jsonPresInfo = Presentations.query.filter_by(user_id=current_user.id).all()
    getPresInfo = get_list(jsonPresInfo)

    jsonAcInfo = AcademicCollaborations.query.filter_by(user_id=current_user.id).all()
    getAcInfo = get_list(jsonAcInfo)

    jsonNonAcInfo = NonAcademicCollaborations.query.filter_by(user_id=current_user.id).all()
    getNonAcInfo = get_list(jsonNonAcInfo)

    jsonEvInfo = Events.query.filter_by(user_id=current_user.id).all()
    getEvInfo = get_list(jsonEvInfo)

    jsonCommInfo = CommunicationsOverview.query.filter_by(user_id=current_user.id).all()
    getCommInfo = get_list(jsonCommInfo)

    jsonSfiInfo = SfiFundingRatio.query.filter_by(user_id=current_user.id).all()
    getSfiInfo = get_list(jsonSfiInfo)

    jsonEdInfo = EducationPublicEngagement.query.filter_by(user_id=current_user.id).all()
    getEdInfo = get_list(jsonEdInfo)

    
    
    if request.method == "POST":

        if genInfoForm.validate_on_submit and "genSubmit" in request.form:

            check_if_exists = GeneralInformation.query.filter_by(user_id=current_user.id).first()

            info = {
                    "firstName" : genInfoForm.firstName.data,
                    "lastName" : genInfoForm.lastName.data,
                    "jobTitle" : genInfoForm.jobTitle.data,
                    "prefix" : genInfoForm.prefix.data, 
                    "suffix" : genInfoForm.suffix.data,
                    "phoneNumPrefix" : genInfoForm.phoneNumPrefix.data,
                    "phoneNum" : genInfoForm.phoneNum.data,
                    "email" : genInfoForm.email.data,
                    "orcid" : genInfoForm.orcid.data
                }

            infoJson = json.dumps(info)

            if check_if_exists is None:
                userInfo = GeneralInformation(user_id=current_user.id)
                db.session.add(userInfo)
            
                userInfo.data = infoJson
            else:
                check_if_exists.data = infoJson

            db.session.commit()
            flash("changes saved")
        
        #elif "genShow" in request:
        #    flash(request)
           
        elif eduForm.validate_on_submit and "eduSubmit" in request.form:
           
            userInfo = EducationInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "degree" : eduForm.degree.data,
                "fieldOfStudy" : eduForm.fieldOfStudy.data,
                "institution" : eduForm.institution.data,
                "location" : eduForm.location.data, 
                "yearOfDegreeAward" : eduForm.yearOfDegreeAward.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif employForm.validate_on_submit and "employSubmit" in request.form: 
            
            userInfo = EmploymentInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "company" : employForm.company.data,
                "location" : employForm.location.data,
                "years" : employForm.years.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif socForm.validate_on_submit and "socSubmit" in request.form:
            
            userInfo = SocietiesInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate" : socForm.startDate.data,
                "endDate" : socForm.endDate.data,
                "nameOfSociety" : socForm.nameOfSociety.data,
                "typeOfMembership" : socForm.typeOfMembership.data, 
                "status" : socForm.status.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif awardsForm.validate_on_submit and "awardsSubmit" in request.form:
            
            userInfo = AwardsInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : awardsForm.year.data,
                "awardingBody" : awardsForm.awardingBody.data,
                "details" : awardsForm.details.data,
                "teamMemberName" : awardsForm.teamMemberName.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif fundingDivForm.validate_on_submit and "fundingDivSubmit" in request.form:
            
            userInfo = FundingDiversification(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate" : fundingDivForm.startDate.data,
                "endDate" : fundingDivForm.endDate.data,
                "amount" : fundingDivForm.amount.data,
                "fundingBody" : fundingDivForm.fundingBody.data, 
                "fundingProgramme" : fundingDivForm.fundingProgramme.data,
                "status" : fundingDivForm.status.data,
                "primaryAttribution" : fundingDivForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif teamMemForm.validate_on_submit and "teamMemSubmit" in request.form:
            flash("testSuccessTea")

        elif impactsForm.validate_on_submit and  "impactsSubmit" in request.form:

            userInfo = Impacts(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "title" : impactsForm.title.data,
                "category" : impactsForm.category.data,
                "primaryBeneficiary" : impactsForm.primaryBeneficiary.data,
                "primaryAttribution" : impactsForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif innovForm.validate_on_submit and "innovSubmit" in request.form:
            
            userInfo = InnovationAndCommercialisation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : innovForm.year.data,
                "type" : innovForm.type.data,
                "title" : innovForm.title.data,
                "primaryAttribution" : innovForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif pubForm.validate_on_submit and "pubSubmit" in request.form:
            
            userInfo = Publications(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : pubForm.year.data,
                "type" : pubForm.type.data,
                "title" : pubForm.title.data,
                "name" : pubForm.name.data,
                "publicationStatus" : pubForm.publicationStatus.data,
                "doi" : pubForm.doi.data,
                "primaryAttribution" : pubForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif presForm.validate_on_submit and "presSubmit" in request.form:
            
            userInfo = Presentations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : presForm.year.data,
                "title" : presForm.title.data,
                "eventType" : presForm.eventType.data,
                "organisingBody" : presForm.organisingBody.data,
                "location" : presForm.location.data,
                "primaryAttribution" : presForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif academicCollabsForm.validate_on_submit and "academicCollabsSubmit" in request.form:
            
            userInfo = AcademicCollaborations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate" : academicCollabsForm.startDate.data,
                "endDate" : academicCollabsForm.endDate.data,
                "nameOfInstitution" : academicCollabsForm.nameOfInstitution.data,
                "department" : academicCollabsForm.department.data,
                "location" : academicCollabsForm.location.data,
                "nameOfCollaborator" : academicCollabsForm.nameOfCollaborator.data,
                "goal" : academicCollabsForm.goal.data,
                "frequency" : academicCollabsForm.frequency.data,
                "primaryAttribution" : academicCollabsForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif nonAcademicCollabsForm.validate_on_submit and "nonAcademicCollabsSubmit" in request.form:
            
            userInfo = NonAcademicCollaborations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate" : nonAcademicCollabsForm.startDate.data,
                "endDate" : nonAcademicCollabsForm.endDate.data,
                "nameOfInstitution" : nonAcademicCollabsForm.nameOfInstitution.data,
                "department" : nonAcademicCollabsForm.department.data,
                "location" : nonAcademicCollabsForm.location.data,
                "nameOfCollaborator" : nonAcademicCollabsForm.nameOfCollaborator.data,
                "goal" : nonAcademicCollabsForm.goal.data,
                "frequency" : nonAcademicCollabsForm.frequency.data,
                "primaryAttribution" : nonAcademicCollabsForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif eventsForm.validate_on_submit and  "eventsSubmit" in request.form:
            
            userInfo = Events(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate" : eventsForm.startDate.data,
                "endDate" : eventsForm.endDate.data,
                "title" : eventsForm.title.data,
                "eventType" : eventsForm.eventType.data,
                "role" : eventsForm.role.data,
                "location" : eventsForm.location.data,
                "primaryAttribution" : eventsForm.primaryAttribution.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")
  
        elif commForm.validate_on_submit and "commSubmit" in request.form:
        
            userInfo = CommunicationsOverview(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : commForm.year.data,
                "numberOfLectures" : commForm.numberOfLectures.data,
                "numberOfVisits" : commForm.numberOfVisits.data,
                "numberOfMediaInteracations" : commForm.numberOfMediaInteracations.data
            }
        
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif fundRatioForm.validate_on_submit and "sfiFundingRatioSubmit" in request.form:
           
            userInfo = SfiFundingRatio(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year" : fundRatioForm.year.data,
                "percentage" : fundRatioForm.percentage.data
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")

        elif pubEngageForm.validate_on_submit and "pubEngageSubmit" in request.form:
           
            userInfo = EducationPublicEngagement(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "nameOfProject" : pubEngageForm.nameOfProject.data,
                "startDate" : pubEngageForm.startDate.data,
                "endDate" : pubEngageForm.endDate.data,
                "activityType" : pubEngageForm.activityType.data,
                "otherType" : pubEngageForm.otherType.data,
                "projectTopic" : pubEngageForm.projectTopic.data,
                "otherTopic" : pubEngageForm.otherTopic.data,
                "target" : pubEngageForm.target.data, 
                "localCountry" : pubEngageForm.localCountry.data, 
            }
         
            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("changes saved")
        
        return redirect(url_for("edit_profile"))


    
    return render_template("edit_profile.html",
                            title="Edit Profile",
                            genInfoForm=genInfoForm,
                            eduForm=eduForm,
                            employForm=employForm,
                            socForm=socForm,
                            awardsForm=awardsForm,
                            fundingDivForm=fundingDivForm,
                            teamMemForm=teamMemForm,
                            impactsForm=impactsForm,
                            innovForm=innovForm,
                            pubForm=pubForm,
                            presForm=presForm,
                            academicCollabsForm=academicCollabsForm,
                            nonAcademicCollabsForm=nonAcademicCollabsForm,
                            eventsForm=eventsForm,
                            commForm=commForm,
                            fundRatioForm=fundRatioForm,
                            pubEngageForm=pubEngageForm,
                            
                            getGenInfo=getGenInfo,
                            getEduInfo=getEduInfo,
                            getEmployInfo=getEmployInfo, 
                            getSocInfo=getSocInfo,
                            getAwardInfo=getAwardInfo,
                            getFundInfo=getFundInfo,
                            getImpInfo=getImpInfo,
                            getInnInfo=getInnInfo,
                            getPubInfo=getPubInfo,
                            getPresInfo=getPresInfo,
                            getAcInfo=getAcInfo,
                            getNonAcInfo=getNonAcInfo,
                            getEvInfo=getEvInfo,
                            getCommInfo=getCommInfo,
                            getSfiInfo=getSfiInfo,
                            getEdInfo=getEdInfo) 

