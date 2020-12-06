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
});


function profile_like(to_user){
	$.get("/profile_like/"+to_user+"/", function(data){});
}
