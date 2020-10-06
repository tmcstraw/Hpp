from django.http import JsonResponse, HttpResponse, Http404
from .app import *
import tempfile, shutil
from osgeo import ogr
import os
import json
from .config import USER_DIR

def move_files(shapefile,file_name):

    return_obj = {}

    SHP_DIR = USER_DIR + file_name+'/'

    SHP_DIR = os.path.join(SHP_DIR, '')

    for file in os.listdir(SHP_DIR):
        f_path = os.path.join(SHP_DIR, file)
        os.remove(f_path)

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

    return_obj["success"]:"success"

    return return_obj
def move_files_get_fields(shapefile,file_name):

    SHP_DIR = USER_DIR+ file_name+'/'

    SHP_DIR = os.path.join(SHP_DIR, '')

    for file in os.listdir(SHP_DIR):
        f_path = os.path.join(SHP_DIR, file)
        os.remove(f_path)

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






    return_obj["field_names"] = field_list
    return_obj = json.dumps(return_obj)



    return return_obj

