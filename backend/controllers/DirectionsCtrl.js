var request = require('request');

console.log('Directions Controller Loaded')

var GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json?mode=walking"

getDirections = function (req, res) {
	if (!req.body.origin) return res.send(400, {error: 'Missing Body: Origin'});
	if (!req.body.destination) return res.send(400, {error: 'Missing Body: Destination'});
	
	// use test locations in philly
	var test_origin = "3643-3661 Walnut St, Philadelphia, PA 19104, USA"
	var test_destination = "3451 Ludlow St, Philadelphia, PA 19104, USA"
	var directionsURL = GOOGLE_DIRECTIONS_URL;
	directionsURL += "&origin=" + test_origin;
	directionsURL += "&destination=" + test_destination;

	request(directionsURL, function (error, response, body) {
		if (!error && response.statusCode == 200) {
			console.log(body);
			return res.send(200, JSON.parse(body));
		}
		return res.send(400, error);
	});
}

module.exports = {
	getDirections: getDirections
}