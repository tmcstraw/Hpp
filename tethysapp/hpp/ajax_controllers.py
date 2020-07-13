from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import ToggleSwitch
import geopandas
from fiona import *
from shapely import *
# from geopandas import *
from geopandas.tools import sjoin
import requests
from .app import *
import json
from .utilities import *

def zone_upload(request):

    return_obj = {}

    if request.is_ajax() and request.method == 'POST':

        file_name = request.POST["file_name"]
        zone_shapefiles = request.FILES.getlist('shapefile')

        print(zone_shapefiles)

        field_names = move_files_get_fields(zone_shapefiles,file_name)
        field_names = json.loads(field_names)
        print('now in ajax')
        print(field_names)

        return_obj["field_names"] = field_names["field_names"]
        print('this is return object')
        print(return_obj)

        return JsonResponse(return_obj)

def file_upload(request):

    return_obj = {}

    if request.is_ajax() and request.method == 'POST':

        file_name = request.POST["file_name"]
        shapefiles = request.FILES.getlist('shapefile')

        field_names = move_files_get_fields(shapefiles,file_name)
        field_names = json.loads(field_names)
        print('now in ajax')
        print(field_names)

        return_obj["field_names"] = field_names["field_names"]
        print('this is return object')
        print(return_obj)

        return JsonResponse(return_obj)


def file_upload_move_files(request):
    return_obj = {}

    if request.is_ajax() and request.method == 'POST':
        file_name = request.POST["file_name"]
        shapefiles = request.FILES.getlist('shapefile')

        move_files(shapefiles, file_name)

        return_obj['success'] = "success"

        print('this is return object')
        print(return_obj)

        return JsonResponse(return_obj)

def zone_spatial_join(request):
    return_obj = {}
    field_list = []
    trgt_field_prelist = []
    trgt_field_list = []


    if request.is_ajax() and request.method == 'POST':
        file_name = request.POST["file_name"]
        shapefiles = request.FILES.getlist('shapefile')

        join_file = geopandas.GeoDataFrame.from_file('/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/jct_file/100yr_Junction_Flood_Risk.shp')  # or geojson etc
        target_file = geopandas.GeoDataFrame.from_file('/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/zone_file/100yr_Zone_Flood_Risk.shp')
        pointInPolys = sjoin(join_file, target_file, how='right',op='intersects')

        pointSumByPoly = pointInPolys.groupby('ZoneID').agg(
            free100=('Freebd100y', 'sum'),
            free50=('Freebd50yr', 'sum'),
            free10=('Freebd10yr', 'sum'))
        print()

        target_file = target_file.merge(pointSumByPoly, on='ZoneID')


        target_file.to_file("/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/Output_Zones.shp", driver='ESRI Shapefile', schema=None, index=None, encoding='utf-8')

        return_obj['success'] = "success"


        return JsonResponse(return_obj)
        # return pointSumByPoly
