from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from tethys_sdk.gizmos import (Button, MapView, TextInput, DatePicker,
                               SelectInput, DataTableView, MVDraw, MVView,
                               MVLayer)
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import ToggleSwitch
import geopandas
import pandas
import fiona
from fiona import *
from shapely import *
from osgeo import ogr, osr
from pyproj.crs import CRS
# from geopandas import *
from geopandas.tools import sjoin
import requests
from .app import *
import json
from .utilities import *
from .model import *
from .config import USER_DIR

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

    if request.is_ajax() and request.method == 'POST':
        risk_analysis_nm = request.POST["risk_analysis_name"]
        zone_id = request.POST["zone_id"]
        file_names = request.POST["file_names"]
        criteria_names = request.POST["criteria_names"]
        field_names = request.POST["field_names"]
        agg_methods = request.POST["aggregation_methods"]
        criteria_types = request.POST["criteria_types"]
        criteria_inputs = request.POST["criteria_inputs"]

        file_names_array = json.loads(file_names)
        criteria_inputs_array = json.loads(criteria_inputs)
        criteria_names_array = json.loads(criteria_names)



        # print(type(criteria_names_array))
        # criteria_inputs_array = [criteria_inputs]


    # if request.is_ajax() and request.method == 'POST':
    #     file_name = request.POST["file_name"]
    #     shapefiles = request.FILES.getlist('shapefile')
        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        allcriteria = session.query(Criteria).all()
        for criteria_entry in allcriteria:
            session.delete(criteria_entry)

        session.commit()
        session.close()

    #
        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()


        l=0



        target_file = geopandas.GeoDataFrame.from_file(USER_DIR+'zone_file/100yr_Zone_Flood_Risk.shp')


        final_crs = target_file.crs

        for i in file_names_array:
            file_prefix = i[:(i.find('_'))]
            print(file_prefix)
            if file_prefix == "zone":
                for z in criteria_inputs_array:
                    criteria_data = json.loads(z)
                    # print(criteria_data)
                    # print(type(criteria_data))
                    criteria_nm = criteria_data[0]
                    field_nm = criteria_data[1]
                    agg_meth = criteria_data[2]
                    criteria_typ = criteria_data[3]

                    # print(criteria_nm)
                    # print(field_nm)
                    # print(agg_meth)
                    if criteria_nm.startswith(file_prefix):
                        criteria_id = (l + 1)
                        file_nm = file_prefix
                        criteria_nm = criteria_nm[(criteria_nm.find('_') + 1):]
                        field_nm = field_nm[(field_nm.find('_') + 1):]
                        agg_meth = agg_meth[(agg_meth.find('_') + 1):]
                        risk_scores = ''
                        criteria_type = (criteria_typ[(criteria_typ.find('_') + 1):]).upper()

                        l = l + 1

                        criteria = Criteria(risk_analysis_name=risk_analysis_nm,
                                            id=criteria_id,
                                            file_name=file_nm,
                                            criteria_name=criteria_nm,
                                            field_name=field_nm,
                                            agg_method=agg_meth,
                                            risk_scores=risk_scores,
                                            criteria_type=criteria_type,
                                            criteria_weight=0
                                            )
                        session.add(criteria)
                        session.commit()

                        target_file = target_file.rename(columns={field_nm: criteria_nm})
            else:

                SHP_DIR = USER_DIR + i + '/'

                SHP_DIR = os.path.join(SHP_DIR, '')

                for file in os.listdir(SHP_DIR):
                    # Reading the shapefile only
                    if file.endswith(".shp"):
                        f_path = os.path.join(SHP_DIR, file)



                join_file = geopandas.GeoDataFrame.from_file(f_path)  # or geojson etc



                # join_file = geopandas.GeoDataFrame.from_file('/Users/tmcstraw/tethysdev/tethysapp-hpp/tethysapp/hpp/workspaces/user_workspaces/jct_file/100yr_Junction_Flood_Risk.shp')  # or geojson etc

                pointInPolys = sjoin(join_file, target_file, how='right', op='intersects',lsuffix=file_prefix,rsuffix="tgt")
                # print(pointInPolys)


                for j in criteria_inputs_array:
                    criteria_data = json.loads(j)
                    # print(criteria_data)
                    # print(type(criteria_data))
                    criteria_nm = criteria_data[0]
                    field_nm = criteria_data[1]
                    agg_meth = criteria_data[2]
                    criteria_typ = criteria_data[3]




                    # print(criteria_nm)
                    # print(field_nm)
                    # print(agg_meth)
                    if criteria_nm.startswith(file_prefix):
                        criteria_id = (l+1)
                        file_nm = file_prefix
                        criteria_nm =criteria_nm[(criteria_nm.find('_')+1):]
                        field_nm = field_nm[(field_nm.find('_') + 1):]
                        agg_meth = agg_meth[(agg_meth.find('_') + 1):]
                        risk_scores = ''
                        criteria_type = (criteria_typ[(criteria_typ.find('_') + 1):]).upper()

                        l = l+1

                        criteria = Criteria(risk_analysis_name=risk_analysis_nm,
                                            id=criteria_id,
                                            file_name=file_nm,
                                            criteria_name=criteria_nm,
                                            field_name=field_nm,
                                            agg_method=agg_meth,
                                            risk_scores=risk_scores,
                                            criteria_type=criteria_type,
                                            criteria_weight=0)
                        session.add(criteria)
                        session.commit()


                        if field_nm not in pointInPolys.columns:
                            field_nm = field_nm+'_x'


                        pointSumByPoly = pointInPolys.groupby(zone_id).agg(
                            newfield=(field_nm, agg_meth)
                        )

                        # print(pointSumByPoly)
                        pointSumByPoly = pointSumByPoly.rename(columns={"newfield":criteria_nm})

                        # print(pointSumByPoly)

                        target_file = target_file.merge(pointSumByPoly, on=zone_id)
                        print(target_file.crs)
        session.close()

        target_file.to_file(USER_DIR+"Output_Zones.shp", driver='ESRI Shapefile', schema=None, index=None, encoding='utf-8')
        test = geopandas.GeoDataFrame.from_file(USER_DIR+"Output_Zones.shp")
        print("Output CRS")
        print(test.crs)
        return_obj['success'] = "success"


        return JsonResponse(return_obj)
        # return pointSumByPoly

def populate_risk_score_modal(request):

    if request.is_ajax() and request.method == 'POST':
        num_classesaj = request.POST['num_classes']
        criteria_name = request.POST['criteria_name']
        criteria_id = request.POST['criteria_id']

        criteria_id = json.loads(criteria_id)

        return_obj = {}

        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)

        target_df = geopandas.GeoDataFrame.from_file(f_path)
        column = target_df[criteria_name]

        total_num_rows = column.count()
        print(total_num_rows)

        num_null = column.isnull().sum()
        print('the number of null values is:')
        print(num_null)

        return_obj["tot"] = str(total_num_rows)

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        criteria_list = []
        criteria_objs = session.query(Criteria).all()

        for criteria in criteria_objs:
            criteria_list.append("%s" % (criteria.criteria_name))

        print(criteria_list)
        if criteria_name in criteria_list:
            criteria_db = session.query(Criteria).get(criteria_id)

            if criteria_db.num_classes != None:
                num_classes = json.loads(criteria_db.num_classes)
                print(num_classes)
                min_1 = criteria_db.min_1
                print(min_1)
                max_1 = criteria_db.max_1
                risk_scr_1 = criteria_db.risk_score_1

                min_2 = criteria_db.min_2
                max_2 = criteria_db.max_2
                risk_scr_2 = criteria_db.risk_score_2

                min_3 = criteria_db.min_3
                max_3 = criteria_db.max_3
                risk_scr_3 = criteria_db.risk_score_3

                min_4 = criteria_db.min_4
                max_4 = criteria_db.max_4
                risk_scr_4 = criteria_db.risk_score_4

                min_5 = criteria_db.min_5
                max_5 = criteria_db.max_5
                risk_scr_5 = criteria_db.risk_score_5


                if num_classes == 2:


                    return_obj["min_1"] = min_1
                    return_obj["max_1"] = max_1
                    return_obj["risk_score_1"] = risk_scr_1
                    return_obj["min_2"] = min_2
                    return_obj["max_2"] = max_2
                    return_obj["risk_score_2"] = risk_scr_2

                    ranges = [min_1,max_1,max_2]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()


                    i = 1



                    for n in count_class[criteria_name]:
                        return_obj["count_"+str(i)] = n
                        i=i+1


                if num_classes == 3:
                    return_obj["min_1"] = min_1
                    return_obj["max_1"] = max_1
                    return_obj["risk_score_1"] = risk_scr_1
                    return_obj["min_2"] = min_2
                    return_obj["max_2"] = max_2
                    return_obj["risk_score_2"] = risk_scr_2
                    return_obj["min_3"] = min_3
                    return_obj["max_3"] = max_3
                    return_obj["risk_score_3"] = risk_scr_3



                    ranges = [min_1, max_1, max_2, max_3]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1

                if num_classes == 4:
                    return_obj["min_1"] = min_1
                    return_obj["max_1"] = max_1
                    return_obj["risk_score_1"] = risk_scr_1
                    return_obj["min_2"] = min_2
                    return_obj["max_2"] = max_2
                    return_obj["risk_score_2"] = risk_scr_2
                    return_obj["min_3"] = min_3
                    return_obj["max_3"] = max_3
                    return_obj["risk_score_3"] = risk_scr_3
                    return_obj["min_4"] = min_4
                    return_obj["max_4"] = max_4
                    return_obj["risk_score_4"] = risk_scr_4

                    ranges = [min_1, max_1, max_2, max_3, max_4]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1

                if num_classes == 5:
                    print("true")
                    return_obj["min_1"] = min_1
                    return_obj["max_1"] = max_1
                    return_obj["risk_score_1"] = risk_scr_1
                    return_obj["min_2"] = min_2
                    return_obj["max_2"] = max_2
                    return_obj["risk_score_2"] = risk_scr_2
                    return_obj["min_3"] = min_3
                    return_obj["max_3"] = max_3
                    return_obj["risk_score_3"] = risk_scr_3
                    return_obj["min_4"] = min_4
                    return_obj["max_4"] = max_4
                    return_obj["risk_score_4"] = risk_scr_4
                    return_obj["min_5"] = min_5
                    return_obj["max_5"] = max_5
                    return_obj["risk_score_5"] = risk_scr_5

                    ranges = [min_1, max_1, max_2, max_3, max_4, max_5]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1


            else:
                num_classes = json.loads(num_classesaj)
                max = column.max()
                min = column.min()

                # for two classes
                fiftyper = column.max()*(0.5)


                # for three classes
                fifteenper = column.max()*(0.15)
                eightyfiveper = column.max()*(0.85)

                # for four classes
                twelveper = column.max()*(.125)
                fiftyperfour = column.max()*(.50)
                eightysevenper = column.max()*(.875)

                #for five classes
                tenper = column.max()*(0.1)
                thirtyper = column.max()*(0.30)
                seventyper = column.max()*(0.70)
                ninetyper = column.max()*(0.90)

                # print(num_classes)
                # print(json.loads(num_classes))
                #
                # num_classes = json.loads(num_classes)
                #
                # total_num_rows = column.count()
                # print(total_num_rows)
                #
                # num_null = column.isnull().sum()
                # print('the number of null values is:')
                # print(num_null)
                #
                # return_obj["tot"] = str(total_num_rows)

                if num_classes == 2:
                    print("got to if")
                    return_obj["min_1"] = (min)
                    return_obj["max_1"] = fiftyper
                    return_obj["min_2"] = (fiftyper + 0.00001)
                    return_obj["max_2"] = (max)

                    ranges = [min,fiftyper,max]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()


                    i = 1



                    for n in count_class[criteria_name]:
                        return_obj["count_"+str(i)] = n
                        i=i+1


                if num_classes == 3:
                    return_obj["min_1"] = min
                    return_obj["max_1"] = fifteenper
                    return_obj["min_2"] = (fifteenper + 0.00001)
                    return_obj["max_2"] = eightyfiveper
                    return_obj["min_3"] = (eightyfiveper + 0.00001)
                    return_obj["max_3"] = max

                    ranges = [min, fifteenper, eightyfiveper, max]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1

                if num_classes == 4:
                    return_obj["min_1"] = min
                    return_obj["max_1"] = twelveper
                    return_obj["min_2"] = (twelveper + 0.00001)
                    return_obj["max_2"] = fiftyper
                    return_obj["min_3"] = (fiftyper + 0.00001)
                    return_obj["max_3"] = eightysevenper
                    return_obj["min_4"] = (eightysevenper + 0.00001)
                    return_obj["max_4"] = max

                    ranges = [min, twelveper, fiftyper, eightysevenper, max]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1

                if num_classes == 5:
                    return_obj["min_1"] = min
                    return_obj["max_1"] = tenper
                    return_obj["min_2"] = (tenper + 0.00001)
                    return_obj["max_2"] = thirtyper
                    return_obj["min_3"] = (thirtyper + 0.00001)
                    return_obj["max_3"] = seventyper
                    return_obj["min_4"] = (seventyper + 0.00001)
                    return_obj["max_4"] = ninetyper
                    return_obj["min_5"] = (ninetyper + 0.00001)
                    return_obj["max_5"] = max

                    ranges = [min, tenper, thirtyper, seventyper, ninetyper, max]

                    count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                    i = 1

                    for n in count_class[criteria_name]:
                        return_obj["count_" + str(i)] = n
                        i = i + 1
        return_obj["num_classes"] = num_classes
        session.close()

        print(return_obj)
        return JsonResponse(return_obj)

def num_class_change_populate_risk_score_modal(request):

    if request.is_ajax() and request.method == 'POST':
        num_classesaj = request.POST['num_classes']
        criteria_name = request.POST['criteria_name']
        criteria_id = request.POST['criteria_id']

        criteria_id = json.loads(criteria_id)

        return_obj = {}

        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)

        target_df = geopandas.GeoDataFrame.from_file(f_path)
        column = target_df[criteria_name]

        total_num_rows = column.count()
        print(total_num_rows)

        num_null = column.isnull().sum()
        print('the number of null values is:')
        print(num_null)

        return_obj["tot"] = str(total_num_rows)

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        criteria_list = []
        criteria_objs = session.query(Criteria).all()

        for criteria in criteria_objs:
            criteria_list.append("%s" % (criteria.criteria_name))

        print(criteria_list)
        if criteria_name in criteria_list:
            criteria_db = session.query(Criteria).get(criteria_id)


            num_classes = json.loads(num_classesaj)
            max = column.max()
            min = column.min()

            # for two classes
            fiftyper = column.max()*(0.5)


            # for three classes
            fifteenper = column.max()*(0.15)
            eightyfiveper = column.max()*(0.85)

            # for four classes
            twelveper = column.max()*(.125)
            fiftyperfour = column.max()*(.50)
            eightysevenper = column.max()*(.875)

            #for five classes
            tenper = column.max()*(0.1)
            thirtyper = column.max()*(0.30)
            seventyper = column.max()*(0.70)
            ninetyper = column.max()*(0.90)

            # print(num_classes)
            # print(json.loads(num_classes))
            #
            # num_classes = json.loads(num_classes)
            #
            # total_num_rows = column.count()
            # print(total_num_rows)
            #
            # num_null = column.isnull().sum()
            # print('the number of null values is:')
            # print(num_null)
            #
            # return_obj["tot"] = str(total_num_rows)

            if num_classes == 2:
                print("got to if")
                return_obj["min_1"] = (min)
                return_obj["max_1"] = fiftyper
                return_obj["min_2"] = (fiftyper + 0.00001)
                return_obj["max_2"] = (max)

                ranges = [min,fiftyper,max]

                count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()


                i = 1



                for n in count_class[criteria_name]:
                    return_obj["count_"+str(i)] = n
                    i=i+1


            if num_classes == 3:
                return_obj["min_1"] = min
                return_obj["max_1"] = fifteenper
                return_obj["min_2"] = (fifteenper + 0.00001)
                return_obj["max_2"] = eightyfiveper
                return_obj["min_3"] = (eightyfiveper + 0.00001)
                return_obj["max_3"] = max

                ranges = [min, fifteenper, eightyfiveper, max]

                count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                i = 1

                for n in count_class[criteria_name]:
                    return_obj["count_" + str(i)] = n
                    i = i + 1

            if num_classes == 4:
                return_obj["min_1"] = min
                return_obj["max_1"] = twelveper
                return_obj["min_2"] = (twelveper + 0.00001)
                return_obj["max_2"] = fiftyper
                return_obj["min_3"] = (fiftyper + 0.00001)
                return_obj["max_3"] = eightysevenper
                return_obj["min_4"] = (eightysevenper + 0.00001)
                return_obj["max_4"] = max

                ranges = [min, twelveper, fiftyper, eightysevenper, max]

                count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                i = 1

                for n in count_class[criteria_name]:
                    return_obj["count_" + str(i)] = n
                    i = i + 1

            if num_classes == 5:
                return_obj["min_1"] = min
                return_obj["max_1"] = tenper
                return_obj["min_2"] = (tenper + 0.00001)
                return_obj["max_2"] = thirtyper
                return_obj["min_3"] = (thirtyper + 0.00001)
                return_obj["max_3"] = seventyper
                return_obj["min_4"] = (seventyper + 0.00001)
                return_obj["max_4"] = ninetyper
                return_obj["min_5"] = (ninetyper + 0.00001)
                return_obj["max_5"] = max

                ranges = [min, tenper, thirtyper, seventyper, ninetyper, max]

                count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

                i = 1

                for n in count_class[criteria_name]:
                    return_obj["count_" + str(i)] = n
                    i = i + 1


        return_obj["num_classes"] = num_classes
        session.close()

        print(return_obj)
        return JsonResponse(return_obj)



def update_min_risk_values(request):

    if request.is_ajax() and request.method == 'POST':
        num_classes = request.POST['num_classes']
        criteria_name = request.POST['criteria_name']
        min_list = request.POST['min_list']

        min_list = json.loads(min_list)


        print(criteria_name)


        return_obj = {}

        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)

        target_df = geopandas.GeoDataFrame.from_file(f_path)
        column = target_df[criteria_name]
        max = column.max()
        # min = 0


        num_classes = json.loads(num_classes)

        total_num_rows = column.count()

        return_obj["tot"] = str(total_num_rows)

        if num_classes == 2:
            min_1 = json.loads(min_list[0])
            min_2 = json.loads(min_list[1])


            max_1 = min_2 - 0.00001


            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max

            ranges = [min_1,max_1,max]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()


            i = 1



            for n in count_class[criteria_name]:
                return_obj["count_"+str(i)] = n
                i=i+1


        if num_classes == 3:

            min_1 = json.loads(min_list[0])
            min_2 = json.loads(min_list[1])
            min_3 = json.loads(min_list[2])


            max_1 = min_2 - 0.00001
            max_2 = min_3 - 0.00001


            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max

            ranges = [min_1, max_1, max_2, max]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        if num_classes == 4:

            min_1 = json.loads(min_list[0])
            min_2 = json.loads(min_list[1])
            min_3 = json.loads(min_list[2])
            min_4 = json.loads(min_list[3])

            max_1 = min_2 - 0.00001
            max_2 = min_3 - 0.00001
            max_3 = min_4 - 0.00001

            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max_3
            return_obj["min_4"] = min_4
            return_obj["max_4"] = max

            ranges = [min_1, max_1, max_2, max_3, max]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        if num_classes == 5:

            min_1 = json.loads(min_list[0])
            min_2 = json.loads(min_list[1])
            min_3 = json.loads(min_list[2])
            min_4 = json.loads(min_list[3])
            min_5 = json.loads(min_list[4])

            max_1 = min_2 - 0.00001
            max_2 = min_3 - 0.00001
            max_3 = min_4 - 0.00001
            max_4 = min_5 - 0.00001



            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max_3
            return_obj["min_4"] = min_4
            return_obj["max_4"] = max_4
            return_obj["min_5"] = min_5
            return_obj["max_5"] = max

            ranges = [min_1, max_1, max_2, max_3, max_4, max]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        return JsonResponse(return_obj)



def update_max_risk_values(request):

    if request.is_ajax() and request.method == 'POST':
        num_classes = request.POST['num_classes']
        criteria_name = request.POST['criteria_name']
        max_list = request.POST['max_list']

        max_list = json.loads(max_list)

        print(criteria_name)


        return_obj = {}

        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)

        target_df = geopandas.GeoDataFrame.from_file(f_path)
        column = target_df[criteria_name]
        # max = column.max()
        min = column.min()


        num_classes = json.loads(num_classes)

        total_num_rows = column.count()

        return_obj["tot"] = str(total_num_rows)

        if num_classes == 2:
            min_1 = min
            max_1 = json.loads(max_list[0])
            min_2 = max_1 + 0.00001
            max_2 = json.loads(max_list[1])

            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2

            ranges = [min_1,max_1,max_2]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()


            i = 1



            for n in count_class[criteria_name]:
                return_obj["count_"+str(i)] = n
                i=i+1


        if num_classes == 3:

            min_1 = min
            max_1 = json.loads(max_list[0])
            min_2 = max_1 + 0.00001
            max_2 = json.loads(max_list[1])
            min_3 = max_2 + 0.00001
            max_3 = json.loads(max_list[2])

            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max_3

            ranges = [min_1, max_1, max_2, max_3]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        if num_classes == 4:

            min_1 = min
            max_1 = json.loads(max_list[0])
            min_2 = max_1 + 0.00001
            max_2 = json.loads(max_list[1])
            min_3 = max_2 + 0.00001
            max_3 = json.loads(max_list[2])
            min_4 = max_3 + 0.00001
            max_4 = json.loads(max_list[3])

            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max_3
            return_obj["min_4"] = min_4
            return_obj["max_4"] = max_4

            ranges = [min_1, max_1, max_2, max_3, max_4]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        if num_classes == 5:

            min_1 = min
            max_1 = json.loads(max_list[0])
            min_2 = max_1 + 0.00001
            max_2 = json.loads(max_list[1])
            min_3 = max_2 + 0.00001
            max_3 = json.loads(max_list[2])
            min_4 = max_3 + 0.00001
            max_4 = json.loads(max_list[3])
            min_5 = max_4 + 0.00001
            max_5 = json.loads(max_list[4])


            return_obj["min_1"] = min_1
            return_obj["max_1"] = max_1
            return_obj["min_2"] = min_2
            return_obj["max_2"] = max_2
            return_obj["min_3"] = min_3
            return_obj["max_3"] = max_3
            return_obj["min_4"] = min_4
            return_obj["max_4"] = max_4
            return_obj["min_5"] = min_5
            return_obj["max_5"] = max_5

            ranges = [min_1, max_1, max_2, max_3, max_4, max_5]

            count_class = target_df.groupby(pandas.cut(column, ranges,include_lowest =True)).count()

            i = 1

            for n in count_class[criteria_name]:
                return_obj["count_" + str(i)] = n
                i = i + 1

        return JsonResponse(return_obj)


def RiskClassifier(row, source_col, output_col, min_val, max_val, reclass_value, weight):
    # If area of input geometry is lower that the threshold value
    if row[source_col] >= min_val and row[source_col] <= max_val :
        # Update the output column with value 0
        row[output_col] = reclass_value * weight
    # If area of input geometry is higher than the threshold value update with value 1

    # Return the updated row
    return row

def RiskScoreCalcs(row, field_list, cof_tot_col, lof_tot_col, tot_rsk_scr_col):
    # If area of input geometry is lower that the threshold value

    for field in field_list:

        field_nm = field[0]
        field_typ = field[1]


        if field_typ == "LOF":
            # Update the output column with value 0
            row[lof_tot_col] = row[field_nm] + row[lof_tot_col]
        elif field_typ == "COF":

            # Update the output column with value 0
            row[cof_tot_col] = row[field_nm] + row[cof_tot_col]

    row[tot_rsk_scr_col] = row[cof_tot_col] * row[lof_tot_col]
    # Return the updated row
    return row


def risk_score_reclassification (request):
    if request.is_ajax() and request.method == 'POST':
        # num_classes = request.POST['num_classes']
        # criteria_name = request.POST['criteria_name']


        return_obj = {}

        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        criteria_list = []
        criteria_objs = session.query(Criteria).all()

        target_df = geopandas.GeoDataFrame.from_file(f_path)
        print("Page 2 Starting CRS")
        zone_crs = target_df.crs

        field_data_list = []


        for criteria in criteria_objs:
            criteria_list.append("%s" % (criteria.criteria_name))

        print(criteria_list)
        for criteria_db in criteria_objs:

            criteria_name = criteria_db.criteria_name
            num_classes = json.loads(criteria_db.num_classes)
            crit_weight = criteria_db.criteria_weight
            crit_type = criteria_db.criteria_type

            min_1 = criteria_db.min_1
            max_1 = criteria_db.max_1
            risk_score_1 = criteria_db.risk_score_1

            min_2 = criteria_db.min_2
            max_2 = criteria_db.max_2
            risk_score_2 = criteria_db.risk_score_2

            min_3 = criteria_db.min_3
            max_3 = criteria_db.max_3
            risk_score_3 = criteria_db.risk_score_3

            min_4 = criteria_db.min_4
            max_4 = criteria_db.max_4
            risk_score_4 = criteria_db.risk_score_4

            min_5 = criteria_db.min_5
            max_5 = criteria_db.max_5
            risk_score_5 = criteria_db.risk_score_5



            reclass_col = criteria_name +'RS'

            target_df[reclass_col] = None
            print(target_df.crs)

            if num_classes == 1:
                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_1, max_val=max_1,reclass_value=risk_score_1, weight=crit_weight, axis=1)


            if num_classes == 2:
                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_1, max_val=max_1,reclass_value=risk_score_1, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_2, max_val=max_2,reclass_value=risk_score_2, weight=crit_weight, axis=1)


            if num_classes == 3:
                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_1, max_val=max_1, reclass_value=risk_score_1, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_2, max_val=max_2, reclass_value=risk_score_2, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_3, max_val=max_3,reclass_value=risk_score_3, weight=crit_weight, axis=1)


            if num_classes == 4:
                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_1, max_val=max_1, reclass_value=risk_score_1, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_2, max_val=max_2, reclass_value=risk_score_2, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_3, max_val=max_3, reclass_value=risk_score_3, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_4, max_val=max_4,reclass_value=risk_score_4, weight=crit_weight, axis=1)


            if num_classes == 5:
                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_1, max_val=max_1, reclass_value=risk_score_1, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_2, max_val=max_2, reclass_value=risk_score_2, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_3, max_val=max_3, reclass_value=risk_score_3, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_4, max_val=max_4, reclass_value=risk_score_4, weight=crit_weight, axis=1)

                target_df = target_df.apply(RiskClassifier, source_col=criteria_name, output_col=reclass_col, min_val=min_5, max_val=max_5,reclass_value=risk_score_5, weight=crit_weight, axis=1)


            print(target_df.type)
            print(target_df.crs)






            field_data_list.append([reclass_col,crit_type])




        lof_tot_col = "TOT_LOF_RS"
        cof_tot_col = "TOT_COF_RS"
        tot_rsk_scr_col = "TOTAL_RISK"

        target_df[cof_tot_col] = 0.0
        target_df[lof_tot_col] = 0.0
        target_df[tot_rsk_scr_col] = 0.0

        target_df = target_df.apply(RiskScoreCalcs, field_list=field_data_list, cof_tot_col=cof_tot_col, lof_tot_col=lof_tot_col, tot_rsk_scr_col=tot_rsk_scr_col, axis=1)
        session.close()
        # orig_file = geopandas.GeoDataFrame.from_file(f_path)
        #
        # target_file = target_file.merge(target_df, on=zone_id)
        #
        #
        target_df = target_df.set_geometry(col="geometry", drop=False, inplace=False, crs=zone_crs)
        target_df.to_file(USER_DIR + "Output_Zones.shp", driver='ESRI Shapefile', schema=None, index=None, encoding='utf-8')
        print("Page 2 Ending Output CRS")
        print(target_df.crs)

        return JsonResponse(return_obj)

def save_risk_classification_to_db (request):
    if request.is_ajax() and request.method == 'POST':
        num_classes = request.POST['num_classes']
        criteria_name = request.POST['criteria_name']
        max_list = request.POST['max_list']
        min_list = request.POST['min_list']
        risk_score_list = request.POST['risk_score_list']
        criteria_id = request.POST['criteria_id']


        num_classes = json.loads(num_classes)
        min_list = json.loads(min_list)
        max_list = json.loads(max_list)
        risk_score_list = json.loads(risk_score_list)
        criteria_id = json.loads(criteria_id)



        min_1 = json.loads(min_list[0])
        max_1 = json.loads(max_list[0])
        risk_score_1 = json.loads(risk_score_list[0])
        min_2 = json.loads(min_list[1])
        max_2 = json.loads(max_list[1])
        risk_score_2 = json.loads(risk_score_list[1])
        if min_list[2] != None and max_list[2] != None:
            min_3 = json.loads(min_list[2])
            max_3 = json.loads(max_list[2])
            risk_score_3 = json.loads(risk_score_list[2])
        else:
            min_3 = min_list[2]
            max_3 = max_list[2]
            risk_score_3 = risk_score_list[2]
        if min_list[3] != None and max_list[3] != None:
            min_4 = json.loads(min_list[3])
            max_4 = json.loads(max_list[3])
            risk_score_4 = json.loads(risk_score_list[3])
        else:
            min_4 = min_list[3]
            max_4 = max_list[3]
            risk_score_4 = risk_score_list[3]
        if min_list[4] != None and max_list[4] != None:
            min_5 = json.loads(min_list[4])
            max_5 = json.loads(max_list[4])
            risk_score_5 = json.loads(risk_score_list[4])
        else:
            min_5 = min_list[4]
            max_5 = max_list[4]
            risk_score_5 = risk_score_list[4]


        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        criteria = session.query(Criteria).get(criteria_id)

        try:

            criteria.num_classes = num_classes
            criteria.min_1 = min_1
            criteria.max_1 = max_1
            criteria.risk_score_1 = risk_score_1
            criteria.min_2 = min_2
            criteria.max_2 = max_2
            criteria.risk_score_2 = risk_score_2
            criteria.min_3 = min_3
            criteria.max_3 = max_3
            criteria.risk_score_3 = risk_score_3
            criteria.min_4 = min_4
            criteria.max_4 = max_4
            criteria.risk_score_4 = risk_score_4
            criteria.min_5 = min_5
            criteria.max_5 = max_5
            criteria.risk_score_5 = risk_score_5


            session.commit()
            session.close()

            return JsonResponse({'success': "Risk classification sucessfully updated!"})
        except:
            return JsonResponse({'error': "A problem with your request exists."})


def save_weight_to_db(request):
    if request.is_ajax() and request.method == 'POST':
        criteria_id = request.POST['criteria_id']
        crit_weight = request.POST['criteria_weight']

        crit_weight = json.loads(crit_weight)

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        criteria = session.query(Criteria).get(criteria_id)

        try:

            criteria.criteria_weight = crit_weight


            session.commit()
            session.close()

            return JsonResponse({'success': "Risk weight sucessfully updated!"})
        except:
            session.close()
            return JsonResponse({'error': "A problem with your request exists."})


def ZoneClassifier(row, lof_col, cof_col, output_col, lof_ranges, cof_ranges, zone_class_list):
    # If area of input geometry is lower that the threshold value

    lmin_1 = lof_ranges[0]

    lmin_2 = lof_ranges[2]
    lmin_3 = lof_ranges[4]
    lmin_4 = lof_ranges[6]
    lmin_5 = lof_ranges[8]

    lmax_1 = lof_ranges[1]
    lmax_2 = lof_ranges[3]
    lmax_3 = lof_ranges[5]
    lmax_4 = lof_ranges[7]
    lmax_5 = lof_ranges[9]

    cmin_1 = cof_ranges[0]
    cmin_2 = cof_ranges[2]
    cmin_3 = cof_ranges[4]
    cmin_4 = cof_ranges[6]
    cmin_5 = cof_ranges[8]

    cmax_1 = cof_ranges[1]
    cmax_2 = cof_ranges[3]
    cmax_3 = cof_ranges[5]
    cmax_4 = cof_ranges[7]
    cmax_5 = cof_ranges[9]

    # print(zone_class_list)

    print(row["ZoneID"])
    print(lmin_1)
    print(lmax_1)
    print(row[lof_col])
    print(row[cof_col])

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_1) and (row[cof_col] >= cmin_1 and row[cof_col] <= cmax_1):
        rnum = zone_class_list[0]
        rnum = json.loads(rnum)
        row[output_col] = rnum[0]

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_1) and (row[cof_col] >= cmin_2 and row[cof_col] <= cmax_2):
        rnum = zone_class_list[0]
        rnum = json.loads(rnum)
        row[output_col] = rnum[1]

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_1) and (row[cof_col] >= cmin_3 and row[cof_col] <= cmax_3):
        rnum = zone_class_list[0]
        rnum = json.loads(rnum)
        row[output_col] = rnum[2]

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_1) and (row[cof_col] >= cmin_4 and row[cof_col] <= cmax_4):
        rnum = zone_class_list[0]
        rnum = json.loads(rnum)
        row[output_col] = rnum[3]

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_1) and (row[cof_col] >= cmin_5 and row[cof_col] <= cmax_5):
        rnum = zone_class_list[0]
        rnum = json.loads(rnum)
        row[output_col] = rnum[4]


    #####

    if (row[lof_col] >= lmin_2 and row[lof_col] <= lmax_2) and (row[cof_col] >= cmin_1 and row[cof_col] <= cmax_1):
        rnum = zone_class_list[1]
        rnum = json.loads(rnum)
        row[output_col] = rnum[0]

    if (row[lof_col] >= lmin_2 and row[lof_col] <= lmax_2) and (row[cof_col] >= cmin_2 and row[cof_col] <= cmax_2):
        rnum = zone_class_list[1]
        rnum = json.loads(rnum)
        row[output_col] = rnum[1]

    if (row[lof_col] >= lmin_2 and row[lof_col] <= lmax_2) and (row[cof_col] >= cmin_3 and row[cof_col] <= cmax_3):
        rnum = zone_class_list[1]
        rnum = json.loads(rnum)
        row[output_col] = rnum[2]

    if (row[lof_col] >= lmin_2 and row[lof_col] <= lmax_2) and (row[cof_col] >= cmin_4 and row[cof_col] <= cmax_4):
        rnum = zone_class_list[1]
        rnum = json.loads(rnum)
        row[output_col] = rnum[3]

    if (row[lof_col] >= lmin_2 and row[lof_col] <= lmax_2) and (row[cof_col] >= cmin_5 and row[cof_col] <= cmax_5):
        rnum = zone_class_list[1]
        rnum = json.loads(rnum)
        row[output_col] = rnum[4]



    ######

    if (row[lof_col] >= lmin_3 and row[lof_col] <= lmax_3) and (row[cof_col] >= cmin_1 and row[cof_col] <= cmax_1):
        rnum = zone_class_list[2]
        rnum = json.loads(rnum)
        row[output_col] = rnum[0]

    if (row[lof_col] >= lmin_3 and row[lof_col] <= lmax_3) and (row[cof_col] >= cmin_2 and row[cof_col] <= cmax_2):
        rnum = zone_class_list[2]
        rnum = json.loads(rnum)
        row[output_col] = rnum[1]

    if (row[lof_col] >= lmin_1 and row[lof_col] <= lmax_3) and (row[cof_col] >= cmin_3 and row[cof_col] <= cmax_3):
        rnum = zone_class_list[2]
        rnum = json.loads(rnum)
        row[output_col] = rnum[2]

    if (row[lof_col] >= lmin_3 and row[lof_col] <= lmax_3) and (row[cof_col] >= cmin_4 and row[cof_col] <= cmax_4):
        rnum = zone_class_list[2]
        rnum = json.loads(rnum)
        row[output_col] = rnum[3]

    if (row[lof_col] >= lmin_3 and row[lof_col] <= lmax_3) and (row[cof_col] >= cmin_5 and row[cof_col] <= cmax_5):
        rnum = zone_class_list[2]
        rnum = json.loads(rnum)
        row[output_col] = rnum[4]



    ######

    if (row[lof_col] >= lmin_4 and row[lof_col] <= lmax_4) and (row[cof_col] >= cmin_1 and row[cof_col] <= cmax_1):
        rnum = zone_class_list[3]
        rnum = json.loads(rnum)
        row[output_col] = rnum[0]

    if (row[lof_col] >= lmin_4 and row[lof_col] <= lmax_4) and (row[cof_col] >= cmin_2 and row[cof_col] <= cmax_2):
        rnum = zone_class_list[3]
        rnum = json.loads(rnum)
        row[output_col] = rnum[1]

    if (row[lof_col] >= lmin_4 and row[lof_col] <= lmax_4) and (row[cof_col] >= cmin_3 and row[cof_col] <= cmax_3):
        rnum = zone_class_list[3]
        rnum = json.loads(rnum)
        row[output_col] = rnum[2]

    if (row[lof_col] >= lmin_4 and row[lof_col] <= lmax_4) and (row[cof_col] >= cmin_4 and row[cof_col] <= cmax_4):
        rnum = zone_class_list[3]
        rnum = json.loads(rnum)
        row[output_col] = rnum[3]

    if (row[lof_col] >= lmin_4 and row[lof_col] <= lmax_4) and (row[cof_col] >= cmin_5 and row[cof_col] <= cmax_5):
        rnum = zone_class_list[3]
        rnum = json.loads(rnum)
        row[output_col] = rnum[4]


    ######

    if (row[lof_col] >= lmin_5 and row[lof_col] <= lmax_5) and (row[cof_col] >= cmin_1 and row[cof_col] <= cmax_1):
        rnum = zone_class_list[4]
        rnum = json.loads(rnum)
        row[output_col] = rnum[0]

    if (row[lof_col] >= lmin_5 and row[lof_col] <= lmax_5) and (row[cof_col] >= cmin_2 and row[cof_col] <= cmax_2):
        rnum = zone_class_list[4]
        rnum = json.loads(rnum)
        row[output_col] = rnum[1]

    if (row[lof_col] >= lmin_5 and row[lof_col] <= lmax_5) and (row[cof_col] >= cmin_3 and row[cof_col] <= cmax_3):
        rnum = zone_class_list[4]
        rnum = json.loads(rnum)
        row[output_col] = rnum[2]

    if (row[lof_col] >= lmin_5 and row[lof_col] <= lmax_5) and (row[cof_col] >= cmin_4 and row[cof_col] <= cmax_4):
        rnum = zone_class_list[4]
        rnum = json.loads(rnum)
        row[output_col] = rnum[3]

    if (row[lof_col] >= lmin_5 and row[lof_col] <= lmax_5) and (row[cof_col] >= cmin_5 and row[cof_col] <= cmax_5):
        rnum = zone_class_list[4]
        rnum = json.loads(rnum)
        row[output_col] = rnum[4]



    # If area of input geometry is higher than the threshold value update with value 1

    # Return the updated row
    return row


def save_zone_classification_to_db (request):
    if request.is_ajax() and request.method == 'POST':
        risk_analysis_nm = request.POST['risk_analysis_name']
        zone_category_list = request.POST['zone_category_list']
        lof_breaks = request.POST['lof_breaks']
        cof_breaks = request.POST['cof_breaks']

        zone_category_list = json.loads(zone_category_list)
        row1 = zone_category_list[0]
        row2 = zone_category_list[1]
        row3 = zone_category_list[2]
        row4 = zone_category_list[3]
        row5 = zone_category_list[4]

        row1 = json.loads(row1)
        row2 = json.loads(row2)
        row3 = json.loads(row3)
        row4 = json.loads(row4)
        row5 = json.loads(row5)



        r1c1 = (row1[0])
        r1c2 = (row1[1])
        r1c3 = (row1[2])
        r1c4 = (row1[3])
        r1c5 = (row1[4])

        r2c1 = (row2[0])
        r2c2 = (row2[1])
        r2c3 = (row2[2])
        r2c4 = (row2[3])
        r2c5 = (row2[4])

        r3c1 = (row3[0])
        r3c2 = (row3[1])
        r3c3 = (row3[2])
        r3c4 = (row3[3])
        r3c5 = (row3[4])

        r4c1 = (row4[0])
        r4c2 = (row4[1])
        r4c3 = (row4[2])
        r4c4 = (row4[3])
        r4c5 = (row4[4])

        r5c1 = (row5[0])
        r5c2 = (row5[1])
        r5c3 = (row5[2])
        r5c4 = (row5[3])
        r5c5 = (row5[4])


        print(r1c5)

        lof_breaks = json.loads(lof_breaks)
        cof_breaks = json.loads(cof_breaks)

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        allzclasses = session.query(Zoneclass).all()
        for entry in allzclasses:
            session.delete(entry)

        zclass = Zoneclass(risk_analysis_name = risk_analysis_nm,
                            row1col1 = r1c1,
                            row1col2 = r1c2,
                            row1col3 = r1c3,
                            row1col4 = r1c4,
                            row1col5 = r1c5,
                            row2col1 = r2c1,
                            row2col2 = r2c2,
                            row2col3 = r2c3,
                            row2col4 = r2c4,
                            row2col5 = r2c5,
                            row3col1 = r3c1,
                            row3col2 = r3c2,
                            row3col3 = r3c3,
                            row3col4 = r3c4,
                            row3col5 = r3c5,
                            row4col1 = r4c1,
                            row4col2 = r4c2,
                            row4col3 = r4c3,
                            row4col4 = r4c4,
                            row4col5 = r4c5,
                            row5col1 = r5c1,
                            row5col2 = r5c2,
                            row5col3 = r5c3,
                            row5col4 = r5c4,
                            row5col5 = r5c5 )

        session.add(zclass)



        session.commit()
        session.close()


        row1 = zone_category_list[0]
        row1adj = json.loads(row1)


        SHP_DIR = USER_DIR

        SHP_DIR = os.path.join(SHP_DIR, '')

        for file in os.listdir(SHP_DIR):
            # Reading the shapefile only
            if file.endswith(".shp"):
                f_path = os.path.join(SHP_DIR, file)





        target_df = geopandas.GeoDataFrame.from_file(f_path)
        print(target_df.crs)
        zone_crs = target_df.crs

        lcolumn = target_df["TOT_LOF_RS"]
        ccolumn = target_df["TOT_COF_RS"]


        lmin_1 = 0
        lmin_2 = lcolumn.max()*(json.loads(lof_breaks[0])/100)+0.00001
        lmin_3 = lcolumn.max()*(json.loads(lof_breaks[1]) / 100)+0.00001
        lmin_4 = lcolumn.max()*(json.loads(lof_breaks[2]) / 100)+0.00001
        lmin_5 = lcolumn.max()*(json.loads(lof_breaks[3]) / 100)+0.00001


        lmax_1 = lcolumn.max()*((json.loads(lof_breaks[0])) / 100)
        lmax_2 = lcolumn.max()*((json.loads(lof_breaks[1])) / 100)
        lmax_3 = lcolumn.max()*((json.loads(lof_breaks[2])) / 100)
        lmax_4 = lcolumn.max()*((json.loads(lof_breaks[3])) / 100)
        lmax_5 = lcolumn.max()

        cmin_1 = 0
        cmin_2 = ccolumn.max()*(json.loads(cof_breaks[0]) / 100)+0.00001
        cmin_3 = ccolumn.max()*(json.loads(cof_breaks[1]) / 100)+0.00001
        cmin_4 = ccolumn.max()*(json.loads(cof_breaks[2]) / 100)+0.00001
        cmin_5 = ccolumn.max()*(json.loads(cof_breaks[3]) / 100)+0.00001

        cmax_1 = ccolumn.max()*((json.loads(cof_breaks[0])) / 100)
        cmax_2 = ccolumn.max()*((json.loads(cof_breaks[1])) / 100)
        cmax_3 = ccolumn.max()*((json.loads(cof_breaks[2])) / 100)
        cmax_4 = ccolumn.max()*((json.loads(cof_breaks[3])) / 100)
        cmax_5 = ccolumn.max()


        lof_range = [lmin_1, lmax_1, lmin_2, lmax_2, lmin_3, lmax_3, lmin_4, lmax_4, lmin_5, lmax_5]
        cof_range = [cmin_1, cmax_1, cmin_2, cmax_2, cmin_3, cmax_3, cmin_4, cmax_4, cmin_5, cmax_5]

        print(lof_range)
        print(cof_range)

        return_obj = {}


        reclass_col = 'ZoneClass'

        target_df[reclass_col] = "0"


        #
        target_df = target_df.apply(ZoneClassifier, lof_col="TOT_LOF_RS", cof_col="TOT_COF_RS", output_col=reclass_col, lof_ranges=lof_range, cof_ranges=cof_range, zone_class_list=zone_category_list, axis=1)
        #
        print(target_df[reclass_col])

        # f, ax = plt.subplots(1)
        # for line in target_df['geometry']:
        #     geopandas.plotting.plot_multipolygon(ax, line, color="red", linewidth=2)
        # mplleaflet.display(fig=f, crs = target_df.crs)

        #
        # # orig_file = geopandas.GeoDataFrame.from_file(f_path)
        # #
        # # target_file = target_file.merge(target_df, on=zone_id)
        # #
        # #
        #
        target_df = target_df.set_geometry(col="geometry", drop=False, inplace=False, crs=zone_crs)
        target_df.to_file(USER_DIR+ "Output_Zones.shp", driver='ESRI Shapefile', schema=None, index=None, encoding='utf-8')
        print(target_df.crs)
        reproj_target_df = target_df.to_crs("EPSG:4326")
        extent_target_df = target_df.to_crs("EPSG:4326")
        olreproj_target_df = target_df.to_crs("EPSG:3857")

        reproj_target_df.to_file(USER_DIR+ "Output_Zones.geojson", driver='GeoJSON', schema=None, index=None, encoding='utf-8')
        olreproj_target_df.to_file(USER_DIR+ "olOutput_Zones.geojson", driver='GeoJSON', schema=None, index=None, encoding='utf-8')

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        all_lof_criteria = session.query(Criteria).filter_by(criteria_type="LOF")

        all_cof_criteria = session.query(Criteria).filter_by(criteria_type="COF")

        zone_list = target_df.index.to_list()

        table_field_names = []
        table_rows = []

        for lof_crit in all_lof_criteria:
            lof_risk_field = lof_crit.criteria_name + "RS"
            table_field_names.append(lof_risk_field)
        table_field_names.append("TOT_LOF_RS")

        for cof_crit in all_cof_criteria:
            cof_risk_field = cof_crit.criteria_name + "RS"
            table_field_names.append(cof_risk_field)
        table_field_names.append("TOT_COF_RS")
        table_field_names.append("TOTAL_RISK")
        table_field_names.append("ZoneClass")



        for i in range(len(zone_list)):
            row = []
            row.append(zone_list[i])
            for col in table_field_names:
                riskcolvals = target_df[col].to_list()
                row.append(riskcolvals[i])
            print(row)
            table_rows.append(row)
            print(table_rows)


        if not extent_target_df.empty:
            this_bounds = extent_target_df.total_bounds
            x1, y1, x2, y2 = this_bounds[0], this_bounds[1], this_bounds[2], this_bounds[3]
            this_extent = [[y1, x1], [y2, x2]]
            return_obj["extent"] = this_extent



        g_path = os.path.join(SHP_DIR, "Output_Zones.geojson")

        geojson_features = []
        with fiona.open(g_path) as data_file:
            for data in data_file:
                # print(data)
                geojson_features.append(data)

        # return_obj["GeoJSON_File"] = data_file
        return_obj["GeoJSON_Features"] = geojson_features




        return JsonResponse(return_obj)

def get_zone_classes_from_db (request):
    if request.is_ajax() and request.method == 'POST':

        return_obj = {}

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        allzclasses = session.query(Zoneclass).all()

        for entry in allzclasses:
            row1 = [entry.row1col1,
                    entry.row1col2,
                    entry.row1col3,
                    entry.row1col4,
                    entry.row1col5]

            row2 = [entry.row2col1,
                    entry.row2col2,
                    entry.row2col3,
                    entry.row2col4,
                    entry.row2col5]

            row3 = [entry.row3col1,
                     entry.row3col2,
                     entry.row3col3,
                     entry.row3col4,
                     entry.row3col5]

            row4 = [entry.row4col1,
                    entry.row4col2,
                    entry.row4col3,
                    entry.row4col4,
                    entry.row4col5]

            row5 = [entry.row5col1,
                    entry.row5col2,
                    entry.row5col3,
                    entry.row5col4,
                    entry.row5col5]

        session.close()

        return_obj["row1"] = row1
        return_obj["row2"] = row2
        return_obj["row3"] = row3
        return_obj["row4"] = row4
        return_obj["row5"] = row5

        return JsonResponse(return_obj)

def get_zone_charts (request):
    if request.is_ajax() and request.method == 'POST':
        zone_id = request.POST['zone_id']
        print(zone_id)
        num_zones = request.POST['num_zones']
        num_zones = json.loads(num_zones)
        return_obj = {}

        Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        cof_name_list = []
        lof_name_list = []
        cof_score_list = []
        lof_score_list = []
        lof_percentile_list = []
        cof_percentile_list = []

        all_lof_criteria = session.query(Criteria).filter_by(criteria_type="LOF")

        all_cof_criteria = session.query(Criteria).filter_by(criteria_type="COF")


        zone_df = geopandas.GeoDataFrame.from_file(USER_DIR+ "Output_Zones.shp")

        zone_df_orig = zone_df
        zone_df.set_index("ZoneID", inplace=True)
        zone_data_row = zone_df.loc[zone_id]

        for lof_entry in all_lof_criteria:
            lfield = lof_entry.criteria_name +"RS"
            max_lof_score = zone_df[lfield].max()
            lof_risk_score = zone_data_row[lfield]

            lof_percentile = (lof_risk_score) / max_lof_score * 100

            lof_name_list.append(lof_entry.criteria_name)
            lof_score_list.append(lof_risk_score)
            lof_percentile_list.append(lof_percentile)


        for cof_entry in all_cof_criteria:
            cfield = cof_entry.criteria_name + "RS"
            max_cof_score = zone_df[cfield].max()
            cof_risk_score = zone_data_row[cfield]

            cof_percentile = (cof_risk_score)/max_cof_score * 100

            cof_name_list.append(cof_entry.criteria_name)
            cof_score_list.append(cof_risk_score)
            cof_percentile_list.append(cof_percentile)

        bar_total_data = zone_df_orig.nlargest(num_zones,"TOTAL_RISK")

        cof_bar_total_data = zone_df_orig.nlargest(num_zones, "TOT_COF_RS")

        lof_bar_total_data = zone_df_orig.nlargest(num_zones, "TOT_LOF_RS")


        print(cof_bar_total_data)
        top_tot_zones = bar_total_data.index.tolist()
        top_tot_vals = bar_total_data["TOTAL_RISK"].tolist()

        tot_color_list = []

        for data in top_tot_zones:
            if data == zone_id:
                tot_colorbar = "ffcc00"
            else: tot_colorbar = "#056eb7"

            tot_color_list.append(tot_colorbar)

        temp_tot_list = []
        for z in top_tot_zones:
            zs = "Zone #" + str(z)
            temp_tot_list.append(zs)

        top_tot_zones = temp_tot_list


        top_lof_zones = lof_bar_total_data.index.tolist()
        top_lof_vals = lof_bar_total_data["TOT_LOF_RS"].tolist()

        lof_color_list = []

        for data in top_lof_zones:
            if data == zone_id:
                lof_colorbar = "ffcc00"
            else:
                lof_colorbar = "#056eb7"

            lof_color_list.append(lof_colorbar)

        temp_lof_list = []
        for z in top_lof_zones:
            zs = "Zone #" + str(z)
            temp_lof_list.append(zs)

        top_lof_zones = temp_lof_list


        top_cof_zones = cof_bar_total_data.index.tolist()


        top_cof_vals = cof_bar_total_data["TOT_COF_RS"].tolist()

        cof_color_list = []

        for data in top_cof_zones:
            if data == zone_id:
                cof_colorbar = "ffcc00"
            else:
                cof_colorbar = "#056eb7"

            cof_color_list.append(cof_colorbar)

        temp_cof_list = []
        for z in top_cof_zones:
            zs = "Zone #" + str(z)
            temp_cof_list.append(zs)

        top_cof_zones = temp_cof_list

        g_path = os.path.join(USER_DIR, "Output_Zones.geojson")

        geojson_features = []
        with fiona.open(g_path) as data_file:
            for data in data_file:
                # print(data)
                geojson_features.append(data)

        # return_obj["GeoJSON_File"] = data_file

        session.close()

        return_obj["GeoJSON_Features"] = geojson_features


        return_obj["top_lof_zones"] = top_lof_zones
        return_obj["top_cof_zones"] = top_cof_zones
        return_obj["top_tot_zones"] = top_tot_zones

        return_obj["top_lof_vals"] = top_lof_vals
        return_obj["top_cof_vals"] = top_cof_vals
        return_obj["top_tot_vals"] = top_tot_vals

        return_obj["cof_color_list"] = cof_color_list
        return_obj["lof_color_list"] = lof_color_list
        return_obj["tot_color_list"] = tot_color_list

        return_obj["cof_name_list"] = cof_name_list
        return_obj["lof_name_list"] = lof_name_list
        return_obj["cof_score_list"] = cof_score_list
        return_obj["lof_score_list"] = lof_score_list
        return_obj["cof_percentile_list"] = cof_percentile_list
        return_obj["lof_percentile_list"] = lof_percentile_list


        return JsonResponse(return_obj)


def get_mini_geojson_features (request):
    if request.is_ajax() and request.method == 'POST':
        zone_id = request.POST['zone_id']
        print(zone_id)
        return_obj = {}


        zone_df = geopandas.GeoDataFrame.from_file(USER_DIR+ "Output_Zones.shp")
        zone_df = zone_df.to_crs("EPSG:3857")
        zone_df.set_index("ZoneID", inplace=True)
        zone_data_row = zone_df.loc[zone_id]
        print(zone_data_row)
        # print(zone_data_row.loc[geometry])

        g_path = os.path.join(USER_DIR, "olOutput_Zones.geojson")

        geojson_features = []
        with fiona.open(g_path) as data_file:
            for data in data_file:
                # print(data)
                geojson_features.append(data)

        # return_obj["GeoJSON_File"] = data_file


        return_obj["GeoJSON_Features"] = geojson_features






        return JsonResponse(return_obj)

def datatable_ajax(request):
    """
    Controller for the datatable ajax request.
    """



    target_df = geopandas.GeoDataFrame.from_file(USER_DIR+ "Output_Zones.shp")

    Session = Hpp.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    all_lof_criteria = session.query(Criteria).filter_by(criteria_type="LOF")

    all_cof_criteria = session.query(Criteria).filter_by(criteria_type="COF")

    zone_list = target_df["ZoneID"].to_list()

    table_field_names = []
    table_rows = []

    for lof_crit in all_lof_criteria:
        lof_risk_field = lof_crit.criteria_name + "RS"
        table_field_names.append(lof_risk_field)
    table_field_names.append("TOT_LOF_RS")

    for cof_crit in all_cof_criteria:
        cof_risk_field = cof_crit.criteria_name + "RS"
        table_field_names.append(cof_risk_field)
    table_field_names.append("TOT_COF_RS")
    table_field_names.append("TOTAL_RISK")
    table_field_names.append("ZoneClass")

    for i in range(len(zone_list)):
        row = []
        row.append(zone_list[i])
        for col in table_field_names:
            riskcolvals = target_df[col].to_list()
            row.append(riskcolvals[i])

        table_rows.append(row)
    table_field_names.insert(0,"ZoneID")

    datatable_default = DataTableView(column_names=table_field_names,
                                      rows= table_rows,
                                      searching=True,
                                      orderClasses=False,
                                      lengthMenu=[ [10, 25, 50, -1], [10, 25, 50, "All"] ],
                                      )

    session.close()

    context = {'datatable_options': datatable_default}

    return render(request, 'hpp/datatable_ajax.html', context)
