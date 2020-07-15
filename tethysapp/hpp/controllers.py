from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
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




    context = {'data_submit_button': data_submit_button,
               'add_custom_file_button': add_custom_file_button,

    }


    return render(request, 'hpp/aggregated_risk.html', context)