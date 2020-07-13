from django.http import JsonResponse, HttpResponse, Http404
from .app import *
import tempfile, shutil
from osgeo import ogr
import os
import json

def move_files(shapefile,file_name):

    return_obj = {}

    SHP_DIR = '/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/'+file_name+'/'

    SHP_DIR = os.path.join(SHP_DIR, '')

    temp_dir = tempfile.mkdtemp()
    for f in shapefile:
        f_name = f.name
        f_path = os.path.join(SHP_DIR, f_name)

        with open(f_path, 'wb') as f_local:
            f_local.write(f.read())

    for file in os.listdir(SHP_DIR):
        # Reading the shapefile only
        if file.endswith(".shp"):
            f_path = os.path.join(SHP_DIR, file)
            pol_shp = f_path
            pol_name = os.path.splitext(f_name)[0]
        elif file.endswith(".tiff"):
            f_path = os.path.join(SHP_DIR, file)
            pol_shp = f_path
            pol_name = os.path.splitext(f_name)[0]


def move_files_get_fields(shapefile,file_name):

    SHP_DIR = '/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/'+file_name+'/'

    SHP_DIR = os.path.join(SHP_DIR, '')

    field_list = []
    return_obj = {}

    temp_dir = tempfile.mkdtemp()
    for f in shapefile:
        f_name = f.name
        f_path = os.path.join(SHP_DIR, f_name)

        with open(f_path, 'wb') as f_local:
            f_local.write(f.read())

    for file in os.listdir(SHP_DIR):
        # Reading the shapefile only
        if file.endswith(".shp"):
            f_path = os.path.join(SHP_DIR, file)
            pol_shp = f_path
            pol_name = os.path.splitext(f_name)[0]


            ds = ogr.Open(f_path)
            lyr = ds.GetLayer()


            field_names = [field.name for field in lyr.schema]

            for field in field_names:
                field_list.append(field)

                print(field_list)




    return_obj["field_names"] = field_list
    return_obj = json.dumps(return_obj)

    print(return_obj)

    return return_obj

