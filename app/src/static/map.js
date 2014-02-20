var postcode_locations;
var postcode_neighbourhoods;
var neighbourhoods = {};
var current_colour = 0x0;



$.get( "get/district/of-postcodes", function (data) {
					postcode_neighbourhoods = $.parseJSON(data);
					parse_neighbourhoods();
					$.get( "get/georef/of-postcodes", function (data) {
					  					postcode_locations = $.parseJSON(data);
					  					initmap();
					});
});

function parse_neighbourhoods () {
	for (var key in postcode_neighbourhoods) {
		var neighbourhood = postcode_neighbourhoods[key];
		if ($.inArray(neighbourhood, neighbourhoods) == -1) {
			neighbourhoods[neighbourhood] = get_colour();
		};
	};
};

function get_colour () {
	current_colour = current_colour + 0x70;
	return "#" + current_colour;
};

//initmap();

function initmap() {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © OpenStreetMap contributors';
	var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});

	map.setView([55.94, -3.2], 13);
	map.addLayer(osm);

	for (var key in postcode_locations) {

		var neighbourhood = postcode_neighbourhoods[key];
		var circle = L.circle(postcode_locations[key].reverse(), 5, {
			opacity: 1,
			color: neighbourhoods[neighbourhood],
			fillOpacity: 1
		}).addTo(map);
		circle.bindPopup(neighbourhood);
	};
};

