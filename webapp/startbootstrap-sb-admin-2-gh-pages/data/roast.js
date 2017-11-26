//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var heater = [];
        for (var i = 0; i < 1200; i++) {
            if (i % 2 == 0){
                heater.push([i, i]);
            }
        }

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
            yaxis: {
                min: 0,
                max: 1750,
            },
            tooltip: true,
            tooltipOpts: {
                content: "'%s' of %x.1 is %y.4",
                shifts: {
                    x: -60,
                    y: 25
                }
            }
        };

        var plotObj = $.plot($("#roast-line-chart"), [{
                data: heater,
                label: "heater (F)"
            }],
            options);
    }
});
