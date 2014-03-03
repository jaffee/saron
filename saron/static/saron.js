

var get_data = function (url) {
    $.get(url, null, render_hosts);
    setTimeout(function () {
	get_data(url);
    }, 1000);
};


var render_data = function(host, data) {
    for (var subj in data) {
	if (data.hasOwnProperty(subj)){
	    for (var metric in data[subj]) {
		if (data[subj].hasOwnProperty(metric)){
		    console.log(data[subj][metric]);
		    var this_id = host + subj + metric.replace("%", "pct").replace("/", "per");
		    var chartdiv = $("#" + this_id);
		    if ( chartdiv.length != 0 ) {
			console.log(chartdiv.length);
			console.log("reusing");
			chartdiv.sparkline(data[subj][metric]);
		    }
		    else {
			console.log("appending");
			$( "#superchartdiv" ).append("<div class='charttitle'>" + this_id + "</div>");
			$( "#superchartdiv" ).append("<div id='" + this_id + "' class='chartdiv'> </div>");
			$( ".chartdiv:last-child" ).sparkline(data[subj][metric]);
		    }
		}
	    }
	}
    }
};


var render_hosts = function(rawhostdata) {
    var hostdata = JSON.parse(rawhostdata);
    for (var host in hostdata) {
	if (hostdata.hasOwnProperty(host)){
	    render_data(host, hostdata[host]);
	}
    }
};
