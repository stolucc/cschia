from app import app, db
from app.models import User, Post, FundingCall, FundingCallAttachment, GeneralInformation, \
EducationInformation, EmploymentInformation, SocietiesInformation, AwardsInformation, \
FundingDiversification, Impacts, InnovationAndCommercialisation, Presentations, \
AcademicCollaborations, NonAcademicCollaborations, Events, CommunicationsOverview, SfiFundingRatio, \
EducationPublicEngagement, AnnualReport


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
        "AnnualReport" : AnnualReport

        }

