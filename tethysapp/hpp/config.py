# import os
# from .app import Hpp as app
# from tethys_sdk.workspaces import app_workspace, user_workspace
#
# @app_workspace
# def a_controller(request, app_workspace):
#     """
#     Example controller that uses @app_workspace() decorator.
#     """
#     new_file_path = os.path.join(app_workspace.path, 'new_file.txt')
#
#     with open(new_file_path, 'w') as a_file:
#         a_file.write('...')
#
#     context = {}
#
#     return render(request, 'hpp/template.html', context)
USER_DIR = "/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/"