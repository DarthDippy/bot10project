-- Table: decode.events

-- DROP TABLE decode.events;

CREATE TABLE decode.events
(
  event_id text,
  source text,
  event_name text,
  event_description text,
  event_url text,
  event_free boolean,
  event_cost numeric,
  event_cost_currency text,
  yes_rsvp_count integer,
  maybe_rsvp_count integer,
  capacity integer,
  waitlist integer,
  venue_name text,
  venue_address text,
  venue_zip integer,
  venue_city text,
  venue_state text,
  venue_lat numeric,
  venue_lon numeric,
  group_name text,
  created timestamp with time zone,
  updated timestamp with time zone,
  start_time timestamp with time zone,
  end_time timestamp with time zone
)
WITH (
  OIDS=FALSE
);
ALTER TABLE decode.events
  OWNER TO group10;
