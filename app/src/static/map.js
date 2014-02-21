var postcode_locations;
var postcode_neighbourhoods;
var neighbourhoods = {};

/* A postcode is a house. Every postcode will have an associated district
   (the "natural neighbourhood"). */
var nodes = {};
var districts = {};

var map;

function Node(d) {
    this.postcode = undefined;
    this.georef = undefined;
    this.district = d;
    this.district_inner_range = [];

    this.infoWindow = new google.maps.InfoWindow({
        content: d.name,
    });
    
    this.calc_district_inner_range = function() {
        if (this.district_inner_range.length != 0) {
            return this.district_inner_range;
        }

        var out = [];

        for (var n in this.district.nodes) {
            node = this.district.nodes[n]
            
            if (node == this) {
                continue;
            }

            out.push(
                [node,
                 google.maps.geometry.spherical.computeDistanceBetween(
                     node.georef, this.georef)]);
        }

        // sort in ascending range order
        this.district_inner_range = out.sort(
            function(a,b) {
                return a[1] - b[1];
            }
        );

        return this.district_inner_range;
    }

    this.closest_in_district = function(num) {
        lst = this.calc_district_inner_range();

        num = Math.min(num, lst.length);

        return lst.slice(0,num-1)
    };


    this.drawCircle = function() {
        var circ = new google.maps.Circle({
            strokeOpacity: 0.0,
            fillColor: this.district.colour,
            fillOpacity: 0.5,
            map: map,
            center: this.georef,
            radius: 100
        });

        google.maps.event.addListener(circ, 'click', function() {
            console.log(this);
            console.log(this.infoWindow);
            this.infoWindow.open(map, this.georef);
        });
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

    this.drawInnerPolygons = function() {
        if (this.nodes.length < 3) {
            return;
        }

        for (var n in this.nodes) {
            vertices = this.nodes[n].closest_in_district(3).map(function(n_) {
                return n_[0].georef;
            });

            vertices.push(this.nodes[n].georef)

            new google.maps.Polygon({
                paths: vertices,
                strokeOpacity: 0,
                fillColor: this.colour,
                fillOpacity: 0.5,
                map: map
            });
        }
    };
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

        n = new Node(d);
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

    // for (var d in districts) {
    //     districts[d].drawInnerPolygons();
    // }

    for (var n in nodes) {
        nodes[n].drawCircle();
    }
}
