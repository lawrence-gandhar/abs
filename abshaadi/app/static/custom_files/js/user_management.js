$(document).ready(function(){

});

//*******************************************************************************
// DELETE USER
//*******************************************************************************

function delete_user(id){
	$("#data_process_modal").modal('show');

	$.get('/staff/user_management/users/delete/'+id+'/', function(data){
		if(data == 1){
			location.reload();
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


//*******************************************************************************
// ADD STAFF
//*******************************************************************************

function add_staff(){
	$("#data_process_modal").modal('show');

	$.post("/staff/user_management/staff/add/", $("#add_staff_form").serialize(), function(){
		if(data==1){
			location.reload();
		}
		else if(data==0){
			$("#data_process_modal").modal('hide');
			alert("In Valid Operation");
		}
		else{
			$("#data_process_modal").modal('hide');
			$("#error_modal").find(".modal-body").empty().append(data);
			$("#error_modal").modal('show');
		}
	});
}

//*******************************************************************************
// USER EDIT MODAL
//*******************************************************************************

function user_edit_modal_form(id){

	$("#user_id").val(id);

	$("#user_edit_modal_form").modal('show');

	$.post("{% url 'fetch_user_details' %}", {"user_id":id, "csrfmiddlewaretoken":csrfmiddlewaretoken}, function(data){

		data = $.parseJSON(data);

		$("#id_phone_number").val(data.phone_number);
		$("#id_fullname").val(data.fullname);
		$("#id_phone_number_alternative").val(data.phone_number_alternative);
		$("#id_package").val(data.package);
		$("#id_assigned_to").val(data.assigned_to);

		console.log(data);
	});
}


//*******************************************************************************
// DELETE SELECTED USERS
//*******************************************************************************

function delete_selected_users(){
	rr = confirm("Do you want to delete the selected users? All data will be lost for the selected users after this operation");
}
