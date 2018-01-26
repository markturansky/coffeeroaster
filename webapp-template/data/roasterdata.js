$(document).ready(function() {
    var roastID = $.url().param("id");

    $(".roaster-element").change(function(){
        var name = $(this).attr("id")
        var value = $(this).val()
        var url = "/rest/set?" + name + "=" + value
        $.getJSON(url, function(data){})
    });

    $("#btn-cool").click(function(){
        var url = "/rest/set"
        $.getJSON(url, {heater:0, drawfan:10,scrollfan:10}, function(data){});
        $("#heater").val(0)
        $("#scrollfan").val(10)
        $("#drawfan").val(10)
    });

    $("#btn-onoff").click(function(){
        var url = "/rest/set"
        $.getJSON(url, {isRunning:0}, function(data){});
        $("#heater").val(0)
        $("#scrollfan").val(0)
        $("#drawfan").val(0)
    });

    var offset = 0;
    plot();

    var yticks = [];
    for(var i = 0; i < 1000; i++){
        if(i % 50 == 0){
            yticks.push(i)
        } else {
            yticks.push()
        }
    }

    var xticks = [];
    for(var i = 0; i < 3600; i++){
        if(i % 60 == 0){
            xticks.push(i)
        } else {
            xticks.push()
        }
    }

    function plot() {
        var heater = [];
        var beans = [];

        $.getJSON("/rest/data?id="+roastID, function(data){
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
                //    ticks: xticks,
                //},
                yaxis: {
                    min: 0,
                    max: 1000,
                    ticks: yticks,
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
