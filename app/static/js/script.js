$(document).ready(function() {
    // Change button colours for active in edit_profile
    $('#section-buttons button').on('click', function(){
        $(this).toggleClass('editSectionOpen');
    });

    // Set up cloning of data in edit_profile
    for (var i=1; i<3; i++) {
        $('#edu'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#eduDegree').val($('#edu'+id+' .eduDegree').text());
            $('#eduFieldOfStudy').val($('#edu'+id+' .eduFieldOfStudy').text());
            $('#eduInstitution').val($('#edu'+id+' .eduInstitution').text());
            $('#eduLoc').val($('#edu'+id+' .eduLoc').text());
            $('#eduYearDegree').val($('#edu'+id+' .eduYearDegree').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#employ'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#employCompany').val($('#employ'+id+' .employCompany').text());
            $('#employLoc').val($('#employ'+id+' .employLoc').text());
            $('#employYears').val($('#employ'+id+' .employYears').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#soc'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#socStart').val($('#soc'+id+' .socStart').text());
            $('#socEnd').val($('#soc'+id+' .socEnd').text());
            $('#socName').val($('#soc'+id+' .socName').text());
            $('#socMembership').val($('#soc'+id+' .socMembership').text());
            $('#socStatus').val($('#soc'+id+' .socStatus').text()).change();
        });
    }

    for (var i=1; i<2; i++) {
        $('#awards'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#awardYear').val($('#awards'+id+' .awardYear').text());
            $('#awardingBody').val($('#awards'+id+' .awardingBody').text());
            $('#awardDetails').val($('#awards'+id+' .awardDetails').text());
            $('#awardTeam').val($('#awards'+id+' .awardTeam').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#fund'+i+'-clone').click(function() {
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

    for (var i=1; i<2; i++) {
        $('#team'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#teamStartDate').val($('#team'+id+' .teamStartDate').text());
            $('#teamDepartDate').val($('#team'+id+' .teamDepartDate').text());
            $('#teamName').val($('#team'+id+' .teamName').text());
            $('#teamPos').val($('#team'+id+' .teamPos').text());
            $('#teamPrimaryAttrib').val($('#team'+id+' .teamPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#impact'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#impactTitle').val($('#impact'+id+' .impactTitle').text());
            $('#impactCategory').val($('#impact'+id+' .impactCategory').text());
            $('#impactPrimaryBen').val($('#impact'+id+' .impactPrimaryBen').text());
            $('#impactPrimaryAttrib').val($('#impact'+id+' .impactPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#innovCom'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#innovComYear').val($('#innovCom'+id+' .innovComYear').text());
            $('#innovComType').val($('#innovCom'+id+' .innovComType').text());
            $('#innovComTitle').val($('#innovCom'+id+' .innovComTitle').text());
            $('#innovComPrimaryAttrib').val($('#innovCom'+id+' .innovComPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#pub'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#pubYear').val($('#pub'+id+' .pubYear').text());
            $('#pubType').val($('#pub'+id+' .pubType').text()).change();
            $('#pubTitle').val($('#pub'+id+' .pubTitle').text());
            $('#pubName').val($('#pub'+id+' .pubName').text());
            $('#pubStatus').val($('#pub'+id+' .pubStatus').text()).change();
            $('#pubDOI').val($('#pub'+id+' .pubDOI').text());
            $('#pubPrimaryAttrib').val($('#pub'+id+' .pubPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#pres'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#presYear').val($('#pres'+id+' .presYear').text());
            $('#presTitle').val($('#pres'+id+' .presTitle').text());
            $('#presEventType').val($('#pres'+id+' .presEventType').text()).change();
            $('#presOrganBody').val($('#pres'+id+' .presOrganBody').text());
            $('#presLoc').val($('#pres'+id+' .presLoc').text());
            $('#presPrimaryAttrib').val($('#pres'+id+' .presPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#acCol'+i+'-clone').click(function() {
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

    for (var i=1; i<2; i++) {
        $('#nonAcCol'+i+'-clone').click(function() {
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

    for (var i=1; i<2; i++) {
        $('#event'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#eventStartDate').val($('#event'+id+' .eventStartDate').text());
            $('#eventEndDate').val($('#event'+id+' .eventEndDate').text());
            $('#eventTitle').val($('#event'+id+' .eventTitle').text());
            $('#eventEventType').val($('#event'+id+' .eventEventType').text()).change();
            $('#eventRole').val($('#event'+id+' .eventRole').text());
            $('#eventLoc').val($('#event'+id+' .eventLoc').text());
            $('#eventPrimaryAttrib').val($('#event'+id+' .eventPrimaryAttrib').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#comm'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#commYear').val($('#comm'+id+' .commYear').text());
            $('#commNumPublic').val($('#comm'+id+' .commNumPublic').text());
            $('#commNumVisits').val($('#comm'+id+' .commNumVisits').text());
            $('#commNumMedia').val($('#comm'+id+' .commNumMedia').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#sfi'+i+'-clone').click(function() {
            var id = parseInt($(this).attr('id').replace(/[^0-9]/g, ''));
            $('#sfiYear').val($('#sfi'+id+' .sfiYear').text());
            $('#sfiPercentage').val($('#sfi'+id+' .sfiPercentage').text());
        });
    }

    for (var i=1; i<2; i++) {
        $('#pEng'+i+'-clone').click(function() {
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
});
