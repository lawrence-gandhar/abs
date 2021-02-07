$(document).ready(function(){

	//*****************************************************
	// preference filters
	//*****************************************************

	pref_age_to = document.getElementById('id_for_pref_aged_to');
	pref_age_from = document.getElementById('id_for_pref_aged_from');

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


  //*****************************************************
  // height filters
  //*****************************************************

  pref_height_to = document.getElementById('id_for_pref_height_to');
  pref_height_from = document.getElementById('id_for_pref_height_from');

  var height_inputs = [pref_height_to, pref_height_from];

	if(pref_height_to.value == '') pref_height_to_val = 180;
	else pref_height_to_val = pref_height_to.value;

	if(pref_height_from.value == '') pref_height_from_val = 150;
	else pref_height_from_val = pref_height_from.value;

	var height_Slider  = document.getElementById('pref_height_slider');

	noUiSlider.create(height_Slider , {
		start: [pref_height_from_val, pref_height_to_val],
		connect: true,
		step: 1,
		range: {
			'min': 130,
			'max': 250
		},
		tooltips: [true, wNumb({decimals: false,})],
		format : wNumb({decimals: false,}),
	});

	height_Slider.noUiSlider.on('update', function (values, handle) {
		height_inputs[handle].value = values[handle];
	});


  //
  //
  //

  if($("#id_for_pref_l_countries").val()!=""){
    kk = $("#id_for_pref_l_countries").val();
    $.post("/get_states_dropdown/", {'csrfmiddlewaretoken': csrf, 'ids':kk}, function(data){
      $("select#id_for_pref_l_states").empty().append(data);
			$("select#id_for_pref_l_states").selectpicker('refresh');
    });
  }


});
