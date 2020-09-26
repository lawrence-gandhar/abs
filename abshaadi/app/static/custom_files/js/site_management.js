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