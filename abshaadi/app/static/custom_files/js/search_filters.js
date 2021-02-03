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

	//*****************************************************
	// preference filters
	//*****************************************************

	pref_age_to = document.getElementById('id_for_pref_aged_from');
	pref_age_from = document.getElementById('id_for_pref_aged_to');

	var pref_inputs = [pref_age_to, pref_age_from];

	if(pref_age_to.value == '') pref_age_to_val = 25;
	else pref_age_to_val = pref_age_to.value;

	if(pref_age_from.value == '') pref_age_from_val = 18;
	else pref_age_from_val = pref_age_from.value;

	var pref_stepsSlider  = document.getElementById('pref_age_slider');

	noUiSlider.create(pref_stepsSlider , {
		start: [pref_age_from_val, pref_age_to_val],
		connect: true,
		step: 1,
		range: {
			'min': 18,
			'max': 70
		},
		tooltips: [true, wNumb({decimals: false,})],
		format : wNumb({decimals: false,}),
	});

	pref_stepsSlider.noUiSlider.on('update', function (values, handle) {
		pref_inputs[handle].value = values[handle];
	});

});


function profile_like(to_user){
	$.get("/profile_like/"+to_user+"/", function(data){});
}


//*******************************************************************************
// FETCH CASTE CREED
//*******************************************************************************

function fetch_caste_creed(elem){

	kk = $(elem).val();

	$.post("/get_castes_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
			$("#id_caste_creed").html(data);
	});
}
