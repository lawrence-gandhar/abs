$(document).ready(function(){

});


function delete_user(id){
	$("#data_process_modal").modal('show');
	
	$.get('/staff/user_management/users/delete/'+id+'/', function(data){
		if(data == 1){
			localtion.reload();
		}else{
			$("#data_process_modal").modal('hide');	
			if(data == 0){
				alert("Invalid operation");
			}
			if(data == 2){
				alert("User not Found, Contact Administrator");
			}
		}
	});
}