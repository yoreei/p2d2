CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION pymax (a integer, b integer)
  RETURNS integer
AS $$
  if a > b:
    return a
  return b
$$ LANGUAGE plpython3u;

DROP FUNCTION plmax(bytea);
DROP FUNCTION allmax(bytea);

CREATE OR REPLACE FUNCTION plmax(tbl bytea)
    RETURNS text
AS $$
   return 'MAX(c_customerkey)'
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION allmax(tbl bytea)
    RETURNS bytea
AS $$
    rv = plpy.execute("SELECT * FROM customer")
$$ LANGUAGE plpython3u;


/*SELECT column_name FROM information_schema.columns WHERE table_name='customer' AND column_name!='c_custkey' */
