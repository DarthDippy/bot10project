-- View: decode.positive_mood_events

-- DROP VIEW decode.positive_mood_events;

CREATE OR REPLACE VIEW decode.positive_mood_events AS 
 SELECT events_with_keyword_counts.event_id,
    events_with_keyword_counts.source,
    events_with_keyword_counts.event_name,
    events_with_keyword_counts.event_description,
    events_with_keyword_counts.event_url,
    events_with_keyword_counts.event_free,
    events_with_keyword_counts.event_cost,
    events_with_keyword_counts.event_cost_currency,
    events_with_keyword_counts.yes_rsvp_count,
    events_with_keyword_counts.maybe_rsvp_count,
    events_with_keyword_counts.capacity,
    events_with_keyword_counts.waitlist,
    events_with_keyword_counts.venue_name,
    events_with_keyword_counts.venue_address,
    events_with_keyword_counts.venue_zip,
    events_with_keyword_counts.venue_city,
    events_with_keyword_counts.venue_state,
    events_with_keyword_counts.venue_lat,
    events_with_keyword_counts.venue_lon,
    events_with_keyword_counts.group_name,
    events_with_keyword_counts.created,
    events_with_keyword_counts.updated,
    events_with_keyword_counts.start_time,
    events_with_keyword_counts.end_time,
    events_with_keyword_counts.negative_keyword_count,
    events_with_keyword_counts.positive_keyword_count
   FROM decode.events_with_keyword_counts
  WHERE events_with_keyword_counts.start_time >= now() AND events_with_keyword_counts.start_time <= (now() + '1 day'::interval)
  ORDER BY events_with_keyword_counts.positive_keyword_count DESC
 LIMIT 10;

ALTER TABLE decode.positive_mood_events
  OWNER TO group10;
