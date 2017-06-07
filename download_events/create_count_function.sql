-- Function: decode.count_instances(text, text)

-- DROP FUNCTION decode.count_instances(text, text);

CREATE OR REPLACE FUNCTION decode.count_instances(
    text,
    text)
  RETURNS integer AS
$BODY$
SELECT CASE WHEN ((CHAR_LENGTH($1) - CHAR_LENGTH(regexp_replace($1, $2, '', 'i'))) / CHAR_LENGTH($2)) is not null
THEN ((CHAR_LENGTH($1) - CHAR_LENGTH(regexp_replace($1, $2, '', 'i'))) / CHAR_LENGTH($2))
ELSE 0
END
$BODY$
  LANGUAGE sql IMMUTABLE
  COST 100;
ALTER FUNCTION decode.count_instances(text, text)
  OWNER TO group10;
