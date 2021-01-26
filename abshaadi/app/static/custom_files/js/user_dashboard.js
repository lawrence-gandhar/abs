$(document).ready(function(){

    //
	//***********************************************************************************
    // Doughnut Chart
    //***********************************************************************************

    var ctx = document.getElementById('myChart').getContext('2d');

    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
			datasets: [{
				data: [90,10],
				backgroundColor: ['rgb(51, 204, 51)', 'rgb(255, 255, 255)'],
			}],
			labels: [
				'Activity Average per month',
				'',
			],

		},
		options: {
				legend:{
					display : false,
				},
				responsive: true,
				animation: {
					animateScale: true,
					animateRotate: true
				},
				borderWidth : 0,
			}
    });

});
