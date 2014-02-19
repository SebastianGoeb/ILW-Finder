var points = [new point(55.943, -3.2), new point(55.933, -3.22)]



initmap();
function initmap() {
	// set up the map
	map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © OpenStreetMap contributors';
	var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});

	map.setView([55.94, -3.2], 13);
	map.addLayer(osm);

	for (var i = points.length - 1; i >= 0; i--) {
		var marker = L.marker(points[i].getCoordinates()).addTo(map);
	};
};

function point (latitude,longitude) {
	this.latitude  = latitude;
	this.longitude = longitude;

	this.getCoordinates = getCoordinates;

	function getCoordinates() {
		return [this.latitude, this.longitude];
	};
};

