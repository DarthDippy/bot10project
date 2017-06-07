-- View: decode.events_with_keyword_counts

-- DROP VIEW decode.events_with_keyword_counts;

CREATE OR REPLACE VIEW decode.events_with_keyword_counts AS 
 SELECT events.event_id,
    events.source,
    events.event_name,
    events.event_description,
    events.event_url,
    events.event_free,
    events.event_cost,
    events.event_cost_currency,
    events.yes_rsvp_count,
    events.maybe_rsvp_count,
    events.capacity,
    events.waitlist,
    events.venue_name,
    events.venue_address,
    events.venue_zip,
    events.venue_city,
    events.venue_state,
    events.venue_lat,
    events.venue_lon,
    events.group_name,
    events.created,
    events.updated,
    events.start_time,
    events.end_time,
    decode.count_instances(events.event_description, 'comfort food'::text) + decode.count_instances(events.event_name, 'comfort food'::text) + decode.count_instances(events.event_description, 'social support'::text) + decode.count_instances(events.event_name, 'social support'::text) + decode.count_instances(events.event_description, 'flowers'::text) + decode.count_instances(events.event_name, 'flowers'::text) + decode.count_instances(events.event_description, 'socialize'::text) + decode.count_instances(events.event_name, 'socialize'::text) + decode.count_instances(events.event_description, 'music'::text) + decode.count_instances(events.event_name, 'music'::text) + decode.count_instances(events.event_description, 'gym'::text) + decode.count_instances(events.event_name, 'gym'::text) + decode.count_instances(events.event_description, 'shopping'::text) + decode.count_instances(events.event_name, 'shopping'::text) + decode.count_instances(events.event_description, 'sports'::text) + decode.count_instances(events.event_name, 'sports'::text) + decode.count_instances(events.event_description, 'dance'::text) + decode.count_instances(events.event_name, 'dance'::text) + decode.count_instances(events.event_description, 'games'::text) + decode.count_instances(events.event_name, 'games'::text) + decode.count_instances(events.event_description, 'comedy'::text) + decode.count_instances(events.event_name, 'comedy'::text) + decode.count_instances(events.event_description, 'karaoke'::text) + decode.count_instances(events.event_name, 'karaoke'::text) AS negative_keyword_count,
    decode.count_instances(events.event_description, 'finance'::text) + decode.count_instances(events.event_name, 'finance'::text) + decode.count_instances(events.event_description, 'career development'::text) + decode.count_instances(events.event_name, 'career development'::text) + decode.count_instances(events.event_description, 'training'::text) + decode.count_instances(events.event_name, 'training'::text) + decode.count_instances(events.event_description, 'networking'::text) + decode.count_instances(events.event_name, 'networking'::text) + decode.count_instances(events.event_description, 'volunteer'::text) + decode.count_instances(events.event_name, 'volunteer'::text) + decode.count_instances(events.event_description, 'community'::text) + decode.count_instances(events.event_name, 'community'::text) + decode.count_instances(events.event_description, 'business'::text) + decode.count_instances(events.event_name, 'business'::text) + decode.count_instances(events.event_description, 'parenting'::text) + decode.count_instances(events.event_name, 'parenting'::text) + decode.count_instances(events.event_description, 'service'::text) + decode.count_instances(events.event_name, 'service'::text) + decode.count_instances(events.event_description, 'learn'::text) + decode.count_instances(events.event_name, 'learn'::text) AS positive_keyword_count
   FROM decode.events;

ALTER TABLE decode.events_with_keyword_counts
  OWNER TO group10;
