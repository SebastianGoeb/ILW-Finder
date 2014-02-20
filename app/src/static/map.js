var postcode_locations;
var postcode_neighbourhoods;
var neighbourhoods = {};

/* A postcode is a house. Every postcode will have an associated district
   (the "natural neighbourhood"). */
var nodes = [];
var districts = {};
var districts_in;
var heatmaps = {};

var map;

/*function Node() {
    this.postcode = undefined;
    this.georef = undefined;
    this.district = undefined;

    function getTwoClosestInDistrict() {
        out = [undefined, undefined];
        outRng = [undefined, undefined];
    };
}*/

function District() {
    this.name;
    this.colour;
    this.polygon;
}

$.get( "get/district/of-postcodes", function (data) {
    districts_in = $.parseJSON(data);
	n_districts = 0
    
    //construct district_name -> District() map
    for (var pc in districts_in) {
        district_name = districts_in[pc];

        var d;

        if (!(district_name in districts)) {
            d = new District();
            d.name = district_name;
            /*d.heatmap = new google.maps.visualization.HeatmapLayer({
				data: new google.maps.MVCArray(),
				opacity: 0.9
			});*/
            districts[district_name] = d;
            n_districts++;
        }
    }

    //assign colors to heatmaps along HSL cylinder
    district_k = 0;
    for (var disctrict_name in districts) {
    	d = districts[district_name];
    	rgb = hslToRgb(district_k / n_districts, 1.0, 0.5);
    	gradient = [
    		'rgba(255, 255, 255, 0)',
    		'rgba('+Math.floor(rgb[0])+', '+Math.floor(rgb[1])+', '+Math.floor(rgb[2])+', 1)'
    	]
 		//d.heatmap.set('gradient', gradient);
        district_k++;
    }
    
    console.log("Found "+n_districts+" districts");

	//populate heatmaps with coordinates
    $.get("get/georef/of-postcodes", function (data) {
        coords = $.parseJSON(data);
        n_nodes = 0;
        for (var pc in coords) {
        	district_name = districts_in[pc];
        	if(district_name){
        		d = districts[district_name];
        		//d.heatmap.getData().push(new google.maps.LatLng(coords[pc][1], coords[pc][0]));
        		n_nodes++;
        	}
        }
        
        console.log("Found "+n_nodes+" postcodes");

        initmap();
    });
});

/* Converts an HSL color to an RGB color
 * h ∈ [0°, 360°], s ∈ [0, 1], v ∈ [0, 1]
 *
 * output will be [r, g, b] where
 * r ∈ [0, 255], g ∈ [0, 255], b ∈ [0, 255]
 */
function hslToRgb(h, s, l){
    var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
        function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return [r * 255, g * 255, b * 255];
}

function initmap() {
	var mapOptions = {
		center: new google.maps.LatLng(55.94, -3.2),
		zoom: 12
	};

	map = new google.maps.Map(document.getElementById("map-canvas"),
		mapOptions);

	var heatmap_n = 0;
    for (var disctrict_name in districts) {

    	if(heatmap_n < 3){
    		d = districts[district_name];
 			//d.heatmap.setMap(map);
 		}
 		heatmap_n++;
	}
}