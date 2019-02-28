from app import app, db
from app.models import User, Post, FundingCall, FundingCallAttachment, GeneralInformation, \
EducationInformation, EmploymentInformation, SocietiesInformation, AwardsInformation, \
FundingDiversification, Impacts, InnovationAndCommercialisation, Presentations, \
AcademicCollaborations, NonAcademicCollaborations, Events, CommunicationsOverview, SfiFundingRatio, \
EducationPublicEngagement, AnnualReport, Collaborators, Grants, GrantApplications, \
GrantApplicationAttachment, SfiProposalCalls, Reviews, GrantEvents, GrantPublications


@app.shell_context_processor
def make_shell_context():

    return {
        "db" : db,
        "User" : User,
        "Post" : Post,
        "FundingCall" : FundingCall,
        "FundingCallAttachment" : FundingCallAttachment,
        "GeneralInformation" : GeneralInformation,
        "EducationInformation" : EducationInformation,
        "EmploymentInformation" : EmploymentInformation,
        "SocietiesInformation" : SocietiesInformation,
        "AwardsInformation" : AwardsInformation,
        "FundingDiversification" : FundingDiversification,
        "Impacts" : Impacts,
        "InnovationAndCommercialisation" : InnovationAndCommercialisation,
        "Presentations" : Presentations,
        "AcademicCollaborations" : AcademicCollaborations,
        "NonAcademicCollaborations" : NonAcademicCollaborations,
        "Events" : Events,
        "CommunicationsOverview" : CommunicationsOverview,
        "SfiFundingRatio" : SfiFundingRatio,
        "EducationPublicEngagement" : EducationPublicEngagement,
        "AnnualReport" : AnnualReport,
        "Grants" : Grants,
        "Collaborators" :  Collaborators,
        "GrantApplications" : GrantApplications,
        "GrantApplicationAttachment" : GrantApplicationAttachment,
        "SfiProposalCalls" : SfiProposalCalls,
        "Reviews" : Reviews,
        "GrantPublications" : GrantPublications,
        "GrantEvents" : GrantEvents
        }

