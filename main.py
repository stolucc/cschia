from app import app, db
from app.models import User, Post, FundingCall, FundingCallAttachment, GeneralInformation, \
EducationInformation, EmploymentInformation, SocietiesInformation, AwardsInformation, \
FundingDiversification, Impacts, InnovationAndCommercialisation, Publications, Presentations, \
AcademicCollaborations, NonAcademicCollaborations, Events, CommunicationsOverview, SfiFundingRatio, \
EducationPublicEngagement


@app.shell_context_processor
def make_shell_context():
<<<<<<< HEAD
    return {"db" : db, "User" : User, "Post" : Post}
=======
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
        "Publications" : Publications, 
        "Presentations" : Presentations,
        "AcademicCollaborations" : AcademicCollaborations,
        "NonAcademicCollaborations" : NonAcademicCollaborations,
        "Events" : Events,
        "CommunicationsOverview" : CommunicationsOverview,
        "SfiFundingRatio" : SfiFundingRatio,
        "EducationPublicEngagement" : EducationPublicEngagement
        }
>>>>>>> bbb9d2da423b39e184c72753acc50d14978e4290
