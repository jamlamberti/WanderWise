var DirectionCtrl = require('./DirectionsCtrl.js');

module.exports = function (app) {
  console.log('Routes Loaded');

  app.post('/directions', DirectionCtrl.getDirections);

  //Catchall Route
  app.use(function (req, res) {
  	// res.send(200, {status: 'Catchall Route'});
  	res.sendfile('./public/views/index.html')
  });
}