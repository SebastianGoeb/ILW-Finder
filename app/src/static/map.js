var postcode_locations;
var postcode_neighbourhoods;
var neighbourhoods = {};
var current_colour = 0x0;

/* A postcode is a house. Every postcode will have an associated district
   (the "natural neighbourhood"). */
var nodes = {};
var districts = {};

var map;

$.get( "get/district/of-postcodes", function (data) {
    districts_in = $.parseJSON(data);
    n_districts = 0
    
    for (var pc in districts_in) {
        district_name = districts_in[pc];

        if (!(district_name in districts)) {
            districts[district_name] = {
                colour: next_district_colour()
            };

            n_districts++;
        }
                  
        nodes[pc] = {district:district_name};
    }
    
    console.log("Found "+n_districts+" districts");

    $.get("get/georef/of-postcodes", function (data) {
        coords = $.parseJSON(data);
        n_nodes = 0
        for (var pc in coords) {
            nodes[pc].georef =
                new google.maps.LatLng(coords[pc][1], coords[pc][0]);
            nodes[pc].marker =
                new google.maps.Marker({
                    position: nodes[pc].georef
                });
            n_nodes++
        }
        
        console.log("Found "+n_nodes+" postcodes");

        initmap();
    });
});


function next_district_colour () {
    current_colour = current_colour + 0x90;
    return "#" + current_colour;
};

function initmap() {
    var mapOptions = {
        center: new google.maps.LatLng(55.94, -3.2),
        zoom: 12
    };
    
    map = new google.maps.Map(document.getElementById("map-canvas"),
		                          mapOptions);
    for (var pc in nodes) {
        nodes[pc].marker.setMap(map);
    }
}
