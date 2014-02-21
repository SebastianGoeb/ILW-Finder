var districts = {};//district name -> District()
var map;

hues = {}

$.get('get/nn-hues/of-datazones', function(data) {
    hues_in = $.parseJSON(data);
    for (var dz in hues_in) {
	hues["S0"+dz.toString()] = rgbStrFromArray(hslToRgb(hues_in[dz],
							   0.5, 0.5))
    }

    intro()
});



function intro() {
    var width = 960, height = 1160;
    
    var projection = d3.geo.albers()
	.center([0.795, 55.89])
	.rotate([4.4, 0])
	.parallels([50, 60])
	.scale(180000)
	.translate([width / 20, height / 3]);

    var path = d3.geo.path()
	.projection(projection);

    var svg = d3.select("body").append("svg")
	.attr("width", width)
	.attr("height", height);


    d3.json("static/edin_topo.json", function(error, data) {
	svg.selectAll(".geometries")
	    .data(topojson.feature(data, data.objects.S12000036_geo).features)
	    .enter().append("path")
	    .attr("style", function(d) {
		offer = hues[d.properties.gss]
		if (offer == '#bf3f3f') {
		    return "fill:#505050"
		} else {
		    return "fill:"+offer
		}
	    })
	    .attr("d", path);
	// svg.append("path")
	//     .datum(topojson.mesh(data, data.objects['S12000036_geo'],
	// 			function(a,b){return a == b}))
	//     .attr("id", "council_area")
	//     .attr("d", path);
    });
}

// function District() {
//     this.name;
//     this.colour = "#FF0000";
//     this.pc_coords = [];
//     this.mean_coord = [0.0,0.0];
//     this.polygon;
// }

// $.get( "get/district/of-postcodes", function (data) {
//     var districts_in = $.parseJSON(data);
// 	var n_districts = 0
    
//     //construct district_name -> District() map
//     for (var pc in districts_in) {
//         var district_name = districts_in[pc];

//         if (!(district_name in districts)) {
//         	var d = new District();
//             d.name = district_name;
//             districts[district_name] = d;
//             n_districts++;
//         }
//     }

//     //assign colors to districts along HSL cylinder
//     var district_k = 0;
//     for (var district_name in districts) {
//     	var d = districts[district_name];
//     	var rgb = hslToRgb(district_k / n_districts, 1.0, 0.5);//TODO higher stride mod 1.0 ???
//     	d.colour = "rgba(" + Math.floor(rgb[0]) + ", " + Math.floor(rgb[1]) + ", " + Math.floor(rgb[2]) + ", 1)";
//         district_k++;
//     }
    
//     console.log("Found " + n_districts + " districts");

//     $.get("get/georef/of-postcodes", function (data) {
//         var coords = $.parseJSON(data);
//         var n_postcodes = 0;

// 		//populate districts with pc_coordinates
//         for (var pc in coords) {
//         	var district_name = districts_in[pc];
//         	if(!district_name || !(district_name in districts)) continue;

//         	var d = districts[district_name];
//         	d.pc_coords.push([coords[pc][0], coords[pc][1]]);//1 = lng, 0 = lat
//         	if(district_name == "Myreside") {
//         		console.log(district_name + ": " + coords[pc]);
//         		console.log(district_name + ": " + d.pc_coords[0]);
//         	}
//         	n_postcodes++;
//         }

//        	console.log("Myreside" + ": " + districts["Myreside"].pc_coords[0]);
//        	console.log(district_name + ": " + districts["Myreside"].mean_coord[0]);
        
//         //calculate mean district position
//         for (var district_name in districts) {
//         	var d = districts[district_name];
//         	d.mean_coord_x = 0
//         	d.mean_coord_y = 0
//         	for (var pc_coord in d.pc_coords) {
//         		d.mean_coord[0] += pc_coord[0];
//         		d.mean_coord[1] += pc_coord[1];
//         	}
//         	d.mean_coord[0] /= d.pc_coords.length;
//         	d.mean_coord[1] /= d.pc_coords.length;
//        		console.log(district_name + ": " + districts["Myreside"].pc_coords[0]);
//        		console.log(district_name + ": " + districts["Myreside"].mean_coord[0]);
//         }

//         console.log("Found " + n_postcodes + " postcodes");

//     });
// });

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

function rgbStrFromArray(arr) {
    return ('#'
	    + parseInt(arr[0]).toString(16)
	    + parseInt(arr[1]).toString(16)
	    + parseInt(arr[2]).toString(16))
}

// function getDatazones() {
//     $.getJSON('static/edin_topo.json', function(data) {
// 	var geoStyle = {
// 	    strokeColor: '#505050',
// 	    strokeOpacity: 0.4,
// 	    fillColor: '#ff0000',
// 	    fillOpacity: 0.1,
// 	};

// 	// var dz_topojson = new topojson.object(data,
// 	// 				  data.objects.S12000036_geo);

// 	var dz_topojson = topojson.mesh(data, data.objects.S12000036_geo)

// 	var dz_geojson = new GeoJSON(dz_topojson, geoStyle);

// 	addGeometries = function(overlays) {
// 	    $.each(overlays, function(i, overlay) {
// 		if (!overlay.length) {
// 		    newOverlay = new google.maps.Polygon({
// 			latLngs: overlay.latLngs,
// 			strokeColor: '#505050',
// 			strokeOpacity: 0.4,
// 			fillColor: '#ff0000',
// 			fillOpacity: 0.1,
// 		    });

// 		    newOverlay.setMap(map);
// 		} else {
// 		    addGeometries(overlay);
// 		}
// 	    });
// 	}

// 	addGeometries(dz_geojson)

// //	addGeometries(dz_geojson);
// //	dz_geojson.setMap(map)
//     });
// }

// google.maps.event.addDomListener(window, 'load', initmap);

// function initmap() {
// 	var mapOptions = {
// 		center: new google.maps.LatLng(55.94, -3.2),
// 		zoom: 12,
// 		mapTypeId: google.maps.MapTypeId.ROADMAP
// 	};

// 	map = new google.maps.Map(document.getElementById("map-canvas"),
// 				  mapOptions);

//     //initialize district polygons
//     // for (var district_name in districts) {
//     // 	var d = districts[district_name];
//     // 	d.polygon = new google.maps.Polygon({
//     // 		paths: [],
//     // 		strokeColor: "#000000",
//     // 		strokeOpacity: 1,
//     // 		fillColor: d.colour,
//     // 		fillOpacity: 0.5
//     // 	});
//     // 	d.polygon.setMap(map);
//     // }

//     getDatazones()
// 	//google.maps.event.addListener(map,'projection_changed', updatePolygons);
// }

//calculate Voronoi polygons per district
// function updatePolygons(){
// 	var mapNE = map.getBounds().getNorthEast();
// 	var mapSW = map.getBounds().getSouthWest();
//     for (var district_name in districts) {
//     	var d = districts[district_name];
//     	var poly_x = [mapSW.lng(), mapNE.lng(), mapNE.lng(), mapSW.lng()];
//     	var poly_y = [mapSW.lat(), mapSW.lat(), mapNE.lat(), mapNE.lat()];
//     	var districs_x = [];
//     	var districs_y = [];
//     	var this_district_x;
//     	var this_district_y;
//     	for (var other_district_name in districts) {
//     		if (other_district_name == district_name) {
//     			this_district_x = districts[other_district_name].mean_coord[0];
//     			this_district_y = districts[other_district_name].mean_coord[1];
//     		} else {
//     			districs_x.push(districts[other_district_name].mean_coord[0]);
//     			districs_y.push(districts[other_district_name].mean_coord[1]);
//     		}
//     	}
//     	calculateVoronoi(poly_x, poly_y, districs_x, districs_y, this_district_x, this_district_y);

//     	var poly_coords = [];
//     	for (var poly_coord_i = 0; poly_coord_i < poly_x.length; poly_coord_i++) {
//     		poly_coords.push(new google.maps.LatLng(poly_y[poly_coord_i], poly_x[poly_coord_i]));
//     	}
//     	d.polygon.setPath(poly_coords);
//     }

//     console.log("map bounds:");
//     console.log("mapNE:" + mapNE);
//     console.log("mapSW:" + mapSW);

//     /*for (var district_name in districts) {
//     	var d = districts[district_name];
//     	console.log(district_name + ": " + d.mean_coord);
//     	for (var poly_coord in districts[district_name].polygon.getPath().getArray()) {
//     		console.log("\t" + poly_coord);
//     	}
//     }*/
// }

/* v = (starting) vertices of polygon
 * n = nodes (postcodes/neighbourhoods)
 * a = center node (around which the Voronoi polygon will be constructed)
 */
// function calculateVoronoi(vx, vy, nx, ny, ax, ay) {
//   for (var i = 0; i < nx.length; i++) {//loop over nodes
//     //tested point
//     var bx = nx[i];
//     var by = ny[i];
//     //midway point
//     var cx = (bx + ax) / 2;
//     var cy = (by + ay) / 2;
//     //second point on perpendicular bisector
//     var dx = (ay - cy) + cx;
//     var dy = (cx - ax) + cy;

//     var discarded = [];
//     var j = 0;
//     while (j < vx.length) {//insert intersections and flag deletions
//       var ex = vx[j];
//       var ey = vy[j];
//       var fx = vx[(j+1) % vx.length];
//       var fy = vy[(j+1) % vx.length];
//       var inE = ((dx - cx)*(ey - cy) - (ex - cx)*(dy - cy)) >= 0;
//       var inF = ((dx - cx)*(fy - cy) - (fx - cx)*(dy - cy)) >= 0;

//       if (inE && inF) {//E in, F in
//         j++;
//       } else if (inE && !inF) {//E in, F out
//         gx = ((cx*dy - cy*dx)*(ex - fx) - (cx - dx)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
//         gy = ((cx*dy - cy*dx)*(ey - fy) - (cy - dy)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
//         vx.splice(j+1, 0, gx);
//         vy.splice(j+1, 0, gy);
//         j += 2;
//       } else if (!inE && inF) {//E out, F in
//         gx = ((cx*dy - cy*dx)*(ex - fx) - (cx - dx)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
//         gy = ((cx*dy - cy*dx)*(ey - fy) - (cy - dy)*(ex*fy - ey*fx)) / ((cx - dx)*(ey - fy) - (cy - dy)*(ex - fx));
//         vx.splice(j+1, 0, gx);
//         vy.splice(j+1, 0, gy);
//         discarded.push(j);
//         j += 2;
//       } else {//E out, F out
//         discarded.push(j);
//         j++;
//       }
//     }

//     while (discarded.length != 0) {//discard flagged vertices
//       j = discarded.pop();
//       vx.splice(j, 1);
//       vy.splice(j, 1);
//     }
//   }
// }
