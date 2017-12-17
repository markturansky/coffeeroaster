//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var heater = [[0, 0], [1, 0], [2, 0], [3, 1657], [4, 0], [5, 1772], [6, 1758], [7, 0], [8, 1815], [9, 0], [10, 0], [11, 0], [12, 1772]];
        var beans = [[0, 0], [1, 1848], [2, 0], [3, 1642], [4, 0], [5, 1642], [6, 1750], [7, 0], [8, 829], [9, 964], [10, 2308], [11, 0], [12, 1642]];

        var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: true
                }
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            //xaxis: {
            //    mode: "time",
            //},
            yaxis: {
                min: 0,
                max: 900,
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' %y",
                shifts: {
                    x: -60,
                    y: 25
                }
            },
	    legend: {
		position: "nw"
		},
        };

        var plotObj = $.plot($("#roast-line-chart"), [{
                data: heater,
                label: "heater (F)"
            },
                {
                    data: beans,
                    label: "beans (F)"
                }],
            options);
    }
});
