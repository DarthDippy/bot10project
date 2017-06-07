var promise = require('bluebird');

var options = {
  // Initialization Options
  promiseLib: promise
};

var pgp = require('pg-promise')(options);
var connectionString = 'postgres://group10@postgresql-group10:connectTHEawesomeness10@postgresql-group10.postgres.database.azure.com:5432/postgres?ssl=true';
var db = pgp(connectionString);

// add query functions

module.exports = {
  getPositiveMoodEvent: getPositiveMoodEvent,
  getNegativeMoodEvent: getNegativeMoodEvent,
  getPositiveMoodEvents: getPositiveMoodEvents,
  getNegativeMoodEvents: getNegativeMoodEvents,
};

function getPositiveMoodEvent(req, res, next) {
  db.one("select * from decode.events_with_keyword_counts where start_time between now() and now() + '1 day'::interval order by positive_keyword_count desc limit 1")
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved most relevant positive mood event occurring in the next day'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function getNegativeMoodEvent(req, res, next) {
  db.one("select * from decode.events_with_keyword_counts where start_time between now() and now() + '1 day'::interval order by negative_keyword_count desc limit 1")
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved most relevant negative mood event occurring in the next day'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function getPositiveMoodEvents(req, res, next) {
  hours = parseInt(req.query.hours)
  count = parseInt(req.query.count)
  db.any("select * from decode.events_with_keyword_counts where start_time between now() and now() + '$1 hours'::interval order by positive_keyword_count desc limit $2", [hours, count])
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved most relevant positive mood event(s) occurring soon'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}

function getNegativeMoodEvents(req, res, next) {
  hours = parseInt(req.query.hours)
  count = parseInt(req.query.count)
  db.any("select * from decode.events_with_keyword_counts where start_time between now() and now() + '$1 hours'::interval order by negative_keyword_count desc limit $2", [hours, count])
    .then(function (data) {
      res.status(200)
        .json({
          status: 'success',
          data: data,
          message: 'Retrieved most relevant negative mood event(s) occurring soon'
        });
    })
    .catch(function (err) {
      return next(err);
    });
}