var districts = {};//district name -> District()
var map;
var infoWindow;
var voronoi_visible = false;

function District() {
    this.name;
    this.colour = "#FF0000";
    this.pc_coords = [];
    this.mean_coord = [0, 0];
    this.polygon;
}

$.get( "get/district/of-postcodes", function (data) {
    var districts_in = $.parseJSON(data);
	var n_districts = 0
    
    //construct district_name -> District() map
    for (var pc in districts_in) {
        var district_name = districts_in[pc];

        if (!(district_name in districts)) {
        	var d = new District();
            d.name = district_name;
            districts[district_name] = d;
            n_districts++;
        }
    }

    //assign colors to districts along HSL cylinder
    var district_k = 0;
    for (var district_name in districts) {
    	var d = districts[district_name];
    	var rgb = hslToRgb(district_k / n_districts, 1.0, 0.5);//TODO higher stride mod 1.0 ???
    	d.colour = "rgba(" + Math.floor(rgb[0]) + ", " + Math.floor(rgb[1]) + ", " + Math.floor(rgb[2]) + ", 1)";
        district_k++;
    }
    
    console.log("Found " + n_districts + " districts");

    $.get("get/georef/of-postcodes", function (data) {
        var coords = $.parseJSON(data);
        var n_postcodes = 0;

		//populate districts with pc_coordinates
        for (var pc in coords) {
        	var district_name = districts_in[pc];
        	if(!district_name || !(district_name in districts)) continue;

        	var d = districts[district_name];
        	d.pc_coords.push([coords[pc][0], coords[pc][1]]);//1 = lng, 0 = lat
        	n_postcodes++;
        }
        
        //calculate mean district position
        for (var district_name in districts) {
        	var d = districts[district_name];
        	for (var i = 0; i < d.pc_coords.length; i++) {
        		var pc_coord = d.pc_coords[i];
        		d.mean_coord[0] += pc_coord[0];
        		d.mean_coord[1] += pc_coord[1];
        	}
        	d.mean_coord[0] /= d.pc_coords.length;
        	d.mean_coord[1] /= d.pc_coords.length;
        }

        console.log("Found " + n_postcodes + " postcodes");

        initmap();
    });
});

/* Converts an HSL color to an RGB color
 * h ∈ [0, 1], s ∈ [0, 1], v ∈ [0, 1]
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
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
	infoWindow = new google.maps.InfoWindow();


    //initialize district polygons
    for (var district_name in districts) {
    	var d = districts[district_name];
    	d.polygon = new google.maps.Polygon({
    		paths: [],
    		strokeColor: "#000000",
    		strokeOpacity: 0.5,
    		strokeWeight: 1,
    		fillColor: d.colour,
    		fillOpacity: 0.05,
            visible: voronoi_visible,
    		district: district_name
    	});
    	d.polygon.setMap(map);
  		google.maps.event.addListener(d.polygon, 'click', showDistrict);
    }
	google.maps.event.addListener(map,'bounds_changed', updatePolygons);
}

//calculate Voronoi polygons per district
function updatePolygons(){
	var mapNE = map.getBounds().getNorthEast();
	var mapSW = map.getBounds().getSouthWest();
    for (var district_name in districts) {
    	var d = districts[district_name];
    	var poly_x = [mapSW.lng(), mapNE.lng(), mapNE.lng(), mapSW.lng()];
    	var poly_y = [mapSW.lat(), mapSW.lat(), mapNE.lat(), mapNE.lat()];
    	var districs_x = [];
    	var districs_y = [];
    	var this_district_x;
    	var this_district_y;
    	for (var other_district_name in districts) {
    		if (other_district_name == district_name) {
    			this_district_x = districts[other_district_name].mean_coord[0];
    			this_district_y = districts[other_district_name].mean_coord[1];
    		} else {
    			districs_x.push(districts[other_district_name].mean_coord[0]);
    			districs_y.push(districts[other_district_name].mean_coord[1]);
    		}
    	}
    	calculateVoronoi(poly_x, poly_y, districs_x, districs_y, this_district_x, this_district_y);

    	var poly_coords = [];
    	for (var poly_coord_i = 0; poly_coord_i < poly_x.length; poly_coord_i++) {
    		poly_coords.push(new google.maps.LatLng(poly_y[poly_coord_i], poly_x[poly_coord_i]));
    	}
    	d.polygon.setPath(poly_coords);
    }
}

/* v = (starting) vertices of polygon
 * n = nodes (postcodes/neighbourhoods)
 * a = center node (around which the Voronoi polygon will be constructed)
 */
function calculateVoronoi(vx, vy, nx, ny, ax, ay) {
  for (var i = 0; i < nx.length; i++) {//loop over nodes
    //tested point
    var bx = nx[i];
    var by = ny[i];
    //midway point
    var cx = (bx + ax) / 2;
    var cy = (by + ay) / 2;
    //second point on perpendicular bisector
    var dx = (ay - cy) + cx;
    var dy = (cx - ax) + cy;

    var discarded = [];
    var j = 0;
    while (j < vx.length) {//insert intersections and flag deletions
      var ex = vx[j];
      var ey = vy[j];
      var fx = vx[(j+1) % vx.length];
      var fy = vy[(j+1) % vx.length];
      var inE = ((dx - cx)*(ey - cy) - (ex - cx)*(dy - cy)) >= 0;
      var inF = ((dx - cx)*(fy - cy) - (fx - cx)*(dy - cy)) >= 0;

      if (inE && inF) {//E in, F in
        j++;
      } else if (inE && !inF) {//E in, F out
        gx = ((cx*dy - cy*dx)*(ex - fx) - (cx - dx)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
        gy = ((cx*dy - cy*dx)*(ey - fy) - (cy - dy)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
        vx.splice(j+1, 0, gx);
        vy.splice(j+1, 0, gy);
        j += 2;
      } else if (!inE && inF) {//E out, F in
        gx = ((cx*dy - cy*dx)*(ex - fx) - (cx - dx)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
        gy = ((cx*dy - cy*dx)*(ey - fy) - (cy - dy)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
        vx.splice(j+1, 0, gx);
        vy.splice(j+1, 0, gy);
        discarded.push(j);
        j += 2;
      } else {//E out, F out
        discarded.push(j);
        j++;
      }
    }

    while (discarded.length != 0) {//discard flagged vertices
      j = discarded.pop();
      vx.splice(j, 1);
      vy.splice(j, 1);
    }
  }
}

function showDistrict(event) {
	var d = districts[this.district];
	infoWindow.setContent(d.name + "<br/>lat: " + d.mean_coord[1] + "<br/>lng: " + d.mean_coord[0]);
	infoWindow.setPosition(new google.maps.LatLng(d.mean_coord[1], d.mean_coord[0]));
	infoWindow.open(map);
}

function toggleVoronoi(){
    voronoi_visible = !voronoi_visible;
    for (var district_name in districts) {
        var d = districts[district_name];
        d.polygon.setVisible(voronoi_visible);
    }
}

function toggleDatazones(){
    alert("Datazones not yet implemented!");
}