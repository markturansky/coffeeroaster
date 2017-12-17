//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var heater = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 1685], [10, 1772], [11, 0], [12, 1772], [13, 0], [14, 1757], [15, 1815], [16, 1815], [17, 1815]];
        var beans = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 422], [9, 1411], [10, 1642], [11, 0], [12, 1642], [13, 0], [14, 1635], [15, 829], [16, 829], [17, 829]];

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
