from flask import render_template, flash, redirect, url_for, request
from app import app, db, admin_required
from app.forms import LoginForm, RegistrationForm, EditProfileForm, GeneralInformationForm, \
    EducationInformationForm, EmploymentInformationForm, \
    SocietiesInformationForm, AwardsInformationForm, \
    FundingDiversificationForm, TeamMembersForm, ImpactsForm, \
    InnovationAndCommercialisationForm, \
    PresentationsForm, AcademicCollaborationsForm, NonAcademicCollaborationsForm, \
    EventsForms, CommunicationsOverviewForm, SfiFundingRatioForm, EducationAndPublicEngagementForm, \
    ChangePassword, ChangeEmail, ProposalForm

from app.models import User, GeneralInformation, EducationInformation, EmploymentInformation, \
    SocietiesInformation, AwardsInformation, FundingDiversification, Impacts, InnovationAndCommercialisation, \
    Presentations, AcademicCollaborations, NonAcademicCollaborations, Events, \
    CommunicationsOverview, SfiFundingRatio, EducationPublicEngagement, SfiProposalCalls, \
    Publication

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import json


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@login_required
def index():
    formList = []

    def check_if_filled(tableName, string):
        result = tableName.query.filter_by(user_id=current_user.id).first()
        if result is None:
            formList.append(string)

    check_if_filled(GeneralInformation, "General Information")
    check_if_filled(EmploymentInformation, "Education")
    check_if_filled(SocietiesInformation, "Societies")
    check_if_filled(AwardsInformation, "Awards")
    check_if_filled(FundingDiversification, "Funding Diversification")
    check_if_filled(Impacts, "Impacts")
    check_if_filled(InnovationAndCommercialisation, "Innovation and Commercialisation")
    check_if_filled(AcademicCollaborations, "Academic Collaborations")
    check_if_filled(NonAcademicCollaborations, "Non academic Collaborations")
    check_if_filled(Events, "Events")
    check_if_filled(CommunicationsOverview, "Communications Overview")
    check_if_filled(SfiFundingRatio, "SFI Funding Ratio")
    check_if_filled(EducationPublicEngagement, "Education and Public engagement")
   

    return render_template("index.html", title="Home ", form=formList)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, orcid=form.orcid.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/calls")
def view_calls():
    calls = SfiProposalCalls.query.all()
    return render_template("view_calls.html", title="Funding Calls", calls=calls)


@app.route("/calls/<call_id>")
def view_call(call_id):
    call = SfiProposalCalls.query.filter_by(id=call_id).first_or_404()
    return render_template("view_call.html", title="Funding Calls", call=call)


@app.route("/admin_register_user", methods=["GET", "POST"])
def admin_register_user():
    admin_required(current_user)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, orcid=form.orcid.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("New user registered")
        return redirect(url_for("admin_control"))
    return render_template("admin_register_user.html", title="Register", form=form)


@app.route("/admin_control")
@login_required
def admin_control():
    admin_required(current_user)
    print("testing testing 1 2 3 ")
    return render_template("admin_control.html", title="Admin Control")


@app.route("/admin_publish_call", methods=["GET", "POST"])
def publish_call():
    admin_required(current_user)
    form = ProposalForm()
    if form.validate_on_submit():
        call = SfiProposalCalls(title=form.title.data, deadline=form.deadline.data, contact=form.contact.data,
                                overview=form.overview.data, funding=form.funding.data, key_dates=form.key_dates.data)
        db.session.add(call)
        db.session.commit()
        flash("Your call for proposal has been published!")
        return redirect(url_for("index"))
    return render_template("admin_publish_call.html", title="Publish Call", form=form)


# not needed
@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Responding Funding call: Project1"},
        {"author": user, "body": "Responding Funding call: Project12"}
    ]
    return render_template("user.html", user=user, posts=posts)


@app.route("/profile/<username>", methods=["GET"])
@login_required
def show_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    check_if_exists = GeneralInformation.query.filter_by(user_id=user.id).first_or_404()
    info = json.loads(check_if_exists.data)

    return render_template("profile.html", title="View Profile", user=user, info=info)

@app.route("/edit_account", methods=["GET", "POST"])
@login_required
def edit_account():
    passwordForm = ChangePassword()
    emailForm = ChangeEmail()

    if request.method == "POST":

        if passwordForm.validate_on_submit and "passSubmit" in request.form:

            user = User.query.filter_by(id=current_user.id).first()
            user.set_password(passwordForm.newPassword2.data)
            db.session.add(user)
            db.session.commit()
            flash("Password has been changed!")
            return redirect(url_for("login"))

        elif emailForm.validate_on_submit:  # and "emailSubmit" in request.form:

            user = User.query.filter_by(email=emailForm.newEmail2.data).first()
            if user is None:
                user = User.query.filter_by(id=current_user.id).first()
                user.email = emailForm.newEmail2.data
                db.session.add(user)
                db.session.commit()
                flash("Email has been changed!")
                return redirect(url_for("login"))
            elif user.email == emailForm.newEmail2.data:
                flash("Please use a different email address")

            return redirect(url_for("edit_account"))
            """
            user = User.query.filter_by(id=current_user.id).first()
            user.email = emailForm.newEmail2.data
            db.session.add(user)
            db.session.commit()
            flash("Email has been changed!")
            return redirect(url_for("login"))
            """

    return render_template("edit_account.html", title="Edit Account", passwordForm=passwordForm,
                           emailForm=emailForm)


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
                "firstName": genInfoForm.firstName.data,
                "lastName": genInfoForm.lastName.data,
                "jobTitle": genInfoForm.jobTitle.data,
                "prefix": genInfoForm.prefix.data,
                "suffix": genInfoForm.suffix.data,
                "phoneNumPrefix": genInfoForm.phoneNumPrefix.data,
                "phoneNum": genInfoForm.phoneNum.data,
                "email": genInfoForm.email.data,
                "orcid": genInfoForm.orcid.data
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

        elif eduForm.validate_on_submit and "eduSubmit" in request.form:

            userInfo = EducationInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "degree": eduForm.degree.data,
                "fieldOfStudy": eduForm.fieldOfStudy.data,
                "institution": eduForm.institution.data,
                "location": eduForm.location.data,
                "yearOfDegreeAward": eduForm.yearOfDegreeAward.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif employForm.validate_on_submit and "employSubmit" in request.form:

            userInfo = EmploymentInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "company": employForm.company.data,
                "location": employForm.location.data,
                "years": employForm.years.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif socForm.validate_on_submit and "socSubmit" in request.form:

            userInfo = SocietiesInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": socForm.startDate.data,
                "endDate": socForm.endDate.data,
                "nameOfSociety": socForm.nameOfSociety.data,
                "typeOfMembership": socForm.typeOfMembership.data,
                "status": socForm.status.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif awardsForm.validate_on_submit and "awardsSubmit" in request.form:

            userInfo = AwardsInformation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": awardsForm.year.data,
                "awardingBody": awardsForm.awardingBody.data,
                "details": awardsForm.details.data,
                "teamMemberName": awardsForm.teamMemberName.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif fundingDivForm.validate_on_submit and "fundingDivSubmit" in request.form:

            userInfo = FundingDiversification(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": fundingDivForm.startDate.data,
                "endDate": fundingDivForm.endDate.data,
                "amount": fundingDivForm.amount.data,
                "fundingBody": fundingDivForm.fundingBody.data,
                "fundingProgramme": fundingDivForm.fundingProgramme.data,
                "status": fundingDivForm.status.data,
                "primaryAttribution": fundingDivForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif teamMemForm.validate_on_submit and "teamMemSubmit" in request.form:
            flash("testSuccessTea")

        elif impactsForm.validate_on_submit and "impactsSubmit" in request.form:

            userInfo = Impacts(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "title": impactsForm.title.data,
                "category": impactsForm.category.data,
                "primaryBeneficiary": impactsForm.primaryBeneficiary.data,
                "primaryAttribution": impactsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif innovForm.validate_on_submit and "innovSubmit" in request.form:

            userInfo = InnovationAndCommercialisation(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": innovForm.year.data,
                "type": innovForm.type.data,
                "title": innovForm.title.data,
                "primaryAttribution": innovForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif presForm.validate_on_submit and "presSubmit" in request.form:

            userInfo = Presentations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": presForm.year.data,
                "title": presForm.title.data,
                "eventType": presForm.eventType.data,
                "organisingBody": presForm.organisingBody.data,
                "location": presForm.location.data,
                "primaryAttribution": presForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif academicCollabsForm.validate_on_submit and "academicCollabsSubmit" in request.form:

            userInfo = AcademicCollaborations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": academicCollabsForm.startDate.data,
                "endDate": academicCollabsForm.endDate.data,
                "nameOfInstitution": academicCollabsForm.nameOfInstitution.data,
                "department": academicCollabsForm.department.data,
                "location": academicCollabsForm.location.data,
                "nameOfCollaborator": academicCollabsForm.nameOfCollaborator.data,
                "goal": academicCollabsForm.goal.data,
                "frequency": academicCollabsForm.frequency.data,
                "primaryAttribution": academicCollabsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif nonAcademicCollabsForm.validate_on_submit and "nonAcademicCollabsSubmit" in request.form:

            userInfo = NonAcademicCollaborations(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": nonAcademicCollabsForm.startDate.data,
                "endDate": nonAcademicCollabsForm.endDate.data,
                "nameOfInstitution": nonAcademicCollabsForm.nameOfInstitution.data,
                "department": nonAcademicCollabsForm.department.data,
                "location": nonAcademicCollabsForm.location.data,
                "nameOfCollaborator": nonAcademicCollabsForm.nameOfCollaborator.data,
                "goal": nonAcademicCollabsForm.goal.data,
                "frequency": nonAcademicCollabsForm.frequency.data,
                "primaryAttribution": nonAcademicCollabsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif eventsForm.validate_on_submit and "eventsSubmit" in request.form:

            userInfo = Events(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": eventsForm.startDate.data,
                "endDate": eventsForm.endDate.data,
                "title": eventsForm.title.data,
                "eventType": eventsForm.eventType.data,
                "role": eventsForm.role.data,
                "location": eventsForm.location.data,
                "primaryAttribution": eventsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif commForm.validate_on_submit and "commSubmit" in request.form:

            userInfo = CommunicationsOverview(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": commForm.year.data,
                "numberOfLectures": commForm.numberOfLectures.data,
                "numberOfVisits": commForm.numberOfVisits.data,
                "numberOfMediaInteracations": commForm.numberOfMediaInteracations.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif fundRatioForm.validate_on_submit and "sfiFundingRatioSubmit" in request.form:

            userInfo = SfiFundingRatio(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": fundRatioForm.year.data,
                "percentage": fundRatioForm.percentage.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif pubEngageForm.validate_on_submit and "pubEngageSubmit" in request.form:

            userInfo = EducationPublicEngagement(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "nameOfProject": pubEngageForm.nameOfProject.data,
                "startDate": pubEngageForm.startDate.data,
                "endDate": pubEngageForm.endDate.data,
                "activityType": pubEngageForm.activityType.data,
                "otherType": pubEngageForm.otherType.data,
                "projectTopic": pubEngageForm.projectTopic.data,
                "otherTopic": pubEngageForm.otherTopic.data,
                "target": pubEngageForm.target.data,
                "localCountry": pubEngageForm.localCountry.data,
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif "edu-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EducationInformation.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "employ-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EmploymentInformation.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "soc-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SocietiesInformation.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "awards-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AwardsInformation.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "fund-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = FundingDiversification.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
            """ Need to add a table to models.py
            elif "team-delete" in request.form:
                num = int([s for s in request.form.keys() if s.isdigit()][0])
                userInfo = TeamMembersForm.query.filter_by(user_id=current_user.id).all()[num-1]
                db.session.delete(userInfo)
                db.session.commit()
                flash("Entry successfully removed.")
            """
        elif "impacts-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Impacts.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "innovCom-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = InnovationAndCommercialisation.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "presentations-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Presentations.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "acCol-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "nonAcCol-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = NonAcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "event-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Events.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "comm-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = CommunicationsOverview.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "sfi-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SfiFundingRatio.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")
        elif "pEng-delete" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EducationPublicEngagement.query.filter_by(user_id=current_user.id).all()[num - 1]
            db.session.delete(userInfo)
            db.session.commit()
            flash("Entry successfully removed.")

        elif eduForm.validate_on_submit and "eduEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EducationInformation.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "degree": eduForm.degree.data,
                "fieldOfStudy": eduForm.fieldOfStudy.data,
                "institution": eduForm.institution.data,
                "location": eduForm.location.data,
                "yearOfDegreeAward": eduForm.yearOfDegreeAward.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif employForm.validate_on_submit and "employEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EmploymentInformation.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "company" : employForm.company.data,
                "location" : employForm.location.data,
                "years" : employForm.years.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif socForm.validate_on_submit and "socEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SocietiesInformation.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif awardsForm.validate_on_submit and "awardsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AwardsInformation.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "year" : awardsForm.year.data,
                "awardingBody" : awardsForm.awardingBody.data,
                "details" : awardsForm.details.data,
                "teamMemberName" : awardsForm.teamMemberName.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif fundingDivForm.validate_on_submit and "fundingDivEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = FundingDiversification.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif teamMemForm.validate_on_submit and "teamMemEdit" in request.form:
            # @TODO
            flash("testSuccessTea")
        elif impactsForm.validate_on_submit and "impactsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = InnovationAndCommercialisation.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "title" : impactsForm.title.data,
                "category" : impactsForm.category.data,
                "primaryBeneficiary" : impactsForm.primaryBeneficiary.data,
                "primaryAttribution" : impactsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif innovForm.validate_on_submit and "innovEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Impacts.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "year" : innovForm.year.data,
                "type" : innovForm.type.data,
                "title" : innovForm.title.data,
                "primaryAttribution" : innovForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif presForm.validate_on_submit and "presEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Presentations.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif academicCollabsForm.validate_on_submit and "academicCollabsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif nonAcademicCollabsForm.validate_on_submit and "nonAcademicCollabsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = NonAcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif eventsForm.validate_on_submit and "eventsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Events.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        elif commForm.validate_on_submit and "commEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = CommunicationsOverview.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "year" : commForm.year.data,
                "numberOfLectures" : commForm.numberOfLectures.data,
                "numberOfVisits" : commForm.numberOfVisits.data,
                "numberOfMediaInteracations" : commForm.numberOfMediaInteracations.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif fundRatioForm.validate_on_submit and "sfiFundingRatioEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SfiFundingRatio.query.filter_by(user_id=current_user.id).all()[num-1]

            info = {
                "year" : fundRatioForm.year.data,
                "percentage" : fundRatioForm.percentage.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif pubEngageForm.validate_on_submit and "pubEngageEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EducationPublicEngagement.query.filter_by(user_id=current_user.id).all()[num-1]

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
            flash("Entry successfully updated.")
        
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
                           getPresInfo=getPresInfo,
                           getAcInfo=getAcInfo,
                           getNonAcInfo=getNonAcInfo,
                           getEvInfo=getEvInfo,
                           getCommInfo=getCommInfo,
                           getSfiInfo=getSfiInfo,
                           getEdInfo=getEdInfo)


@app.route('/search')
@login_required
def search():
    keyword = request.args.get('keyword')

    """
    result = User.query.filter(User.username.contains(keyword)).order_by(
        User.username.contains(keyword)).all()

    result_orcid = User.query.filter(User.orcid.contains(keyword)).order_by(
        User.orcid.contains(keyword)).all()
    """
   

    result = User.query.filter_by(username=keyword).first()
    result_orcid = User.query.filter_by(orcid=keyword).first()

    
    if result is not None:
        return redirect(url_for("show_profile", username=result.username))
    elif result_orcid is not None:
        orcid_username = result_orcid.username
        return redirect(url_for("show_profile", username=orcid_username))
    else:
        return render_template('search_not_found.html')
