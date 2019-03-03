from flask import render_template, flash, redirect, url_for, request
from app import app, db, admin_required, reviewer_required
from app.forms import LoginForm, RegistrationForm, RegistrationFormAdmin, EditProfileForm, GeneralInformationForm, \
    EducationInformationForm, EmploymentInformationForm, \
    SocietiesInformationForm, AwardsInformationForm, \
    FundingDiversificationForm, TeamMembersForm, ImpactsForm, \
    InnovationAndCommercialisationForm, \
    PresentationsForm, AcademicCollaborationsForm, NonAcademicCollaborationsForm, \
    EventsForms, CommunicationsOverviewForm, SfiFundingRatioForm, EducationAndPublicEngagementForm, \
    ChangePassword, ChangeEmail, ProposalForm, GrantApplicationForm, CollaboratorForm, \
    ReviewProposalForm, AddReviewerForm, ResetPasswordRequestForm, ResetPasswordForm, \
    FreeTextForm, AddCollaboratorForm, PublicationForm, BibtexPublicationForm, FullSearchForm

from app.models import User, GeneralInformation, EducationInformation, EmploymentInformation, \
    SocietiesInformation, AwardsInformation, FundingDiversification, Impacts, InnovationAndCommercialisation, \
    Presentations, AcademicCollaborations, NonAcademicCollaborations, Events, \
    CommunicationsOverview, SfiFundingRatio, EducationPublicEngagement, SfiProposalCalls, \
    Publication, GrantApplications, GrantApplicationAttachment, FundingCallReviewers, \
    AnnualReport, Grants, Collaborators, Reviews, GrantPublications, GrantEvents

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import as_text


def query_table(table):
    return table.query.filter_by(user_id=current_user.id).all()


def get_list(q):
    lst = []
    for item in q:
        lst.append(json.loads(item.data))
    return lst


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route("/")
@login_required
def index():
    if current_user.is_reviewer:
        return redirect(url_for("proposals_to_review"))

    formList = []
    appList = []

    def check_if_filled(tableName, string):
        result = tableName.query.filter_by(user_id=current_user.id).first()
        if result is None:
            formList.append(string)

    appList = GrantApplications.query.filter_by(user_id=current_user.id).filter_by(is_draft=1).all()

    genInfo = None
    if current_user.is_admin == False and current_user.is_reviewer == False:
        q = GeneralInformation.query.filter_by(user_id=current_user.id).first()
        if q is not None:
            genInfo = json.loads(q.data)

    check_if_filled(GeneralInformation, "General Information")
    check_if_filled(EducationInformation, "Education")
    check_if_filled(EmploymentInformation, "Employment")
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

    year = int(datetime.now().year)
    q = AnnualReport.query.filter_by(user_id=current_user.id, is_submit=True, date=year).first()
    if q is not None:
        q = False
    else:
        q = True
    annualReport = q

    proposals = SfiProposalCalls.query.all()

    applications = GrantApplications.query.filter_by(user_id=current_user.id, is_draft=True).all()

    return render_template("index.html", title="Home ", form=formList, \
                           proposals=proposals, app=appList, applications=applications, \
                           annualReport=annualReport, genInfo=genInfo)


@app.route("/login", methods=["GET", "POST"])
def login():
    def check_exists(name):
        return User.query.filter_by(username=name).first()

    if check_exists("admin") is None:
        password = "admin"
        admin = User(id=0, orcid="0", username="admin", email="admin@admin.com", is_admin=True)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

    if check_exists("reviewer") is None:
        password = "reviewer"
        admin = User(id=1, orcid="-2", username="reviewer", email="reviewer@reviewer.com", is_reviewer=True)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

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
    # if current_user.is_anonymous == False:
    #     complete_general = GeneralInformation.query.filter_by(user_id=current_user.id).first()

    # if current_user.is_anonymous == False and current_user.is_admin == False and current_user.is_reviewer == False and complete_general is None:
    #     flash("Please complete your General Information form first!")
    #     return redirect("edit_profile")

    calls = SfiProposalCalls.query.all()
    return render_template("view_calls.html", title="Funding Calls", calls=calls)


@app.route("/calls/<call_id>", methods=["GET", "POST"])
def view_call(call_id):
    call = SfiProposalCalls.query.filter_by(id=call_id).first_or_404()
    proposals = GrantApplications.query.filter_by(call_id=call_id).all()

    form = AddReviewerForm()
    if form.validate_on_submit():
        reviewer_usr = User.query.filter_by(email=form.reviewer_username.data).first()
        if reviewer_usr is not None:
            already_reviewer = FundingCallReviewers.query.filter_by(call_id=call_id,
                                                                    reviewer_id=reviewer_usr.id).first()
            if already_reviewer is None and reviewer_usr.is_reviewer == 1:
                reviewer = FundingCallReviewers(call_id=call_id, reviewer_id=reviewer_usr.id)
                db.session.add(reviewer)
                db.session.commit()
                flash("Successfully invited reviewer for call for proposal.")
                return redirect(url_for("view_calls"))
            else:
                flash("Reviewer of that username already assigned to this funding call.")
        else:
            flash("Reviewer of that username does not exist.")

    return render_template("view_call.html", title="Funding Calls", call=call, form=form, proposals=proposals)


@app.route("/apply/<call_id>", methods=["GET", "POST"])
def apply(call_id):
    if current_user.is_anonymous == False:
        complete_general = GeneralInformation.query.filter_by(user_id=current_user.id).first()

    if current_user.is_anonymous == False and current_user.is_admin == False and current_user.is_reviewer == False and complete_general is None:
        flash("Please complete your General Information form first!")
        return redirect("edit_profile")

    call = SfiProposalCalls.query.filter_by(id=call_id).first_or_404()
    is_applied = GrantApplications.query.filter_by(user_id=current_user.id, call_id=call_id).first()
    form = GrantApplicationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if is_applied is None:
                is_applied = GrantApplications(user_id=current_user.id, call_id=call_id)
                db.session.add(is_applied)

            is_applied.title = form.title.data
            is_applied.duration = form.duration.data
            is_applied.nrp = form.nrp.data
            is_applied.legal_align = form.legal_align.data
            is_applied.ethical_q1 = form.ethical_q1.data
            is_applied.ethical_q2 = form.ethical_q2.data
            is_applied.country = form.country.data
            is_applied.sci_abstract = form.sci_abstract.data
            is_applied.lay_abstract = form.lay_abstract.data

            # if Collaborators.query.filter_by(grant_id=is_applied.id, user_id=current_user.id).first() is None:
            #   collab_row = Collaborators(grant_id=is_applied.id, user_id=current_user.id, is_pi=True)
            # db.session.add(collab_row)

            db.session.commit()

            flash("You have completed the application")

        if "submit" in request.form:
            if is_applied is not None:
                is_applied.is_draft = False
                is_applied.is_pending = True
                db.session.commit()
                flash("Submitted proposal")
        if "draft" in request.form:
            if is_applied is not None and is_applied.is_pending is False:
                is_applied.is_draft = True
                db.session.commit()
                flash("Submitted draft")
            if is_applied.is_pending is True:
                flash("You have already applied for this award")

        return redirect(url_for("index"))

    if request.method == "GET":

        if is_applied is not None and is_applied.is_pending is True:
            flash("You have already applied for this award")
            return redirect(url_for("view_calls"))

        elif is_applied is not None:

            form.title.data = is_applied.title
            form.duration.data = is_applied.duration
            form.nrp.data = is_applied.nrp
            form.legal_align.data = is_applied.legal_align
            form.country.data = is_applied.country
            form.sci_abstract.data = is_applied.sci_abstract
            form.lay_abstract.data = is_applied.lay_abstract

    return render_template("application.html", title="Apply", form=form)


@app.route("/edit/<call_id>", methods=["GET", "POST"])
def edit(call_id):
    admin_required(current_user)
    call = SfiProposalCalls.query.filter_by(id=call_id).first()

    form = ProposalForm(obj=call)
    if form.validate_on_submit():
        call.title = form.title.data
        call.deadline = form.deadline.data
        call.contact = form.contact.data
        call.overview = form.overview.data
        call.funding = form.funding.data
        call.key_dates = form.key_dates.data
        db.session.add(call)
        db.session.commit()
        flash("The call for proposal has been edited!")
        return redirect(url_for("view_calls"))

    """
    search datebade for calls with that id
    display form with that text filled in
    editable and then send it back to 
    """
    return render_template("admin_edit_call_for_proposal.html", title="Edit Call For Proposal", form=form)


@app.route("/delete/<call_id>", methods=["GET", "POST"])
def delete(call_id):
    admin_required(current_user)
    print("omg is this working")
    SfiProposalCalls.query.filter_by(id=call_id).delete()
    db.session.commit()
    flash("The call for proposal has been deleted!")
    return redirect(url_for("view_calls"))

    return render_template("viewcalls.html", title="Funding Calls")

    """
    should take callid
    search through table for first item with that id
    then delete it and show a message
    """


@app.route("/admin_register_user", methods=["GET", "POST"])
def admin_register_user():
    admin_required(current_user)
    form = RegistrationFormAdmin()
    admin = 0
    reviewer = 0

    if form.validate_on_submit():
        if form.prefix.data == "SFI ADMIN":
            admin = 1
        elif form.prefix.data == "Reviewer":
            reviewer = 1

        user = User(username=form.username.data, email=form.email.data, orcid=form.orcid.data, is_admin=admin,
                    is_reviewer=reviewer)
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
        return redirect(url_for("view_calls"))
    return render_template("admin_publish_call.html", title="Publish Call", form=form)


@app.route("/admin_edit_proposals")
@login_required
def admin_edit_proposals():
    admin_required(current_user)
    print("testing testing 1 2 3 ")
    return render_template("admin_edit_proposals.html", title="Admin Edit proposals")


@app.route("/admin_reviews", methods=["GET", "POST"])
@login_required
def admin_submitted_reviews():
    admin_required(current_user)
    getAllFundingCalls = SfiProposalCalls.query.all()
    getSubmittedReviews = Reviews.query.all()

    if request.method == "POST" and "accept" in request.form:
        review = Reviews.query.filter_by(id=request.form["review_id"]).first()
        db.session.delete(review)

        proposal = GrantApplications.query.filter_by(id=review.proposal_id).first()
        proposal.is_pending = False
        accepted_grant = Grants(call_id=proposal.call_id, application_id=proposal.id, title=proposal.title,
                                duration=proposal.duration)
        db.session.add(accepted_grant)
        db.session.commit()

        collab = Collaborators(grant_id=accepted_grant.id, user_id=proposal.user_id, is_pi=True)
        db.session.add(collab)

        db.session.commit()
        flash("Proposal successfully accepted.")
        return redirect(url_for("admin_submitted_reviews"))

    return render_template("admin_submitted_reviews.html", title="Submitted reviews",
                           getAllFundingCalls=getAllFundingCalls, getSubmittedReviews=getSubmittedReviews)


@app.route("/review", methods=["GET", "POST"])
@login_required
def proposals_to_review():
    reviewer_required(current_user)
    callIds = FundingCallReviewers.query.filter_by(reviewer_id=current_user.id).all()

    if callIds:
        getPendingFunds = []
        for item in callIds:
            proposals = GrantApplications.query.filter_by(call_id=item.call_id).all()
            to_add = []
            for prop in proposals:
                review = Reviews.query.filter_by(proposal_id=prop.id).first()
                if not review:
                    to_add.append(prop)
            if len(to_add) > 0:
                title = SfiProposalCalls.query.filter_by(id=item.call_id).first().title
                getPendingFunds.append([to_add, title])
    else:
        getPendingFunds = None

    return render_template("proposals_to_review.html",
                           title="Pending reviews",
                           getPendingFunds=getPendingFunds)


@app.route("/applications")
def view_applications():
    draft = GrantApplications.query.filter_by(user_id=current_user.id, is_draft=1).all()
    # pending = GrantApplications.query.filter_by(is_awarded=1).all()
    pending = GrantApplications.query.filter_by(user_id=current_user.id, is_pending=1).all()

    g = Collaborators.query.filter_by(user_id=current_user.id).all()
    grant_ids = []
    for a in g:
        grant_ids.append(a.grant_id)

    awarded = []
    for grant in grant_ids:
        q = Grants.query.filter_by(id=grant).first()
        if grant is not None and q is not None:
            awarded.append(q)

    return render_template("view_applications.html", title="MyGrants", draft=draft, pending=pending, awarded=awarded)


@app.route("/applications/<grant_id>", methods=["GET", "POST"])
def view_application(grant_id):
    grant = GrantApplications.query.filter_by(id=grant_id).first_or_404()
    call = SfiProposalCalls.query.filter_by(id=grant.call_id).first()
    user = User.query.filter_by(id=grant.user_id).first()
    reviewer = FundingCallReviewers.query.filter_by(call_id=grant.call_id).first()

    awarded = Grants.query.filter_by(application_id=grant_id).first()

    getReviewInfo = Reviews.query.filter_by(proposal_id=grant_id).filter_by(reviewer_id=current_user.id).first()

    if not getReviewInfo and awarded is None and reviewer is not None and reviewer.reviewer_id == current_user.id:
        form = ReviewProposalForm()
        if form.validate_on_submit():
            review = Reviews(call_id=grant.call_id, proposal_id=grant_id, proposal_title=grant.title,
                             reviewer_id=reviewer.reviewer_id, user_id=grant.user_id, username=user.username,
                             desc=form.description.data, rating=form.rating.data)
            db.session.add(review)
            db.session.commit()
            flash("Your review has been successfully submitted.")
            return redirect(url_for("proposals_to_review"))
    else:
        form = None

    return render_template("view_application.html", title="Grant Application", grant=grant, form=form,
                           getReviewInfo=getReviewInfo, call=call)


@app.route("/view_grant/<id>", methods=["GET", "POST"])
def view_grant(id):
    grant = Grants.query.filter_by(id=id).first_or_404()
    collabs = Collaborators.query.filter_by(grant_id=grant.id).all()
    userC = Collaborators.query.filter_by(user_id=current_user.id).first()
    collabForm = AddCollaboratorForm()

    if collabForm.validate_on_submit():
        user = User.query.filter_by(email=collabForm.email.data).first_or_404()
        check_exists = Collaborators.query.filter_by(user_id=user.id, grant_id=id).first()
        if check_exists is None:
            is_pi = False
            if collabForm.is_pi.data == "yes":
                is_pi = True
            c = Collaborators(grant_id=id, user_id=user.id, is_pi=is_pi)
            db.session.add(c)
            db.session.commit()
            flash("New collaborator added")

    return render_template("view_grant.html", user=userC, grant=grant, collabs=collabs, collabForm=collabForm)


@app.route("/pi_forms/<grant_id>/<user_id>", methods=["GET", "POST"])
def pi_form(grant_id, user_id):
    pubForm = PublicationForm()
    bibForm = BibtexPublicationForm()
    eventsForm = EventsForms()

    if request.method == "POST":
        if pubForm.validate_on_submit():
            new_publication = Publication(title=pubForm.title.data, doi=pubForm.doi.data, year=pubForm.year.data, \
                                          journal=pubForm.journal.data, type=pubForm.type.data,
                                          status=pubForm.status.data, \
                                          primary_user=user_id)
            db.session.add(new_publication)
            db.session.commit()

            new_grantpub = GrantPublications(grant_id=grant_id, user_id=user_id, pub_row=new_publication.id)
            db.session.add(new_grantpub)
            db.session.commit()
            flash("New publications form has been submitted")


        elif eventsForm.validate_on_submit():

            userInfo = Events(user_id=user_id)
            db.session.add(userInfo)
            info = {
                "startDate": eventsForm.startDate.data, #.strftime("%Y/%m/%d"),
                "endDate": eventsForm.endDate.data, #.strftime("%Y/%m/%d"),
                "title": eventsForm.title.data,
                "eventType": eventsForm.eventType.data,
                "role": eventsForm.role.data,
                "location": eventsForm.location.data,
                "primaryAttribution": eventsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()

            new_grantev = GrantEvents(grant_id=grant_id, user_id=user_id, event_row=userInfo.id)
            db.session.add(new_grantev)
            db.session.commit()

            flash("New events form has been submitted")

        elif bibForm.validate_on_submit():

            bp = BibTexParser(interpolate_strings=False)
            bib_database = bp.parse(bibForm.parse.data)
            bib_database.entries[0]

            def value(key):
                return bib_database.entries[0][key]

            keys = ("author", "title", "doi", "year", "ID", "journal", "status")
            if set(keys) <= set(bib_database.entries[0]):
                publication = Publication(title=value("title"), doi=value("doi"), year=value("year"),
                                          journal=value("journal"), type=value("ENTRYTYPE"), status=value("status"),
                                          primary_user=user_id)
                db.session.add(publication)
                db.session.commit()

                new_grantpub = GrantPublications(grant_id=grant_id, user_id=user_id, pub_row=new_publication.id)
                db.session.add(new_grantpub)
                db.session.commit()
                flash("New publications form has been submitted")

        return redirect(url_for("view_grant", id=grant_id))

    return render_template("fill_pi_form.html", grant_id=grant_id, user_id=user_id, pubForm=pubForm, bibForm=bibForm,
                           eventsForm=eventsForm)


@app.route("/grant_forms/<grant_id>", methods=["GET"])
def view_grant_forms(grant_id):
    pub_grant = GrantPublications.query.filter_by(grant_id=grant_id).all()
    event_grant = GrantEvents.query.filter_by(grant_id=grant_id).all()

    publications = []
    events = []

    for item in pub_grant:
        q = Publication.query.filter_by(id=item.pub_row).all()
        for query in q:
            if query is not None:
                publications.append(query)

    for item in event_grant:
        q = Events.query.filter_by(id=item.event_row).all()
        for query in q:
            if query is not None:
                events.append(query)

    return render_template("grant_forms.html", publications=publications, events=events, grant_id=grant_id)


@app.route("/grant_pub/<grant_id>/<form_id>", methods=["GET"])
def view_grant_pub(grant_id, form_id):
    publication = Publication.query.filter_by(id=form_id).first_or_404()

    return render_template("grant_form.html", publication=publication, event=False, data=None)


@app.route("/grant_event/<grant_id>/<form_id>", methods=["GET"])
def view_grant_event(grant_id, form_id):
    event = Events.query.filter_by(id=form_id).first_or_404()
    data = json.loads(event.data)

    return render_template("grant_form.html", publication=False, event=event, data=data)


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
    check_if_exists = GeneralInformation.query.filter_by(user_id=user.id).first()
    gen_info = None
    if check_if_exists is not None:
        gen_info = json.loads(check_if_exists.data)

    edu_info = get_list(query_table(EducationInformation))

    return render_template("profile.html", title="View Profile", user=user,
                           info=gen_info,
                           edu_info=edu_info)


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

    user_info = User.query.filter_by(id=current_user.id).first()
    user_name = False
    jsonGenInfo = GeneralInformation.query.filter_by(user_id=current_user.id).first()
    if jsonGenInfo is not None:
        getGenInfo = json.loads(jsonGenInfo.data)
        user_name = getGenInfo["firstName"] + " " + getGenInfo["lastName"]

    else:
        getGenInfo = ""

    getEduInfo = get_list(query_table(EducationInformation))
    getEmployInfo = get_list(query_table(EmploymentInformation))
    getSocInfo = get_list(query_table(SocietiesInformation))
    getAwardInfo = get_list(query_table(AwardsInformation))
    getFundInfo = get_list(query_table(FundingDiversification))
    getImpInfo = get_list(query_table(Impacts))
    getInnInfo = get_list(query_table(InnovationAndCommercialisation))
    getPresInfo = get_list(query_table(Presentations))
    getAcInfo = get_list(query_table(AcademicCollaborations))
    getNonAcInfo = get_list(query_table(NonAcademicCollaborations))
    getEvInfo = get_list(query_table(Events))
    getCommInfo = get_list(query_table(CommunicationsOverview))
    getSfiInfo = get_list(query_table(SfiFundingRatio))
    getEdInfo = get_list(query_table(EducationPublicEngagement))

    if request.method == "GET":
        genInfoForm.email.data = user_info.email
        genInfoForm.orcid.data = user_info.orcid

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
                "email": user_info.email,
                "orcid": user_info.orcid
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
            userInfo = EmploymentInformation.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "company": employForm.company.data,
                "location": employForm.location.data,
                "years": employForm.years.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif socForm.validate_on_submit and "socEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SocietiesInformation.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif awardsForm.validate_on_submit and "awardsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AwardsInformation.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "year": awardsForm.year.data,
                "awardingBody": awardsForm.awardingBody.data,
                "details": awardsForm.details.data,
                "teamMemberName": awardsForm.teamMemberName.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif fundingDivForm.validate_on_submit and "fundingDivEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = FundingDiversification.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif teamMemForm.validate_on_submit and "teamMemEdit" in request.form:
            # @TODO
            flash("testSuccessTea")
        elif innovForm.validate_on_submit and "innovEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = InnovationAndCommercialisation.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "year": innovForm.year.data,
                "type": innovForm.type.data,
                "title": innovForm.title.data,
                "primaryAttribution": innovForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif impactsForm.validate_on_submit and "impactsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Impacts.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "title": impactsForm.title.data,
                "category": impactsForm.category.data,
                "primaryBeneficiary": impactsForm.primaryBeneficiary.data,
                "primaryAttribution": impactsForm.primaryAttribution.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif presForm.validate_on_submit and "presEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Presentations.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif academicCollabsForm.validate_on_submit and "academicCollabsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = AcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif nonAcademicCollabsForm.validate_on_submit and "nonAcademicCollabsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = NonAcademicCollaborations.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif eventsForm.validate_on_submit and "eventsEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = Events.query.filter_by(user_id=current_user.id).all()[num - 1]

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
            flash("Entry successfully updated.")
        elif commForm.validate_on_submit and "commEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = CommunicationsOverview.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "year": commForm.year.data,
                "numberOfLectures": commForm.numberOfLectures.data,
                "numberOfVisits": commForm.numberOfVisits.data,
                "numberOfMediaInteracations": commForm.numberOfMediaInteracations.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif fundRatioForm.validate_on_submit and "sfiFundingRatioEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = SfiFundingRatio.query.filter_by(user_id=current_user.id).all()[num - 1]

            info = {
                "year": fundRatioForm.year.data,
                "percentage": fundRatioForm.percentage.data
            }

            infoJson = json.dumps(info)
            userInfo.data = infoJson
            db.session.commit()
            flash("Entry successfully updated.")
        elif pubEngageForm.validate_on_submit and "pubEngageEdit" in request.form:
            num = int([s for s in request.form.keys() if s.isdigit()][0])
            userInfo = EducationPublicEngagement.query.filter_by(user_id=current_user.id).all()[num - 1]

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
                           getEdInfo=getEdInfo,
                           user_name=user_name)


# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# def search():
#     keyword = request.args.get('keyword')
#     result = User.query.filter(User.username.contains(keyword)).order_by(
#         User.username.contains(keyword)).all()
#     if result:
#         return render_template('user_result.html', user=result)
#     else:
#         return render_template('search_result.html')


# @app.route('/search')
# @login_required
# def search():
#     keyword = request.args.get('keyword')

#     result = User.query.filter(User.username.contains(keyword)).all()
#     result_orcid = User.query.filter(User.orcid.contains(keyword)).all()

#     if len(result) > 1 or len(result_orcid) > 1:
#         return render_template("search_result2.html", results=result, results_orcid=result_orcid)
#     elif len(result) > 0:
#         r = result[0].username
#         return redirect(url_for("show_profile", username=r))
#     elif len(result_orcid) > 0:
#         orcid_username = result_orcid[0].username
#         return redirect(url_for("show_profile", username=orcid_username))
#     else:
#         return render_template('search_not_found.html')


@app.route("/annual_report", methods=["GET", "POST"])
@login_required
def annual_report():
    def query_table2(table):
        year = int(datetime.now().year)
        return table.query.filter_by(user_id=current_user.id, date=year).first()

    def get_list2(q):
        lst = []
        for item in q:
            if item.data is not None:
                lst.append(json.loads(item.data))
        return lst

    def get_list(item):
        if item is None:
            return {}
        temp, final, dev, hi, ch, act = {}, {}, {}, {}, {}, {}
        if item.is_submit is not None:
            final["submit"] = item.is_submit
        if item.publications_data is not None:
            pub = json.loads(item.publications_data)
            final["publications_data"] = pub
        if item.edu_pub_engagement is not None:
            edu = json.loads(item.edu_pub_engagement)
            final["edu_pub_engagement"] = edu
        if item.academic_collab is not None:
            ac = json.loads(item.academic_collab)
            final["academic_collab"] = ac
        if item.nonacademic_collab is not None:
            non = json.loads(item.nonacademic_collab)
            final["nonacademic_collab"] = non
        if item.commerc is not None:
            com = json.loads(item.commerc)
            final["commerc"] = com
        if item.impact is not None:
            imp = json.loads(item.impact)
            final["impact"] = imp
        if item.deviations is not None:
            dev["deviations"] = item.deviations
        if item.highlights is not None:
            hi = json.loads(item.highlights)
        if item.challenges is not None:
            ch["challenges"] = item.challenges
        if item.activities is not None:
            act["activities"] = item.activities
        temp = {**act, **ch, **hi, **dev}
        final["freeText"] = temp
        return final

    pubEngageForm = EducationAndPublicEngagementForm()
    academicCollabsForm = AcademicCollaborationsForm()
    nonAcademicCollabsForm = NonAcademicCollaborationsForm()
    innovForm = InnovationAndCommercialisationForm()
    impactsForm = ImpactsForm()
    freeForm = FreeTextForm()

    getImpInfo = get_list2(query_table(Impacts))
    getAcInfo = get_list2(query_table(AcademicCollaborations))
    getNonAcInfo = get_list2(query_table(NonAcademicCollaborations))
    getEdInfo = get_list2(query_table(EducationPublicEngagement))
    getInnovInfo = get_list2(query_table(InnovationAndCommercialisation))
    getFreeTextInfo = get_list(query_table2(AnnualReport))

    if request.method == "POST":
        userInfo = query_table2(AnnualReport)

        if pubEngageForm.validate_on_submit and "pubEngageSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "nameOfProject": pubEngageForm.nameOfProject.data,
                "startDate": pubEngageForm.startDate.data, #.strftime("%Y/%m/%d"),
                "endDate": pubEngageForm.endDate.data, #.strftime("%Y/%m/%d"),
                "activityType": pubEngageForm.activityType.data,
                "otherType": pubEngageForm.otherType.data,
                "projectTopic": pubEngageForm.projectTopic.data,
                "otherTopic": pubEngageForm.otherTopic.data,
                "target": pubEngageForm.target.data,
                "localCountry": pubEngageForm.localCountry.data,
            }
            infoJson = json.dumps(info)
            userInfo.edu_pub_engagement = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif academicCollabsForm.validate_on_submit and "academicCollabsSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "startDate": academicCollabsForm.startDate.data, #.strftime("%Y/%m/%d"),
                "endDate": academicCollabsForm.endDate.data, #.strftime("%Y/%m/%d"),
                "nameOfInstitution": academicCollabsForm.nameOfInstitution.data,
                "department": academicCollabsForm.department.data,
                "location": academicCollabsForm.location.data,
                "nameOfCollaborator": academicCollabsForm.nameOfCollaborator.data,
                "goal": academicCollabsForm.goal.data,
                "frequency": academicCollabsForm.frequency.data,
                "primaryAttribution": academicCollabsForm.primaryAttribution.data
            }
            infoJson = json.dumps(info)
            userInfo.academic_collab = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif nonAcademicCollabsForm.validate_on_submit and "nonAcademicCollabsSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
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
            userInfo.nonacademic_collab = infoJson
            db.session.commit()
            flash("Changes saved.")

        elif impactsForm.validate_on_submit and "impactsSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "title": impactsForm.title.data,
                "category": impactsForm.category.data,
                "primaryBeneficiary": impactsForm.primaryBeneficiary.data,
                "primaryAttribution": impactsForm.primaryAttribution.data
            }
            infoJson = json.dumps(info)
            userInfo.impact = infoJson
            db.session.commit()
            flash("Changes saved.")

        elif innovForm.validate_on_submit and "innovSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            info = {
                "year": innovForm.year.data,
                "type": innovForm.type.data,
                "title": innovForm.title.data,
                "primaryAttribution": innovForm.primaryAttribution.data
            }
            infoJson = json.dumps(info)
            userInfo.commerc = infoJson

            db.session.commit()
            flash("Changes saved.")

        elif freeForm.validate_on_submit and "freeTextSubmit" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            userInfo.deviations = freeForm.deviations.data
            highlights = {
                "highlight1": freeForm.highlight1.data,
                "highlight2": freeForm.highlight2.data,
                "highlight3": freeForm.highlight3.data
            }
            userInfo.highlights = json.dumps(highlights)
            userInfo.challenges = freeForm.challenges.data
            userInfo.activities = freeForm.activities.data
            db.session.commit()
            flash("Changes saved.")

        elif "submitFinalVersion" in request.form:
            #flash(getFreeTextInfo)
            if len(getFreeTextInfo) < 6:
                flash("You must complete all forms first")
            else:
                #flash(getFreeTextInfo)
                if userInfo is None:
                    userInfo = AnnualReport(user_id=current_user.id)
                db.session.add(userInfo)
                userInfo.is_submit = True
                db.session.commit()
                flash("Report Submitted.")

        elif "editDraft" in request.form:
            if userInfo is None:
                userInfo = AnnualReport(user_id=current_user.id)
            db.session.add(userInfo)
            userInfo.is_submit = False
            db.session.commit()
            flash("Report in draft mode.")

        elif "viewDraft" in request.form:
            form = getFreeTextInfo = get_list(query_table2(AnnualReport))
            return render_template("annual_report_draft.html", form=form)

        return redirect(url_for("annual_report"))

    elif request.method == "GET":

        getFreeTextInfo = query_table2(AnnualReport)
        if getFreeTextInfo is not None:
            getFreeTextInfo = get_list(query_table2(AnnualReport))
        else:
            t = AnnualReport(user_id=current_user.id)
            db.session.add(t)
            getFreeTextInfo = get_list(query_table2(AnnualReport))
            db.session.commit()

        if getFreeTextInfo["submit"] == True:
            flash("Report already submitted for this year")

        if "impact" in getFreeTextInfo:
            impactsForm.title.data = getFreeTextInfo["impact"]["title"]
            impactsForm.category.data = getFreeTextInfo["impact"]["category"]
            impactsForm.primaryBeneficiary.data = getFreeTextInfo["impact"]["primaryBeneficiary"]
            impactsForm.primaryAttribution.data = getFreeTextInfo["impact"]["primaryAttribution"]

        if "edu_pub_engagement" in getFreeTextInfo:
            pubEngageForm.nameOfProject.data = getFreeTextInfo["edu_pub_engagement"]["nameOfProject"]
            pubEngageForm.startDate.data = getFreeTextInfo["edu_pub_engagement"]["startDate"]
            pubEngageForm.endDate.data = getFreeTextInfo["edu_pub_engagement"]["endDate"]
            pubEngageForm.activityType.data = getFreeTextInfo["edu_pub_engagement"]["activityType"]
            pubEngageForm.otherType.data = getFreeTextInfo["edu_pub_engagement"]["otherType"]
            pubEngageForm.projectTopic.data = getFreeTextInfo["edu_pub_engagement"]["projectTopic"]
            pubEngageForm.otherTopic.data = getFreeTextInfo["edu_pub_engagement"]["otherTopic"]
            pubEngageForm.target.data = getFreeTextInfo["edu_pub_engagement"]["target"]
            pubEngageForm.localCountry.data = getFreeTextInfo["edu_pub_engagement"]["localCountry"]

        if "academic_collab" in getFreeTextInfo:
            academicCollabsForm.startDate.data = getFreeTextInfo["academic_collab"]["startDate"]
            academicCollabsForm.endDate.data = getFreeTextInfo["academic_collab"]["endDate"]
            academicCollabsForm.nameOfInstitution.data = getFreeTextInfo["academic_collab"]["nameOfInstitution"]
            academicCollabsForm.department.data = getFreeTextInfo["academic_collab"]["department"]
            academicCollabsForm.location.data = getFreeTextInfo["academic_collab"]["location"]
            academicCollabsForm.nameOfCollaborator.data = getFreeTextInfo["academic_collab"]["nameOfCollaborator"]
            academicCollabsForm.goal.data = getFreeTextInfo["academic_collab"]["goal"]
            academicCollabsForm.frequency.data = getFreeTextInfo["academic_collab"]["frequency"]
            academicCollabsForm.primaryAttribution.data = getFreeTextInfo["academic_collab"]["primaryAttribution"]

        if "nonacademic_collab" in getFreeTextInfo:
            nonAcademicCollabsForm.startDate.data = getFreeTextInfo["nonacademic_collab"]["startDate"]
            nonAcademicCollabsForm.endDate.data = getFreeTextInfo["nonacademic_collab"]["endDate"]
            nonAcademicCollabsForm.nameOfInstitution.data = getFreeTextInfo["nonacademic_collab"]["nameOfInstitution"]
            nonAcademicCollabsForm.department.data = getFreeTextInfo["nonacademic_collab"]["department"]
            nonAcademicCollabsForm.location.data = getFreeTextInfo["nonacademic_collab"]["location"]
            nonAcademicCollabsForm.nameOfCollaborator.data = getFreeTextInfo["nonacademic_collab"]["nameOfCollaborator"]
            nonAcademicCollabsForm.goal.data = getFreeTextInfo["nonacademic_collab"]["goal"]
            nonAcademicCollabsForm.frequency.data = getFreeTextInfo["nonacademic_collab"]["frequency"]
            nonAcademicCollabsForm.primaryAttribution.data = getFreeTextInfo["nonacademic_collab"]["primaryAttribution"]

        if "commerc" in getFreeTextInfo:
            innovForm.year.data = getFreeTextInfo["commerc"]["year"]
            innovForm.type.data = getFreeTextInfo["commerc"]["type"]
            innovForm.title.data = getFreeTextInfo["commerc"]["title"]
            innovForm.primaryAttribution.data = getFreeTextInfo["commerc"]["primaryAttribution"]

        if "freeText" in getFreeTextInfo:
            if "deviations" in getFreeTextInfo["freeText"]:
                freeForm.deviations.data = getFreeTextInfo["freeText"]["deviations"]
            if "highlight1" in getFreeTextInfo["freeText"]:
                freeForm.highlight1.data = getFreeTextInfo["freeText"]["highlight1"]
            if "highlight2" in getFreeTextInfo["freeText"]:
                freeForm.highlight2.data = getFreeTextInfo["freeText"]["highlight2"]
            if "highlight3" in getFreeTextInfo["freeText"]:
                freeForm.highlight3.data = getFreeTextInfo["freeText"]["highlight3"]
            if "challenges" in getFreeTextInfo["freeText"]:
                freeForm.challenges.data = getFreeTextInfo["freeText"]["challenges"]
            if "activities" in getFreeTextInfo["freeText"]:
                freeForm.activities.data = getFreeTextInfo["freeText"]["activities"]

    return render_template("annual_report.html",
                           title="Edit Profile",
                           impactsForm=impactsForm,
                           innovForm=innovForm,
                           academicCollabsForm=academicCollabsForm,
                           nonAcademicCollabsForm=nonAcademicCollabsForm,
                           pubEngageForm=pubEngageForm,
                           freeForm=freeForm,

                           getImpInfo=getImpInfo,
                           getInnovInfo=getInnovInfo,
                           getAcInfo=getAcInfo,
                           getNonAcInfo=getNonAcInfo,
                           getEdInfo=getEdInfo,
                           getFreeTextInfo=getFreeTextInfo)

    """
    if len(result) > 1 or len(result_orcid) > 1:

        return render_template("search_result2.html", results=result, results_orcid=result_orcid)

    elif len(result) > 0:
        r = result[0].username
        return redirect(url_for("show_profile", username=r))
    elif len(result_orcid) > 0:
        orcid_username = result_orcid[0].username
        return redirect(url_for("show_profile", username=orcid_username))
    else:
        return render_template('search_not_found.html')
    """


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    keyword = request.args.get('keyword')
    result = User.query.filter_by(username=keyword).first()
    result_orcid = User.query.filter_by(orcid=keyword).first()
    if result is not None:
        return redirect(url_for("show_profile", username=result.username))
    elif result_orcid is not None:
        orcid_username = result_orcid.username
        return redirect(url_for("show_profile", username=orcid_username))
    search = FullSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search_page.html', form=search)


@app.route('/result')
@login_required
def search_results(search):
    result = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = user.query(User)
        result = qry.all()

    if not result:
        flash('No result found!')
        return redirect('/search')
    else:
        return render_template('search_result.html')

