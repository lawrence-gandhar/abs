$(document).ready(function(){
	
	$(".states_select").hide();
	
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

$(".country_select").on('hidden.bs.select', function (){
	
	kk = $(this).val();
	
	console.log(kk)
	
	$(".state-div").hide();
	
	if(kk.length>0){
		$.get("/get_states_dropdown/", {'ids':kk}, function(data){
			$(".states_select").empty().append(data);
			$(".states_select").selectpicker();
			
			$(".state-div").show();
		});
	}
		
});


//***********************************************************************
// Get Cities Dropdown
//***********************************************************************
//


$(".states_select").on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue){
	id = $(this).val();
	
	if(id !=""){
		$.get("/get_cities_dropdown/", function(data){
			console.log(data);
		});
	}
});




	
	