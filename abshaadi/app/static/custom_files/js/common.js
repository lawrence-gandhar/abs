$(document).ready(function(){

	//
	//***********************************************************************************
    // Start upload preview image
    //***********************************************************************************

	$(".gambar").attr("src", "https://user.gadjian.com/static/images/personnel_boy.png");

	var $uploadCrop,
	tempFilename,
	rawImg,
	imageId;

	$uploadCrop = $('#upload-demo').croppie({
		viewport: {
			width: 150,
			height: 150,
		},
		enforceBoundary: false,
		enableExif: true
	});


	function readFile(input) {
		if (input.files && input.files[0]) {
		  var reader = new FileReader();
			reader.onload = function (e) {
				$('#upload-demo').show();
				rawImg = e.target.result;

				$uploadCrop.croppie('bind', {
					url: rawImg
				}).then(function(){
					console.log('jQuery bind complete');
				});
			}
			reader.readAsDataURL(input.files[0]);
		}
		else {
			swal("Sorry - you're browser doesn't support the FileReader API");
		}
	}

	//
	//

	$('.item-img').on('change', function () {
		imageId = $(this).data('id');
		tempFilename = $(this).val();
		$('#cancelCropBtn').data('id', imageId);
		readFile(this);

		$("#cropImageBtn, #cropImageSubmitBtn").show();
	});


	//
	//

	$('#cropImageBtn').on('click', function (ev) {
		$uploadCrop.croppie('result', {
			type: 'base64',
			format: 'png',
			size: {width: 150, height: 200}
		}).then(function (resp) {
			$('#item-img-output').attr('src', resp);
		});
	});

	//
	//

	$('#cropImageSubmitBtn').on('click', function (ev) {

		$("#file_uploading_loader_modal").modal('show');

		$uploadCrop.croppie('result', {
			type: 'base64',
			format: 'png',
			size: {width: 170, height: 200}
		}).then(function (resp) {

			var block = resp.split(";");
			var contentType = block[0].split(":")[1];
			var realData = block[1].split(",")[1];

			var blob = b64toBlob(realData, contentType);

			var form = document.getElementById("upload_profile_pic_form");

			var formDataToUpload = new FormData(form);
			formDataToUpload.append("picture", blob);
			formDataToUpload.append("csrfmiddlewaretoken", csrfmiddlewaretoken);


			$.ajax({
				url:"/upload_profile_pic/",
				data: formDataToUpload,
				type:"POST",
				contentType:false,
				processData:false,
				cache:false,
				error:function(err){
					console.error(err);
				},
				success:function(data){
					console.log(data);
				},
				complete:function(){
					location.reload();
				}
			});


		});

	});


	//
	//

	$('#cancelCropBtn').on('click', function (ev){
		$("#profile_picture_modal").modal('hide');
	});


	//
	//
	$("#profile_picture_modal").on('hidden.bs.modal', function (e) {
		$('.item-img').val('');
		$('#upload-demo').hide();
		$(".gambar").attr("src", "https://user.gadjian.com/static/images/personnel_boy.png");
	});





});



//***********************************************************************
// Match Two Strings
//***********************************************************************
//

function success_msg(msg){
	htm = '<div class="alert alert-success">';
	htm += '<i class="fa fa-check"></i> <strong>Success!</strong> '+msg+'!';
	htm += '</div>';

	return htm;
}

function error_msg(msg){
	htm = '<div class="alert alert-warning">';
	htm += '<i class="fa fa-exclamation-triangle"></i> <strong>Error!</strong> '+msg+'!';
	htm += '</div>';

	return htm;
}




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

	$(".state-div").hide();
	$(".city-div").hide();
	$(".city-div-spinner").hide();

	$(".state-div-spinner").show();


	e.stopImmediatePropagation();

	kk = $(this).val();

	if(kk.length>0){
		$.post("/get_states_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){

			$(".state-div-spinner").hide();
			$(".state-div").show();
			$("select.states_select").empty().append(data);
			$("select.states_select").selectpicker('refresh');
		});
	}else{
		$(".state-div-spinner").hide();
		$(".city-div-spinner").hide();
		$("select.states_select").val('');
		$("select.states_select").selectpicker('refresh');
		$("select.city_select").val('');
		$("select.city_select").selectpicker('refresh');
	}
});


$(".country_select_single").on('hidden.bs.select', function (e){

	$(".state-div").hide();
	$(".city-div").hide();
	$(".city-div-spinner").hide();

	$(".state-div-spinner").show();


	e.stopImmediatePropagation();

	kk = $(this).val();

	if(kk!=""){
		$.post("/get_states_dropdown_single/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){

			$(".state-div-spinner").hide();
			$(".state-div").show();
			$("select.states_select_single").empty().append(data);
			$("select.states_select_single").selectpicker('refresh');
		});
	}else{
		$(".state-div-spinner").hide();
		$(".city-div-spinner").hide();
		$("select.states_select_single").val('');
		$("select.states_select_single").selectpicker('refresh');
		$("select.city_select_single").val('');
		$("select.city_select_single").selectpicker('refresh');
	}
});


//***********************************************************************
// Get Cities Dropdown
//***********************************************************************
//


$(".states_select").on('hidden.bs.select', function (e){

	$(".city-div-spinner").show();

	e.stopImmediatePropagation();

	kk = $(this).val();


	if(kk.length>0){

		$.post("/get_cities_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			$(".city-div-spinner").hide();
			$(".city-div").show();
			$("select.city_select").empty().append(data);
			$("select.city_select").selectpicker('refresh');

		});
	}else{

		$(".city-div").hide();
		$("select.city_select").val('');
		$("select.city_select").selectpicker('refresh');
		$(".city-div-spinner").hide();
	}
});

$(".states_select_single").on('hidden.bs.select', function (e){

	$(".city-div-spinner").show();

	e.stopImmediatePropagation();

	kk = $(this).val();


	if(kk!=""){

		$.post("/get_cities_dropdown_single/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			$(".city-div-spinner").hide();
			$(".city-div").show();
			$("select.city_select_single").empty().append(data);
			$("select.city_select_single").selectpicker('refresh');

		});
	}else{

		$(".city-div").hide();
		$("select.city_select_single").val('');
		$("select.city_select_single").selectpicker('refresh');
		$(".city-div-spinner").hide();
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

	$(".processing-div-spinner").show();

	formdata = $(elem).serialize();

	inp = $(inp_name).val();


	if($.trim(inp)!=""){

		f_data = formdata + "&inp="+inp;

		$.post("/save_partner_preferences/", f_data, function(data){
			$(".processing-div-spinner").hide();
			$(".message_div").append(success_msg('Data Saved'));
		});
	}else{
		$(".message_div").empty().append(error_msg('Filter Name is required'));
		$(inp_name).focus();
	}
}

//***********************************************************************
// Change Password
//***********************************************************************
//

function change_password(){
	form_d = $("#change_password_form").serialize();

	$("#change_password_modal").modal('hide');

	$.post("/change_password/",form_d, function(data){
		alert(data);
	});
}




//***********************************************************************
// Profile validation
//***********************************************************************
//


$("#id_phone_number").on("focusout", function(){

	Phone_number = $(this).val();
	console.log(Phone_number)
	var phoneno = /^\d{10}$/;
	if(Phone_number.match(phoneno))
	{
		console.log('hhh')
	}
	else
	{
		   alert("Not a valid Phone Number");
		// $("#passwd1_error").text("Not a valid Phone Number");

	}


});

$("#id_phone_number_alternative").on("focusout", function(){

	Phone_number = $(this).val();
	console.log(Phone_number)
	var phoneno = /^\d{10}$/;
	if(Phone_number.match(phoneno))
	{
		console.log('hhh')
	}
	else
	{
		   alert("Not a valid Phone Number");
		// $("#passwd1_error").text("Not a valid Phone Number");

	}


});


$(function() {
    $('#id_fullname').keydown(function(e) {
      if (e.shiftKey || e.ctrlKey || e.altKey) {
        e.preventDefault();
      } else {
        var key = e.keyCode;
        if (!((key == 8) || (key == 32) || (key == 46) || (key >= 35 && key <= 40) || (key >= 65 && key <= 90))) {
          e.preventDefault();
        }
      }
    });
  });

  $(function() {
    $('#id_father_name').keydown(function(e) {
      if (e.shiftKey || e.ctrlKey || e.altKey) {
        e.preventDefault();
      } else {
        var key = e.keyCode;
        if (!((key == 8) || (key == 32) || (key == 46) || (key >= 35 && key <= 40) || (key >= 65 && key <= 90))) {
          e.preventDefault();
        }
      }
    });
  });

  $(function() {
    $('#id_mother_name').keydown(function(e) {
      if (e.shiftKey || e.ctrlKey || e.altKey) {
        e.preventDefault();
      } else {
        var key = e.keyCode;
        if (!((key == 8) || (key == 32) || (key == 46) || (key >= 35 && key <= 40) || (key >= 65 && key <= 90))) {
          e.preventDefault();
        }
      }
    });
  });

  $("#id_height").keypress(function(event) {
		return /\d/.test(String.fromCharCode(event.keyCode));
  });
  $("#id_weight").keypress(function(event) {
		return /\d/.test(String.fromCharCode(event.keyCode));
  });


	//*******************************************************************************
	// Message Counters
	//*******************************************************************************

	$("textarea#word_count").on('keyup', function() {

		var mlen = $(this).val().length;

		if(mlen <= 250){
			$("#display_count").empty().text(250 - mlen);
		}else{
			alert("Maximum reached");
		}
	});


	//*******************************************************************************
	// Connect/Message Modal
	//*******************************************************************************

	function open_connect_modal(to_id){
		$("#connect_modal_form").modal('show');
		$("#to_user_id").val(to_id);
	}


	function connect_modal_form_cancel(){
		$("#display_count").empty().text(250);
		$("#connect_modal_form").modal('hide');
	}

	function on_connect_save(){

		if($.trim($("textarea#word_count").val()).length == 0){
			alert('Cannot')
		}else{
			formdata = $("#connect_save_form").serialize();

			$.post("/connect_msg_save/", formdata, function(data){
				alert("Message successfully sent");
				$("#connect_modal_form").modal('hide');
			});
		}
	}


	//*******************************************************************************
	// Multi Select Checkbox
	//*******************************************************************************

	$("#select_all").change(function(){  //"select all" change
	    $(".checkbox").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
	});

	//".checkbox" change
	$('.checkbox').change(function(){
		//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#select_all").prop('checked', false); //change "select all" checked status to false
    }
		//check "select all" if all checkbox items are checked
		if ($('.checkbox:checked').length == $('.checkbox').length ){
			$("#select_all").prop('checked', true);
		}
	});
