$(document).ready(function() {
    var items = [];
    $.getJSON("/rest/roasts", function(data){
        console.log(data)
        for (var d in data){
            var href = "/webapp/pages/flot.html?id=" + data[d]
            $("#roast-list").find("ul").append("<li><a href='" + href + "'>" + data[d] + "</a></li>");
        }
    });
});
