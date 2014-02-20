var postcode_locations;
var postcode_neighbourhoods;
var neighbourhoods = {};

/* A postcode is a house. Every postcode will have an associated district
   (the "natural neighbourhood"). */
var nodes = {};
var districts = {};

var map;

function Node() {
    this.postcode = undefined;
    this.georef = undefined;
    this.district = undefined;

    function getTwoClosestInDistrict() {
        out = [undefined, undefined];
        outRng = [undefined, undefined];
    };
}

current_colour = 0x101010;

function District() {
    this.nodes = [];
    this.name = undefined;

    function _nextColour() {
        current_colour = current_colour + 0xB0;
        return "#" + current_colour.toString(16);
    };

    this.colour = _nextColour();
}

$.get( "get/district/of-postcodes", function (data) {
    districts_in = $.parseJSON(data);
    n_districts = 0
    
    for (var pc in districts_in) {
        district_name = districts_in[pc];

        var d;

        if (!(district_name in districts)) {
            d = new District();
            d.name = district_name;
            districts[district_name] = d;

            n_districts++;
        } else {
            d = districts[district_name];
        }

        n = new Node();
        n.district = d;
        n.postcode = pc;
        d.nodes.push(n);

        nodes[pc] = n;
    }
    
    console.log("Found "+n_districts+" districts");

    $.get("get/georef/of-postcodes", function (data) {
        coords = $.parseJSON(data);
        n_nodes = 0
        for (var pc in coords) {
            nodes[pc].georef =
                new google.maps.LatLng(coords[pc][1], coords[pc][0]);
            n_nodes++
        }
        
        console.log("Found "+n_nodes+" postcodes");

        initmap();
    });
});

function initmap() {
    var mapOptions = {
        center: new google.maps.LatLng(55.94, -3.2),
        zoom: 12
    };
    
    map = new google.maps.Map(document.getElementById("map-canvas"),
		                          mapOptions);
    for (var pc in nodes) {
        nodes[pc].circ =
            new google.maps.Circle({
                strokeOpacity: 0.0,
                fillColor: nodes[pc].district.colour,
                fillOpacity: 0.5,
                map: map,
                center: nodes[pc].georef,
                radius: 40
            });
    }
}
