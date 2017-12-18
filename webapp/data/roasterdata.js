//Flot Line Chart
$(document).ready(function() {

    var offset = 0;
    plot();

    function plot() {
        var heater = [];
        var beans = [];

        $.getJSON("rest/data", function(data){
            heater = data[0]
            beans = data[1]

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

            var plotObj = $.plot($("#roast-line-chart"), [
                {
                    data: heater,
                    label: "heater (F)"
                },
                {
                    data: beans,
                    label: "beans (F)"
                }
            ], options);
        });

        window.setTimeout(plot, 1000)
    }
});
