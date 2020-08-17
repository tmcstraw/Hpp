from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
from .app import *
from .model import *

# @login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # init_primary_db()

    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hpp/home.html', context)

def zone_construction(request):
    """
    Controller for the app home page.
    """





    context = {

    }

    return render(request, 'hpp/zone_construction.html', context)


def storm_sewer_performance(request):
    """
    Controller for the app home page.
    """


    context = {

    }


    return render(request, 'hpp/storm_sewer_performance.html', context)


def infrastructure_risk(request):
    """
    Controller for the app home page.
    """

    context = {

    }


    return render(request, 'hpp/infrastructure_risk.html', context)


def aggregated_risk(request):
    """
    Controller for the app home page.
    """
    add_custom_file_button = Button(
        display_text='Add File',
        name='add-custom-file-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={
            'id': 'add-custom-file-button',
            'onclick': 'hideShowCustomCheck()',
        }
    )
    data_submit_button = Button(
        display_text='Submit',
        name='data-submit-button',
        icon='glyphicon glyphicon-upload',
        style='success',
        attributes={
            'id': 'data-submit-button',
            'onclick': 'executeSpatialJoins()',
        }
    )

    # initialize session
    Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query DB for data store types
    criteria_list = session.query(Criteria) \
                  .order_by(Criteria.id) \
                  .all()



    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Previous',
            'onclick':'hidePageTwoShowOne()'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Next'
        }
    )

    apply_risk_scores_button = Button(
        display_text='Apply',
        name='apply-risk-scores-button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Previous',
            'onclick': 'applyRiskScores()'
        }
    )

    classify_zones_button = Button(
        display_text='Classify Zones',
        name='classify_zones-button',
        attributes={
            'data-toggle': 'tooltip',
            'data-placement': 'top',
            'title': 'Previous',
            'onclick': 'saveZoneClassTableToDB()'
        }
    )

    context = {'data_submit_button': data_submit_button,
               'add_custom_file_button': add_custom_file_button,
               'apply_risk_scores_button': apply_risk_scores_button,
               'initial_page': 0,
               'previous_button': previous_button,
               'classify_zones_button': classify_zones_button,
               'next_button': next_button,
               'criteria_list': criteria_list,

    }

    session.close()

    return render(request, 'hpp/aggregated_risk.html', context)



