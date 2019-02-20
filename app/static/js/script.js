$(document).ready(function() {
    // Change button colours for active in edit_profile
    $('#section-buttons button').on('click', function(){
        $(this).toggleClass('editSectionOpen');
    });

    // Set up cloning of data in edit_profile
    for (var i=1; i<parseInt($('#numEdu').text())+1; i++) {
        $('#edu'+i+'-clone').click(function() {
            addMode('edu', 'Edu', 'Add Education Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#eduDegree').val($('#edu'+id+' .eduDegree').text());
            $('#eduFieldOfStudy').val($('#edu'+id+' .eduFieldOfStudy').text());
            $('#eduInstitution').val($('#edu'+id+' .eduInstitution').text());
            $('#eduLoc').val($('#edu'+id+' .eduLoc').text());
            $('#eduYearDegree').val($('#edu'+id+' .eduYearDegree').text());
        });
    }

    for (var i=1; i<parseInt($('#numEmploy').text())+1; i++) {
        $('#employ'+i+'-clone').click(function() {
            addMode('employ', 'Employ', 'Add Employment Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#employCompany').val($('#employ'+id+' .employCompany').text());
            $('#employLoc').val($('#employ'+id+' .employLoc').text());
            $('#employYears').val($('#employ'+id+' .employYears').text());
        });
    }

    for (var i=1; i<parseInt($('#numSoc').text())+1; i++) {
        $('#soc'+i+'-clone').click(function() {
            addMode('soc', 'Soc', 'Add Societies Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#socStart').val($('#soc'+id+' .socStart').text());
            $('#socEnd').val($('#soc'+id+' .socEnd').text());
            $('#socName').val($('#soc'+id+' .socName').text());
            $('#socMembership').val($('#soc'+id+' .socMembership').text());
            $('#socStatus').val($('#soc'+id+' .socStatus').text()).change();
        });
    }

    for (var i=1; i<parseInt($('#numAwards').text())+1; i++) {
        $('#awards'+i+'-clone').click(function() {
            addMode('awards', 'Awards', 'Add Awards Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#awardYear').val($('#awards'+id+' .awardYear').text());
            $('#awardingBody').val($('#awards'+id+' .awardingBody').text());
            $('#awardDetails').val($('#awards'+id+' .awardDetails').text());
            $('#awardTeam').val($('#awards'+id+' .awardTeam').text());
        });
    }

    for (var i=1; i<parseInt($('#numFund').text())+1; i++) {
        $('#fund'+i+'-clone').click(function() {
            addMode('fund', 'Fund', 'Add Funding Diversification Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#fundStartDate').val($('#fund'+id+' .fundStartDate').text());
            $('#fundEndDate').val($('#fund'+id+' .fundEndDate').text());
            $('#fundAmount').val($('#fund'+id+' .fundAmount').text());
            $('#fundBody').val($('#fund'+id+' .fundBody').text());
            $('#fundProgramme').val($('#fund'+id+' .fundProgramme').text());
            $('#fundStatus').val($('#fund'+id+' .fundStatus').text()).change();
            $('#fundPrimaryAttrib').val($('#fund'+id+' .fundPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numTeam').text())+1; i++) {
        $('#team'+i+'-clone').click(function() {
            addMode('team', 'Team', 'Add New Team Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#teamStartDate').val($('#team'+id+' .teamStartDate').text());
            $('#teamDepartDate').val($('#team'+id+' .teamDepartDate').text());
            $('#teamName').val($('#team'+id+' .teamName').text());
            $('#teamPos').val($('#team'+id+' .teamPos').text());
            $('#teamPrimaryAttrib').val($('#team'+id+' .teamPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numImpacts').text())+1; i++) {
        $('#impact'+i+'-clone').click(function() {
            addMode('impact', 'Impacts', 'Add Impacts Information');

            $('#impactsSubmit').removeClass('d-none');
            $('#impactsEdit').addClass('d-none');
            $('#impactsAddMode').addClass('d-none');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#impactsTitle').val($('#impact'+id+' .impactTitle').text());
            $('#impactCategory').val($('#impact'+id+' .impactCategory').text());
            $('#impactPrimaryBen').val($('#impact'+id+' .impactPrimaryBen').text());
            $('#impactPrimaryAttrib').val($('#impact'+id+' .impactPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numInnovCom').text())+1; i++) {
        $('#innovCom'+i+'-clone').click(function() {
            for (var j=1; j<parseInt($('#numInnovCom').text())+1; j++) {
                $('#innovCom'+j).removeClass('bg-dark text-white');
            }

            $('#innovComTitle').text('Add Innovation and Commercialisation Information');
            $('#innovComForm').trigger('reset');

            $('#innovSubmit').removeClass('d-none');
            $('#innovEdit').addClass('d-none');
            $('#innovAddMode').addClass('d-none');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#innovComYear').val($('#innovCom'+id+' .innovComYear').text());
            $('#innovComType').val($('#innovCom'+id+' .innovComType').text());
            $('#innovComTitle2').val($('#innovCom'+id+' .innovComTitle').text());
            $('#innovComPrimaryAttrib').val($('#innovCom'+id+' .innovComPrimaryAttrib').text());
        });
    }

    /*for (var i=1; i<parseInt($('#numPub').text())+1; i++) {
        $('#pub'+i+'-clone').click(function() {
            addMode('pub', 'Pub', 'Add Publications Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#pubYear').val($('#pub'+id+' .pubYear').text());
            $('#pubType').val($('#pub'+id+' .pubType').text()).change();
            $('#pubTitle2').val($('#pub'+id+' .pubTitle').text());
            $('#pubName').val($('#pub'+id+' .pubName').text());
            $('#pubStatus').val($('#pub'+id+' .pubStatus').text()).change();
            $('#pubDOI').val($('#pub'+id+' .pubDOI').text());
            $('#pubPrimaryAttrib').val($('#pub'+id+' .pubPrimaryAttrib').text());
        });
    }*/

    for (var i=1; i<parseInt($('#numPres').text())+1; i++) {
        $('#pres'+i+'-clone').click(function() {
            addMode('pres', 'Pres', 'Add Presentations Information');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#presYear').val($('#pres'+id+' .presYear').text());
            $('#presTitle2').val($('#pres'+id+' .presTitle').text());
            $('#presEventType').val($('#pres'+id+' .presEventType').text()).change();
            $('#presOrganBody').val($('#pres'+id+' .presOrganBody').text());
            $('#presLoc').val($('#pres'+id+' .presLoc').text());
            $('#presPrimaryAttrib').val($('#pres'+id+' .presPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numAc').text())+1; i++) {
        $('#acCol'+i+'-clone').click(function() {
            addMode('acCol', 'Ac', 'Add Academic Collaborations');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#acColStartDate').val($('#acCol'+id+' .acColStartDate').text());
            $('#acColEndDate').val($('#acCol'+id+' .acColEndDate').text());
            $('#acColInstitution').val($('#acCol'+id+' .acColInstitution').text());
            $('#acColDepartment').val($('#acCol'+id+' .acColDepartment').text());
            $('#acColName').val($('#acCol'+id+' .acColName').text());
            $('#acColGoal').val($('#acCol'+id+' .acColGoal').text()).change();
            $('#acColFreq').val($('#acCol'+id+' .acColFreq').text());
            $('#acColPrimaryAttrib').val($('#acCol'+id+' .acColPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numNonAc').text())+1; i++) {
        $('#nonAcCol'+i+'-clone').click(function() {
            addMode('nonAcCol', 'NonAc', 'Add Non Academic Collaborations');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#nonAcColStartDate').val($('#nonAcCol'+id+' .nonAcColStartDate').text());
            $('#nonAcColEndDate').val($('#nonAcCol'+id+' .nonAcColEndDate').text());
            $('#nonAcColInstitution').val($('#nonAcCol'+id+' .nonAcColInstitution').text());
            $('#nonAcColDepartment').val($('#nonAcCol'+id+' .nonAcColDepartment').text());
            $('#nonAcColName').val($('#nonAcCol'+id+' .nonAcColName').text());
            $('#nonAcColGoal').val($('#nonAcCol'+id+' .nonAcColGoal').text()).change();
            $('#nonAcColFreq').val($('#nonAcCol'+id+' .nonAcColFreq').text());
            $('#nonAcColPrimaryAttrib').val($('#nonAcCol'+id+' .nonAcColPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numEvents').text())+1; i++) {
        $('#event'+i+'-clone').click(function() {
            addMode('event', 'Events', 'Add Events');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#eventStartDate').val($('#event'+id+' .eventStartDate').text());
            $('#eventEndDate').val($('#event'+id+' .eventEndDate').text());
            $('#eventTitle2').val($('#event'+id+' .eventTitle').text());
            $('#eventEventType').val($('#event'+id+' .eventEventType').text()).change();
            $('#eventRole').val($('#event'+id+' .eventRole').text());
            $('#eventLoc').val($('#event'+id+' .eventLoc').text());
            $('#eventPrimaryAttrib').val($('#event'+id+' .eventPrimaryAttrib').text());
        });
    }

    for (var i=1; i<parseInt($('#numComm').text())+1; i++) {
        $('#comm'+i+'-clone').click(function() {
            addMode('comm', 'Comm', 'Communications Overview');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#commYear').val($('#comm'+id+' .commYear').text());
            $('#commNumPublic').val($('#comm'+id+' .commNumPublic').text());
            $('#commNumVisits').val($('#comm'+id+' .commNumVisits').text());
            $('#commNumMedia').val($('#comm'+id+' .commNumMedia').text());
        });
    }

    for (var i=1; i<parseInt($('#numSfi').text())+1; i++) {
        $('#sfi'+i+'-clone').click(function() {
            addMode('sfi', 'Sfi', 'SFI Funding Ratio');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#sfiYear').val($('#sfi'+id+' .sfiYear').text());
            $('#sfiPercentage').val($('#sfi'+id+' .sfiPercentage').text());
        });
    }

    for (var i=1; i<parseInt($('#numPEng').text())+1; i++) {
        $('#pEng'+i+'-clone').click(function() {
            addMode('pEng', 'PEng', 'Education and Public Engagement');

            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#pEngName').val($('#pEng'+id+' .pEngName').text());
            $('#pEngStartDate').val($('#pEng'+id+' .pEngStartDate').text());
            $('#pEngEndDate').val($('#pEng'+id+' .pEngEndDate').text());
            $('#pEngActivityType').val($('#pEng'+id+' .pEngActivityType').text()).change();
            $('#pEngActivityOther').val($('#pEng'+id+' .pEngActivityOther').text());
            $('#pEngTopic').val($('#pEng'+id+' .pEngTopic').text()).change();
            $('#pEngTopicOther').val($('#pEng'+id+' .pEngTopicOther').text());
            $('#pEngArea').val($('#pEng'+id+' .pEngAreapEng').text()).change();  // @TODO: Not updating correctly
            $('#pEngAreaOther').val($('#pEng'+id+' .pEngAreaOther').text());
        });
    }


    // Set up editing of data in edit_profile
    for (var i=1; i<parseInt($('#numEdu').text())+1; i++) {
        $('#edu'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#eduDegree').val($('#edu'+id+' .eduDegree').text());
            $('#eduFieldOfStudy').val($('#edu'+id+' .eduFieldOfStudy').text());
            $('#eduInstitution').val($('#edu'+id+' .eduInstitution').text());
            $('#eduLoc').val($('#edu'+id+' .eduLoc').text());
            $('#eduYearDegree').val($('#edu'+id+' .eduYearDegree').text());

            $('#eduTitle').text('Edit Education Information');

            $('#eduSubmit').addClass('d-none');
            $('#eduEdit').removeClass('d-none');
            $('#eduAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numEdu').text())+1; j++) {
                $('#edu'+j).removeClass('bg-dark text-white');
            }

            $('#edu'+id).addClass('bg-dark text-white');

            $('#eduIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numEmploy').text())+1; i++) {
        $('#employ'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#employCompany').val($('#employ'+id+' .employCompany').text());
            $('#employLoc').val($('#employ'+id+' .employLoc').text());
            $('#employYears').val($('#employ'+id+' .employYears').text());

            $('#employTitle').text('Edit Employment Information');

            $('#employSubmit').addClass('d-none');
            $('#employEdit').removeClass('d-none');
            $('#employAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numEmploy').text())+1; j++) {
                $('#employ'+j).removeClass('bg-dark text-white');
            }

            $('#employ'+id).addClass('bg-dark text-white');

            $('#employIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numSoc').text())+1; i++) {
        $('#soc'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#socStart').val($('#soc'+id+' .socStart').text());
            $('#socEnd').val($('#soc'+id+' .socEnd').text());
            $('#socName').val($('#soc'+id+' .socName').text());
            $('#socMembership').val($('#soc'+id+' .socMembership').text());
            $('#socStatus').val($('#soc'+id+' .socStatus').text()).change();

            $('#socTitle').text('Edit Societies Information');

            $('#socSubmit').addClass('d-none');
            $('#socEdit').removeClass('d-none');
            $('#socAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numSoc').text())+1; j++) {
                $('#soc'+j).removeClass('bg-dark text-white');
            }

            $('#soc'+id).addClass('bg-dark text-white');

            $('#socIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numAwards').text())+1; i++) {
        $('#awards'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#awardYear').val($('#awards'+id+' .awardYear').text());
            $('#awardingBody').val($('#awards'+id+' .awardingBody').text());
            $('#awardDetails').val($('#awards'+id+' .awardDetails').text());
            $('#awardTeam').val($('#awards'+id+' .awardTeam').text());

            $('#awardsTitle').text('Edit Awards Information');

            $('#awardsSubmit').addClass('d-none');
            $('#awardsEdit').removeClass('d-none');
            $('#awardsAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numAwards').text())+1; j++) {
                $('#awards'+j).removeClass('bg-dark text-white');
            }

            $('#awards'+id).addClass('bg-dark text-white');

            $('#awardsIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numFund').text())+1; i++) {
        $('#fund'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#fundStartDate').val($('#fund'+id+' .fundStartDate').text());
            $('#fundEndDate').val($('#fund'+id+' .fundEndDate').text());
            $('#fundAmount').val($('#fund'+id+' .fundAmount').text());
            $('#fundBody').val($('#fund'+id+' .fundBody').text());
            $('#fundProgramme').val($('#fund'+id+' .fundProgramme').text());
            $('#fundStatus').val($('#fund'+id+' .fundStatus').text()).change();
            $('#fundPrimaryAttrib').val($('#fund'+id+' .fundPrimaryAttrib').text());

            $('#fundTitle').text('Edit Funding Diversification Information');

            $('#fundingDivSubmit').addClass('d-none');
            $('#fundingDivEdit').removeClass('d-none');
            $('#fundingDivAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numFund').text())+1; j++) {
                $('#fund'+j).removeClass('bg-dark text-white');
            }

            $('#fund'+id).addClass('bg-dark text-white');

            $('#fundingDivIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numTeam').text())+1; i++) {
        $('#team'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#teamStartDate').val($('#team'+id+' .teamStartDate').text());
            $('#teamDepartDate').val($('#team'+id+' .teamDepartDate').text());
            $('#teamName').val($('#team'+id+' .teamName').text());
            $('#teamPos').val($('#team'+id+' .teamPos').text());
            $('#teamPrimaryAttrib').val($('#team'+id+' .teamPrimaryAttrib').text());

            $('#teamTitle').text('Edit Team Information');

            $('#teamMemSubmit').addClass('d-none');
            $('#teamMemEdit').removeClass('d-none');
            $('#teamMemAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numTeam').text())+1; j++) {
                $('#team'+j).removeClass('bg-dark text-white');
            }

            $('#team'+id).addClass('bg-dark text-white');

            $('#teamMemIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numImpacts').text())+1; i++) {
        $('#impact'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#impactsTitle').val($('#impact'+id+' .impactTitle').text());
            $('#impactCategory').val($('#impact'+id+' .impactCategory').text());
            $('#impactPrimaryBen').val($('#impact'+id+' .impactPrimaryBen').text());
            $('#impactPrimaryAttrib').val($('#impact'+id+' .impactPrimaryAttrib').text());

            $('#impactTitle').text('Edit Impacts Information');

            $('#impactsSubmit').addClass('d-none');
            $('#impactsEdit').removeClass('d-none');
            $('#impactsAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numImpacts').text())+1; j++) {
                $('#impact'+j).removeClass('bg-dark text-white');
            }

            $('#impact'+id).addClass('bg-dark text-white');

            $('#impactsIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numInnovCom').text())+1; i++) {
        $('#innovCom'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#innovComYear').val($('#innovCom'+id+' .innovComYear').text());
            $('#innovComType').val($('#innovCom'+id+' .innovComType').text());
            $('#innovComTitle2').val($('#innovCom'+id+' .innovComTitle').text());
            $('#innovComPrimaryAttrib').val($('#innovCom'+id+' .innovComPrimaryAttrib').text());

            $('#innovComTitle').text('Edit Innovation and Commercialisation Information');

            $('#innovSubmit').addClass('d-none');
            $('#innovEdit').removeClass('d-none');
            $('#innovAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numInnovCom').text())+1; j++) {
                $('#innovCom'+j).removeClass('bg-dark text-white');
            }

            $('#innovCom'+id).addClass('bg-dark text-white');

            $('#innovIndex').attr('name', id.toString());
        });
    }

    /*for (var i=1; i<parseInt($('#numPub').text())+1; i++) {
        $('#pub'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#pubYear').val($('#pub'+id+' .pubYear').text());
            $('#pubType').val($('#pub'+id+' .pubType').text()).change();
            $('#pubTitle2').val($('#pub'+id+' .pubTitle').text());
            $('#pubName').val($('#pub'+id+' .pubName').text());
            $('#pubStatus').val($('#pub'+id+' .pubStatus').text()).change();
            $('#pubDOI').val($('#pub'+id+' .pubDOI').text());
            $('#pubPrimaryAttrib').val($('#pub'+id+' .pubPrimaryAttrib').text());

            $('#pubTitle').text('Edit Publications Information');

            $('#pubSubmit').addClass('d-none');
            $('#pubEdit').removeClass('d-none');
            $('#pubAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numPub').text())+1; j++) {
                $('#pub'+j).removeClass('bg-dark text-white');
            }

            $('#pub'+id).addClass('bg-dark text-white');

            $('#pubIndex').attr('name', id.toString());
        });
    }*/

    for (var i=1; i<parseInt($('#numPres').text())+1; i++) {
        $('#pres'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#presYear').val($('#pres'+id+' .presYear').text());
            $('#presTitle2').val($('#pres'+id+' .presTitle').text());
            $('#presEventType').val($('#pres'+id+' .presEventType').text()).change();
            $('#presOrganBody').val($('#pres'+id+' .presOrganBody').text());
            $('#presLoc').val($('#pres'+id+' .presLoc').text());
            $('#presPrimaryAttrib').val($('#pres'+id+' .presPrimaryAttrib').text());

            $('#presTitle').text('Edit Presentations Information');

            $('#presSubmit').addClass('d-none');
            $('#presEdit').removeClass('d-none');
            $('#presAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numPres').text())+1; j++) {
                $('#pres'+j).removeClass('bg-dark text-white');
            }

            $('#pres'+id).addClass('bg-dark text-white');

            $('#presIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numAc').text())+1; i++) {
        $('#acCol'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#acColStartDate').val($('#acCol'+id+' .acColStartDate').text());
            $('#acColEndDate').val($('#acCol'+id+' .acColEndDate').text());
            $('#acColInstitution').val($('#acCol'+id+' .acColInstitution').text());
            $('#acColDepartment').val($('#acCol'+id+' .acColDepartment').text());
            $('#acColName').val($('#acCol'+id+' .acColName').text());
            $('#acColGoal').val($('#acCol'+id+' .acColGoal').text()).change();
            $('#acColFreq').val($('#acCol'+id+' .acColFreq').text());
            $('#acColPrimaryAttrib').val($('#acCol'+id+' .acColPrimaryAttrib').text());

            $('#acColTitle').text('Edit Academic Collaborations');

            $('#academicCollabsSubmit').addClass('d-none');
            $('#academicCollabsEdit').removeClass('d-none');
            $('#acAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numAc').text())+1; j++) {
                $('#acCol'+j).removeClass('bg-dark text-white');
            }

            $('#acCol'+id).addClass('bg-dark text-white');

            $('#acIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numNonAc').text())+1; i++) {
        $('#nonAcCol'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#nonAcColStartDate').val($('#nonAcCol'+id+' .nonAcColStartDate').text());
            $('#nonAcColEndDate').val($('#nonAcCol'+id+' .nonAcColEndDate').text());
            $('#nonAcColInstitution').val($('#nonAcCol'+id+' .nonAcColInstitution').text());
            $('#nonAcColDepartment').val($('#nonAcCol'+id+' .nonAcColDepartment').text());
            $('#nonAcColName').val($('#nonAcCol'+id+' .nonAcColName').text());
            $('#nonAcColGoal').val($('#nonAcCol'+id+' .nonAcColGoal').text()).change();
            $('#nonAcColFreq').val($('#nonAcCol'+id+' .nonAcColFreq').text());
            $('#nonAcColPrimaryAttrib').val($('#nonAcCol'+id+' .nonAcColPrimaryAttrib').text());

            $('#nonAcColTitle').text('Edit Non Academic Collaborations');

            $('#nonAcademicCollabsSubmit').addClass('d-none');
            $('#nonAcademicCollabsEdit').removeClass('d-none');
            $('#nonAcAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numNonAc').text())+1; j++) {
                $('#nonAcCol'+j).removeClass('bg-dark text-white');
            }

            $('#nonAcCol'+id).addClass('bg-dark text-white');

            $('#nonAcIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numEvents').text())+1; i++) {
        $('#event'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#eventStartDate').val($('#event'+id+' .eventStartDate').text());
            $('#eventEndDate').val($('#event'+id+' .eventEndDate').text());
            $('#eventTitle2').val($('#event'+id+' .eventTitle').text());
            $('#eventEventType').val($('#event'+id+' .eventEventType').text()).change();
            $('#eventRole').val($('#event'+id+' .eventRole').text());
            $('#eventLoc').val($('#event'+id+' .eventLoc').text());
            $('#eventPrimaryAttrib').val($('#event'+id+' .eventPrimaryAttrib').text());

            $('#eventTitle').text('Edit Events');

            $('#eventsSubmit').addClass('d-none');
            $('#eventsEdit').removeClass('d-none');
            $('#eventsAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numEvents').text())+1; j++) {
                $('#event'+j).removeClass('bg-dark text-white');
            }

            $('#event'+id).addClass('bg-dark text-white');

            $('#eventsIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numComm').text())+1; i++) {
        $('#comm'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#commYear').val($('#comm'+id+' .commYear').text());
            $('#commNumPublic').val($('#comm'+id+' .commNumPublic').text());
            $('#commNumVisits').val($('#comm'+id+' .commNumVisits').text());
            $('#commNumMedia').val($('#comm'+id+' .commNumMedia').text());

            $('#commTitle').text('Edit Communications');

            $('#commSubmit').addClass('d-none');
            $('#commEdit').removeClass('d-none');
            $('#commAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numComm').text())+1; j++) {
                $('#comm'+j).removeClass('bg-dark text-white');
            }

            $('#comm'+id).addClass('bg-dark text-white');

            $('#commIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numSfi').text())+1; i++) {
        $('#sfi'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#sfiYear').val($('#sfi'+id+' .sfiYear').text());
            $('#sfiPercentage').val($('#sfi'+id+' .sfiPercentage').text());

            $('#sfiTitle').text('Edit SFI Funding Ratios');

            $('#sfiFundingRatioSubmit').addClass('d-none');
            $('#sfiFundingRatioEdit').removeClass('d-none');
            $('#sfiAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numSfi').text())+1; j++) {
                $('#sfi'+j).removeClass('bg-dark text-white');
            }

            $('#sfi'+id).addClass('bg-dark text-white');

            $('#sfiIndex').attr('name', id.toString());
        });
    }

    for (var i=1; i<parseInt($('#numPEng').text())+1; i++) {
        $('#pEng'+i+'-edit').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));

            $('#pEngName').val($('#pEng'+id+' .pEngName').text());
            $('#pEngStartDate').val($('#pEng'+id+' .pEngStartDate').text());
            $('#pEngEndDate').val($('#pEng'+id+' .pEngEndDate').text());
            $('#pEngActivityType').val($('#pEng'+id+' .pEngActivityType').text()).change();
            $('#pEngActivityOther').val($('#pEng'+id+' .pEngActivityOther').text());
            $('#pEngTopic').val($('#pEng'+id+' .pEngTopic').text()).change();
            $('#pEngTopicOther').val($('#pEng'+id+' .pEngTopicOther').text());
            $('#pEngArea').val($('#pEng'+id+' .pEngAreapEng').text()).change();  // @TODO: Not updating correctly
            $('#pEngAreaOther').val($('#pEng'+id+' .pEngAreaOther').text());

            $('#pEngTitle').text('Edit Education and Public Engagement Information');

            $('#pubEngageSubmit').addClass('d-none');
            $('#pubEngageEdit').removeClass('d-none');
            $('#pubEngageAddMode').removeClass('d-none');

            for (var j=1; j<parseInt($('#numPEng').text())+1; j++) {
                $('#pEng'+j).removeClass('bg-dark text-white');
            }

            $('#pEng'+id).addClass('bg-dark text-white');

            $('#pubEngageIndex').attr('name', id.toString());
        });
    }


    // Switch a section to add new mode (not editing current)
    function addMode(section, uSection, title) {
        for (var j=1; j<parseInt($('#num'+uSection).text())+1; j++) {
            $('#'+section+j).removeClass('bg-dark text-white');
        }

        $('#'+section+'Title').text(title);
        $('#'+section+'Form').trigger('reset');

        $('#'+section+'Submit').removeClass('d-none');
        $('#'+section+'Edit').addClass('d-none');
        $('#'+section+'AddMode').addClass('d-none');
    }


    // Functionality to go back to adding a new entry instead of editing
    $('#eduAddMode').click(function() {
        addMode('edu', 'Edu', 'Add Education Information');
    });

    $('#employAddMode').click(function() {
        addMode('employ', 'Employ', 'Add Employment Information');
    });

    $('#socAddMode').click(function() {
        addMode('soc', 'Soc', 'Add Societies Information');
    });

    $('#awardsAddMode').click(function() {
        addMode('awards', 'Awards', 'Add Awards Information');
    });

    $('#fundingDivAddMode').click(function() {
        addMode('fund', 'Fund', 'Add Funding Diversification Information');
    });

    $('#teamMemAddMode').click(function() {
        addMode('team', 'Team', 'Add New Team Information');
    });

    $('#impactsAddMode').click(function() {
        addMode('impact', 'Impacts', 'Add Impacts Information');

        $('#impactsSubmit').removeClass('d-none');
        $('#impactsEdit').addClass('d-none');
        $('#impactsAddMode').addClass('d-none');
    });

    $('#innovAddMode').click(function() {
        for (var j=1; j<parseInt($('#numInnovCom').text())+1; j++) {
            $('#innovCom'+j).removeClass('bg-dark text-white');
        }

        $('#innovComTitle').text('Add Innovation and Commercialisation Information');
        $('#innovComForm').trigger('reset');

        $('#innovSubmit').removeClass('d-none');
        $('#innovEdit').addClass('d-none');
        $('#innovAddMode').addClass('d-none');
    });

    /*$('#pubAddMode').click(function() {
        addMode('pub', 'Pub', 'Add Publications Information');
    });*/ // moved

    $('#presAddMode').click(function() {
        addMode('pres', 'Pres', 'Add Presentations Information');
    });

    $('#acAddMode').click(function() {
        addMode('acCol', 'Ac', 'Add Academic Collaborations');
    });

    $('#nonAcAddMode').click(function() {
        addMode('nonAcCol', 'NonAc', 'Add Non Academic Collaborations');
    });

    $('#eventsAddMode').click(function() {
        addMode('event', 'Events', 'Add Events');
    });

    $('#commAddMode').click(function() {
        addMode('comm', 'Comm', 'Communications Overview');
    });

    $('#sfiAddMode').click(function() {
        addMode('sfi', 'Sfi', 'SFI Funding Ratio');
    });

    $('#pubEngageAddMode').click(function() {
        addMode('pEng', 'PEng', 'Education and Public Engagement');
    });
});
