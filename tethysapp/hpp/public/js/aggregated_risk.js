var currentTab = 0; // Current tab is set to be the first tab (0)
var map;
var view;


function uncheckAll() {
        var inputs = document.querySelectorAll('.checkbox-input');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].checked = false;
            var inputValue = inputs[i].value;


            if(inputs[i].checked == true){
                document.getElementById(inputValue).style.display ="block";
            }
            else if(inputs[i].checked == false){
                document.getElementById(inputValue).style.display ="none"};
        };

};
function logAndClearSubweightData(){


        }

function showSubweightsModal (){

//        if(input_element.checked == true){
//            document.getElementById(inputValue).style.display ="block";
//        };

        $("#subweights-modal").modal('show');


};

function hideShow(checkbox_id){
        var input_element =document.getElementById(checkbox_id)
        var inputValue = input_element.value;


        if(input_element.checked == true){
            document.getElementById(inputValue).style.display ="block";
        }
        else if(input_element.checked == false){
            document.getElementById(inputValue).style.display ="none"
        };
    };

function clearFile (checkbox_id,close_id){
        document.getElementById(checkbox_id).style.display ="none";
        document.getElementById(close_id).style.display ="none";

        var n = checkbox_id.slice(0,(checkbox_id.search("-")));
        $('#'+n+'-shp-upload-input').val('');
        $('#'+n+'-file-num-fields').val(0);
        checkNumberOfFields(n+'-file-num-fields',n+'-field-');



        for (var i = 1; i < 11; i++) {
            $('#'+n+'-criteria-name-'+i).val('');
            $('#'+n+'-field-select-'+i).val('');
            if (document.getElementById(n+'-add-subweights-checkbox-'+i).checked ==true){
                document.getElementById(n+'-add-subweights-checkbox-'+i).checked =false;
            };

            $('#'+n+'-agg-method-select-'+i).val('sum');
            $('#'+n+'-lof-or-cof-select-'+i).val('lof');
        };
        if (document.getElementById(n+'-checkbox').checked ==true){
                document.getElementById(n+'-checkbox').checked =false;
        };
        document.getElementById(n+'-file-inputs').style.display = 'none';

};

function hideShowCustomCheck(){
        var custom_file_name = $('#custom-file-name-input').val();
        console.log(custom_file_name);
        var inputs = document.querySelectorAll('.custom-check');
        for (var i = 0; i < inputs.length; i++) {

           if(inputs[i].style.display == "block"){continue};


           if(inputs[i].style.display == "none"){
           var checkbox_label = document.getElementById(inputs[i].id+'box-label');
           console.log(inputs[i].id+'-label');

           checkbox_label.innerHTML = custom_file_name;
           var id_str = inputs[i].id;
           var n = id_str.slice(0,(id_str.search("-")));
           document.getElementById(n+'-close').style.display = "block";

           inputs[i].style.display = "block";



           break};

//


        };

    };

function hideCustomFields() {
        var inputs = document.querySelectorAll('.custom-check');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].style.display = 'none';

        };

};

function hideShowFieldDivs(div_id){



        if(document.getElementById(div_id).style.display == "none"){
            document.getElementById(div_id).style.display ="block";
        }
//        else if(document.getElementById(div_id).style.display == "block"){
//            document.getElementById(div_id).style.display ="none"}
};

function checkNumberOfFields(dropdown_id,div_id) {
    var num_fields = $('#'+dropdown_id).val();

    for(var i = 1, l = 11; i < l; ++i){

            document.getElementById(div_id+i).style.display ="none";
         }

    for(var i = 1, l = num_fields; i <= l; ++i){


        hideShowFieldDivs(div_id + i);
      }
};
//require(["esri/Map", "esri/views/MapView"], function(Map, MapView) {
//        var map = new Map({
//          basemap: "streets"
//        });
//        var view = new MapView({
//          container: "showzonemap", // Reference to the scene div created in step 5
//          map: map, // Reference to the map object created before the scene
//          zoom: 12, // Sets zoom level based on level of detail (LOD)
//          center: [-93.25, 44.75] // Sets center point of view using longitude,latitude
//        });
//      });

//function showTab(n) {
//  // This function will display the specified tab of the form ...
//  var x = document.getElementsByClassName("tab");
//  x[n].style.display = "block";
//  // ... and fix the Previous/Next buttons:
//  if (n == 0) {
//    document.getElementById("prevBtn").style.display = "none";
//  } else {
//    document.getElementById("prevBtn").style.display = "inline";
//  }
//  if (n == (x.length - 1)) {
//    document.getElementById("nextBtn").innerHTML = "Submit";
//  } else {
//    document.getElementById("nextBtn").innerHTML = "Next";
//  }
//  // ... and run a function that displays the correct step indicator:
//  fixStepIndicator(n)
//}
//
//function nextPrev(n) {
//  // This function will figure out which tab to display
//  var x = document.getElementsByClassName("tab");
//  // Exit the function if any field in the current tab is invalid:
//  if (n == 1 && !validateForm()) return false;
//  // Hide the current tab:
//  x[currentTab].style.display = "none";
//  // Increase or decrease the current tab by 1:
//  currentTab = currentTab + n;
//  // if you have reached the end of the form... :
//  if (currentTab >= x.length) {
//    //...the form gets submitted:
//    document.getElementById("regForm").submit();
//    return false;
//  }
//  // Otherwise, display the correct tab:
//  showTab(currentTab);
//}
//
//function validateForm() {
//  // This function deals with validation of the form fields
//  var x, y, i, valid = true;
//  x = document.getElementsByClassName("tab");
//  y = x[currentTab].getElementsByTagName("input");
//  // A loop that checks every input field in the current tab:
//  for (i = 0; i < y.length; i++) {
//    // If a field is empty...
//    if (y[i].value == "") {
//      // add an "invalid" class to the field:
//      y[i].className += " invalid";
//      // and set the current valid status to false:
//      valid = false;
//    }
//  }
//  // If the valid status is true, mark the step as finished and valid:
//  if (valid) {
//    document.getElementsByClassName("step")[currentTab].className += " finish";
//  }
//  return valid; // return the valid status
//}
//
//function fixStepIndicator(n) {
//  // This function removes the "active" class of all steps...
//  var i, x = document.getElementsByClassName("step");
//  for (i = 0; i < x.length; i++) {
//    x[i].className = x[i].className.replace(" active", "");
//  }
//  //... and adds the "active" class to the current step:
//  x[n].className += " active";
//}

//zone_upload_process = function(data) {
//        var zone_upload = ajax_update_database_with_file("zone-upload",data); //Submitting the data through the ajax function, see main.js for the helper function.
//        zone_upload.done(function(return_data){ //Reset the form once the data is added successfully
//            if("field_names" in return_data){
//                var submit_button = $("#init-risk-analysis");
//                var submit_button_html = submit_button.html();
//                submit_button.text('Submitted');
//                var options = return_data.field_names;
//                console.log(options)
//
//                var select = document.getElementById("zoneid-field");
////                var options = ["1", "2", "3", "4", "5"];
//
//                // Optional: Clear all existing options first:
//                select.innerHTML = "<option value=\"" + "Select Field" + "\">" + "Select Field" + "</option>";
//                // Populate list with options:
//                for(var i = 0; i < options.length; i++) {
//                    var opt = options[i];
//                    select.innerHTML += "<option value=\"" + opt + "\">" + opt + "</option>";
//                }
////
//            };
//
//        });
//};
function uploadFileNoFields(file_upload_id,file_name){
        var shapefiles = $(file_upload_id)[0].files;
//        var file_name = "zone_file"
        //Preparing data to be submitted via AJAX POST request
        var data = new FormData();
        data.append("file_name",file_name);
        for(var i=0;i < shapefiles.length;i++){
            data.append("shapefile",shapefiles[i]);
        }


//        var submit_button = $("#init-risk-analysis");
//        var submit_button_html = submit_button.html();
//        submit_button.text('Submitting ...');


        file_upload_process_no_fields(file_upload_id, data);

        };



function file_upload_process_no_fields(file_upload_id, data) {
        var file_upload = ajax_update_database_with_file("file-upload-move-files",data); //Submitting the data through the ajax function, see main.js for the helper function.
        file_upload.done(function(return_data){ //Reset the form once the data is added successfully
            if("success" in return_data){
                var file_upload_button = $(file_upload_id);
                var file_upload_button_html = file_upload_button.html();
                file_upload_button.text('File Uploaded');

//
            };

        });
};

function executeSpatialJoins(){

        var inputs = document.querySelectorAll('.checkbox-input');
        console.log(inputs);
        var data = new FormData();
        var file_names = [];
        var criteria_name_array =[];
        var field_name_array = [];
        var aggregation_method_array = [];
        var criteria_type_array = [];


        for (var i = 0; i < inputs.length; i++) {
            console.log('i is '+i)

            if(inputs[i].checked == true){
                var id_str = inputs[i].id;
//                console.log(id_str);

                var n = id_str.slice(0,(id_str.search("-")));
                var file_name = n +'_file';
                console.log(file_name);

                file_names.push(file_name);

                console.log(file_names)


                var file_inputs_div = document.getElementById(n+'-file-inputs');
//                console.log(file_inputs_div);
                field_dropdowns = file_inputs_div.getElementsByClassName("criteria-inputs");
//                field_dropdowns = Array.prototype.slice.call(field_dropdowns);
//                console.log(field_dropdowns);
                for (var j = 0; j < (field_dropdowns.length); j++) {

                    if(field_dropdowns[j].style.display == 'block'){
//                        console.log(field_dropdowns[i]);
                        console.log(n+"-criteria-name-"+(j+1))
                        var criteria_name_id = document.getElementById(n+"-criteria-name-"+(j+1));
                        var field_name_id = document.getElementById(n+"-field-select-"+(j+1));
                        var subweights_checkbox_id = document.getElementById(n+"-add-subweights-checkbox-"+(j+1));
                        var aggregation_method_id = document.getElementById(n+"-agg-method-select-"+(j+1));
                        var criteria_type_id = document.getElementById(n+"-lof-or-cof-select-"+(j+1));
                        console.log(field_name_id.value);

                        criteria_name_array.push(n+'_'+criteria_name_id.value);
                        field_name_array.push(n+'_'+field_name_id.value);
                        aggregation_method_array.push(n+'_'+aggregation_method_id.value);
                        criteria_type_array.push(n+'_'+criteria_type_id.value);



//                        ****subweight data function




//                        data.append(n+"_criteria_name_"+(i+1),criteria_name_id.value);
//                        data.append(n+"_field_name_"+(i+1),field_name_id.value);
//                        data.append(n+"_agg_method_"+(i+1),aggregation_method_id.value);
//                        data.append(n+"_criteria_type_"+(i+1),criteria_type_id.value);

//                        zone_spatial_join_process(data, file_name, "#data-submit-button")

//
                    };
                };
            };
        };
        console.log(criteria_name_array);
        console.log(field_name_array);
        console.log(aggregation_method_array);
        console.log(criteria_type_array);


        data.append("file_names",file_names);
        data.append("criteria_names",criteria_name_array);
        data.append("field_names",field_name_array);
        data.append("aggregation_methods",aggregation_method_array);
        data.append("criteria_types",criteria_type_array);


//                        zone_spatial_join_process(data, file_name, "#data-submit-button")



};





execute_spatial_join = function(file_name){

//        var file_name = "jct_file"
        //Preparing data to be submitted via AJAX POST request
        var data = new FormData();
        data.append("file_name",file_name);


        var submit_button = $("#data-submit-button");
        var submit_button_html = submit_button.html();
        submit_button.text('Uploading ...');


        zone_spatial_join_process(data, file_name, "#data-submit-button");

    };

zone_spatial_join_process = function(data,file_name,upload_button_id) {
        var file_upload_button = $(upload_button_id);
        var file_upload_button_html = file_upload_button.html();
        file_upload_button.text('Joining '+file_name+' data...')

        var file_upload = ajax_update_database_with_file("zone-spatial-join",data); //Submitting the data through the ajax function, see main.js for the helper function.
        file_upload.done(function(return_data){ //Reset the form once the data is added successfully
            if("success" in return_data){

                file_upload_button.text('Done');

//
            };

        });
};



function uploadFile(file_upload_id,file_name){
        var shapefiles = $(file_upload_id)[0].files;
//        var file_name = "zone_file"
        //Preparing data to be submitted via AJAX POST request
        var data = new FormData();
        data.append("file_name",file_name);
        for(var i=0;i < shapefiles.length;i++){
            data.append("shapefile",shapefiles[i]);
        }
        var field_list = [];
        for(var j=0; j<10;j++){
            var n = file_name.slice(0,(file_name.search("_")));
            field_list[j] = n+'-field-select-'+(j+1);

        }
        console.log(field_list);
//        var submit_button = $("#init-risk-analysis");
//        var submit_button_html = submit_button.html();
//        submit_button.text('Submitting ...');


        file_upload_process(data,field_list);

        };

function file_upload_process(data,field_list) {
        var file_upload = ajax_update_database_with_file("file-upload",data); //Submitting the data through the ajax function, see main.js for the helper function.
        file_upload.done(function(return_data){ //Reset the form once the data is added successfully
            if("field_names" in return_data){
//                var submit_button = $("#init-risk-analysis");
//                var submit_button_html = submit_button.html();
//                submit_button.text('Submitted');
                var options = return_data.field_names;
                console.log(options);
                console.log(field_list);
                for(var j=0; j < field_list.length; j++){

                    console.log(field_list.length);

                    var select = document.getElementById(field_list[j]);
    //                var options = ["1", "2", "3", "4", "5"];

                    // Optional: Clear all existing options first:
                    select.innerHTML = "<option value=\"" + "Select Field" + "\">" + "Select Field" + "</option>";
                    // Populate list with options:
                    for(var i = 0; i < options.length; i++) {
                        var opt = options[i];
                        select.innerHTML += "<option value=\"" + opt + "\">" + opt + "</option>";
                    }
                };


//                var select = document.getElementById(field_one_select);
////                var options = ["1", "2", "3", "4", "5"];
//
//                // Optional: Clear all existing options first:
//                select.innerHTML = "<option value=\"" + "Select Field" + "\">" + "Select Field" + "</option>";
//                // Populate list with options:
//                for(var i = 0; i < options.length; i++) {
//                    var opt = options[i];
//                    select.innerHTML += "<option value=\"" + opt + "\">" + opt + "</option>";
//                }
////
//
//                console.log(field_two_select)
//
//
//                var select_two = document.getElementById(field_two_select);
//    //                var options = ["1", "2", "3", "4", "5"];
//
//                // Optional: Clear all existing options first:
//                select_two.innerHTML = "<option value=\"" + "Select Field" + "\">" + "Select Field" + "</option>";
//                // Populate list with options:
//                for(var i = 0; i < options.length; i++) {
//                    var opt = options[i];
//                    select_two.innerHTML += "<option value=\"" + opt + "\">" + opt + "</option>";
//                }



            };

        });
};


$(function() {
    uncheckAll();
    hideCustomFields();




    checkNumberOfFields('zone-file-num-fields','zone-field-');
    checkNumberOfFields('subcat-file-num-fields','subcat-field-');
    checkNumberOfFields('pipe-file-num-fields','pipe-field-');
    checkNumberOfFields('bld-file-num-fields','bld-field-');
    checkNumberOfFields('street-file-num-fields','street-field-');
    checkNumberOfFields('jct-file-num-fields','jct-field-');
    checkNumberOfFields('ls-file-num-fields','ls-field-');
    checkNumberOfFields('1custom-file-num-fields','1custom-field-');
    checkNumberOfFields('2custom-file-num-fields','2custom-field-');
    checkNumberOfFields('3custom-file-num-fields','3custom-field-');
    checkNumberOfFields('4custom-file-num-fields','4custom-field-');
    checkNumberOfFields('5custom-file-num-fields','5custom-field-');




    $('#zone-shp-upload-input').change(function(){
        uploadFile('#zone-shp-upload-input','zone_file');
    });

    $('#zone-file-num-fields').change(function(){
        checkNumberOfFields('zone-file-num-fields','zone-field-')
    });
    $('#subcatchment-shp-upload-input').change(function(){
        uploadFile('#subcatchment-shp-upload-input','subcat_file');
    });
    $('#subcat-file-num-fields').change(function(){
        checkNumberOfFields('subcat-file-num-fields','subcat-field-')
    });
    $('#pipe-shp-upload-input').change(function(){
        uploadFile('#pipe-shp-upload-input','pipe_file');
    });
    $('#pipe-file-num-fields').change(function(){
        checkNumberOfFields('pipe-file-num-fields','pipe-field-')
    });
    $('#bld-shp-upload-input').change(function(){
        uploadFile('#bld-shp-upload-input','bld_file');
    });
    $('#bld-file-num-fields').change(function(){
        checkNumberOfFields('bld-file-num-fields','bld-field-')
    });
    $('#street-shp-upload-input').change(function(){
        uploadFile('#street-shp-upload-input','street_file');
    });
    $('#street-file-num-fields').change(function(){
        checkNumberOfFields('street-file-num-fields','street-field-')
    });
    $('#jct-shp-upload-input').change(function(){
        uploadFile('#jct-shp-upload-input','jct_file');
    });
    $('#jct-file-num-fields').change(function(){
        checkNumberOfFields('jct-file-num-fields','jct-field-')
    });
    $('#ls-shp-upload-input').change(function(){
        uploadFile('#ls-shp-upload-input','ls_file');
    });
    $('#ls-file-num-fields').change(function(){
        checkNumberOfFields('ls-file-num-fields','ls-field-')
    });
    $('#1custom-shp-upload-input').change(function(){
        uploadFile('#1custom-shp-upload-input','1custom_file');
    });
    $('#1custom-file-num-fields').change(function(){
        checkNumberOfFields('1custom-file-num-fields','1custom-field-')
    });
    $('#2custom-shp-upload-input').change(function(){
        uploadFile('#2custom-shp-upload-input','2custom_file');
    });
    $('#2custom-file-num-fields').change(function(){
        checkNumberOfFields('2custom-file-num-fields','2custom-field-')
    });
    $('#3custom-shp-upload-input').change(function(){
        uploadFile('#3custom-shp-upload-input','3custom_file');
    });
    $('#3custom-file-num-fields').change(function(){
        checkNumberOfFields('3custom-file-num-fields','3custom-field-')
    });
    $('#4custom-shp-upload-input').change(function(){
        uploadFile('#4custom-shp-upload-input','4custom_file');
    });
    $('#4custom-file-num-fields').change(function(){
        checkNumberOfFields('4custom-file-num-fields','4custom-field-')
    });
    $('#5custom-shp-upload-input').change(function(){
        uploadFile('#5custom-shp-upload-input','5custom_file');
    });
    $('#5custom-file-num-fields').change(function(){
        checkNumberOfFields('5custom-file-num-fields','5custom-field-')
    });
});
