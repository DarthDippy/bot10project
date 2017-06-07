var express = require('express');
var router = express.Router();

var db = require('../queries');

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/api/positiveMoodEvent', db.getPositiveMoodEvent);
router.get('/api/negativeMoodEvent', db.getNegativeMoodEvent);
router.get('/api/positiveMoodEvents', db.getPositiveMoodEvents);
router.get('/api/negativeMoodEvents', db.getNegativeMoodEvents);

module.exports = router;
