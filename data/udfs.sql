CREATE OR REPLACE function _final_random(anyarray)           
 RETURNS anyelement AS
$BODY$
 SELECT $1[array_lower($1,1) + floor((1 + array_upper($1, 1) - array_lower($1, 1))*random())];
$BODY$
LANGUAGE 'sql' IMMUTABLE;

CREATE AGGREGATE random(anyelement) (
  SFUNC=array_append, --Function to call for each row. Just builds the array
  STYPE=anyarray,
  FINALFUNC=_final_random, --Function to call after everything has been added to array
  INITCOND='{}' --Initialize an empty array when starting
);

CREATE OR REPLACE FUNCTION _final_median(numeric[])
   RETURNS numeric AS
$$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$$
LANGUAGE 'sql' IMMUTABLE;

CREATE AGGREGATE median(numeric) (
  SFUNC=array_append,
  STYPE=numeric[],
  FINALFUNC=_final_median,
  INITCOND='{}'
);

-- SELECT * FROM my_table TABLESAMPLE SYSTEM_ROWS(100);
CREATE EXTENSION tsm_system_rows;
