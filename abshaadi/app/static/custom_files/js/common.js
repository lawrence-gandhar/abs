$(document).ready(function(){
	
	//*******************************************************************************
	// SET CLASS
	//*******************************************************************************
	
	$("select").addClass("form-control");
	$("input").addClass("form-control");
	
	//*******************************************************************************
	// AGE SLIDER
	//*******************************************************************************
	
	age_to = document.getElementById('id_aged_from');
	age_from = document.getElementById('id_aged_to');
	
	var inputs = [age_to, age_from];
	
	if(age_to.value == '') age_to_val = 25;
	else age_to_val = age_to.value;
	
	if(age_from.value == '') age_from_val = 18;
	else age_from_val = age_from.value;
	
	var stepsSlider  = document.getElementById('age_slider');
	
	noUiSlider.create(stepsSlider , {
		start: [age_from_val, age_to_val],
		connect: true,
		step: 1,
		range: {
			'min': 18,
			'max': 70
		},
		tooltips: [true, wNumb({decimals: false,})],
		format : wNumb({decimals: false,}),
	});
	
	stepsSlider.noUiSlider.on('update', function (values, handle) {
		inputs[handle].value = values[handle];
	});
	
	//*******************************************************************************
	//*******************************************************************************
	
});

/**
 * Convert a base64 string in a Blob according to the data and contentType.
 * 
 * @param b64Data {String} Pure base64 string without contentType
 * @param contentType {String} the content type of the file i.e (image/jpeg - image/png - text/plain)
 * @param sliceSize {Int} SliceSize to process the byteCharacters
 * @see http://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
 * @return Blob
 */
function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

      var blob = new Blob(byteArrays, {type: contentType});
      return blob;
}


//***********************************************************************
// Match Two Strings
//***********************************************************************
//

function match_fields_data(input1, input2, elem=null){
	
	var field1 = $(input1).val();
	var field2 = $(input2).val();
	
	if(field1 !== field2){		
		if(elem) $(elem).text("Both fields should match. It is case-sensitive");
		$(input1).addClass("is-invalid");
		$(input2).addClass("is-invalid");
		alert("Did not match");
	}else{
		$(input1).removeClass("is-invalid");
		$(input2).removeClass("is-invalid");
	}
}


//***********************************************************************
// Check Confirm Password
//***********************************************************************
//

$("#id_password2").on("focusout", function(){
	
	confirm_passwd = $(this).val();
	main_passwd = $("#id_password1").val();
		
	if(confirm_passwd!=""){
		if(main_passwd !== confirm_passwd){
			$("#passwd1_error").text("Password and Confirm Password does not match");
			$(".save_button").prop("disabled", true);
		}else{
			
			if(main_passwd.length < 8){
				$("#passwd1_error").text("This password must contain at least 8 characters.");
			}else{
				$("#passwd1_error").text("");		
				$(".save_button").prop("disabled", false);
				$(".error").text("");
			}
		}
	}else{
		$("#passwd1_error").text("Confirm Password is required.");
	}
});


//***********************************************************************
// Validate Password
//***********************************************************************
//

$("#id_password1").on("focusout", function(){
	passwd = $(this).val();
	
	if(passwd.length < 8){
		$("#passwd1_error").text("This password must contain at least 8 characters.");
	}else{
		
		confirm_passwd = $("#id_password2").val();
		main_passwd = $("#id_password1").val();
			
		if(confirm_passwd!=""){
			if(main_passwd !== confirm_passwd){
				$("#passwd1_error").text("Password and Confirm Password does not match");
				$(".save_button").prop("disabled", true);
			}else{
				
				if(main_passwd.length < 8){
					$("#passwd1_error").text("This password must contain at least 8 characters.");
				}else{
					$("#passwd1_error").text("");		
					$(".save_button").prop("disabled", false);
					$(".error").text("");
				}
			}
		}else{
			$("#passwd1_error").text("Confirm Password is required.");
		}
		
		$("#passwd1_error").text("");		
	}
});


//***********************************************************************
// Get States Dropdown
//***********************************************************************
//

$(".country_select").on('hidden.bs.select', function (e){
	
	e.stopImmediatePropagation();
	
	kk = $(this).val();
		
	if(kk.length>0){
		$.post("/get_states_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			
			$(".state-div").show();
			$("select.states_select").empty().append(data);
			$("select.states_select").selectpicker('refresh');
			
		});
	}
		
});


//***********************************************************************
// Get Cities Dropdown
//***********************************************************************
//


$(".states_select").on('hidden.bs.select', function (e){
	
	e.stopImmediatePropagation();
	
	kk = $(this).val();
	
	if(kk.length>0){
		$.post("/get_cities_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			
			$(".city-div").show();
			$("select.city_select").empty().append(data);
			$("select.city_select").selectpicker('refresh');
			
		});
	}
});


//***********************************************************************
// Get Castes Dropdown
//***********************************************************************
//

$(".religion_select").on('hidden.bs.select', function (e){
	
	e.stopImmediatePropagation();
	
	kk = $(this).val();
	
	if(kk.length>0){
		$.post("/get_castes_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			
			$(".caste-div").show();
			$("select.castes_select").empty().append(data);
			$("select.castes_select").selectpicker('refresh');
			
		});
	}
	
});


//***********************************************************************
// Save Partner Search
//***********************************************************************
//

function save_partner_search(elem, inp_name){
	formdata = $(elem).serialize();
	
	inp = $(inp_name).val();
	
	if($.trim(inp)!=""){
		
		$("#data_process_modal").modal('show');
		
		f_data = formdata + "&inp="+inp;
		
		$("#save_partner_preferences_modal").modal('hide');
				
		$.post("/save_partner_preferences/", f_data, function(data){
			console.log(data);
			$("#data_process_modal").modal('hide');
		});
		
	}else{
		$("#data_process_modal").modal('hide');
		alert('Filter Name is required');
		$(inp_name).focus();
	}
	
	
}



	
	