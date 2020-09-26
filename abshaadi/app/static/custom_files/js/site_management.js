$(document).ready(function(){

});


//
//
//

function start_religion_auto_renew(){
	
	var r = confirm("This operation will remove previous enteries and re-insert all the religions and castes from initial file. Do you want to continue");
	if (r == true) {
		$("#data_process_modal").modal('show');
	
		$.get("/load_religions_into_db/", function(data){
			if(data == 1){
				location.reload();
			}
		});
	} 	
}


//
//
//

function validate_add_religion_form(elem){
	
	$.post("/add_religion/", $(elem).serialize(), function(data){
		
		if(data == 1){}
		else{
			$(elem).find(".modal-body >  .error-div").empty().append(data);
		}		
	});
	
	
	return false;
}