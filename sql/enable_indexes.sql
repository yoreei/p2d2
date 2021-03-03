--taken from https://dba.stackexchange.com/a/276949

CREATE OR REPLACE PROCEDURE enable_indexes(
    IN schema_name TEXT
,   IN table_name TEXT
,   IN index_name TEXT
,   IN enable_use BOOLEAN
,   IN enable_updates BOOLEAN
,   IN skip_essentials BOOLEAN DEFAULT TRUE
)
LANGUAGE plpgsql
AS $$
DECLARE
    each_record RECORD;
BEGIN

IF array_replace(ARRAY[schema_name, table_name, index_name], NULL, '') <@ ARRAY[''] THEN
    RAISE EXCEPTION 'Must specify at least one of schema_name | table_name | index_name';
END IF;


FOR each_record IN
    UPDATE pg_index
    SET
        indisvalid = enable_use
    ,   indisready = enable_updates
    FROM pg_indexes
    WHERE
        indexrelid = (schemaname||'.'||indexname)::regclass
    AND case when schema_name <> '' THEN schemaname = schema_name ELSE TRUE END
    AND case when table_name <> '' THEN tablename = table_name ELSE TRUE END
    AND case when index_name <> '' THEN indexname = index_name ELSE TRUE END
    AND case when skip_essentials THEN indisprimary = FALSE ELSE TRUE END
    AND case when skip_essentials THEN indisunique = FALSE ELSE TRUE END
    RETURNING (schemaname||'.'||indexname) as index_name, indisvalid, indisready
LOOP

    RAISE INFO 'Set index % to have use % and updates %.'
        ,   each_record.index_name
        ,   (case when each_record.indisvalid THEN 'enabled' else 'disabled' END)
        ,   (case when each_record.indisready THEN 'enabled' else 'disabled' END)
    ;
END LOOP;

END
$$;

CREATE OR REPLACE PROCEDURE set_indexes(IN state BOOLEAN)
AS $$
DECLARE
rec record;
tbl_name varchar(50);
BEGIN
FOR rec IN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public') LOOP
tbl_name=rec.table_name;
CALL enable_indexes('public',tbl_name,'',state,true);

END LOOP;
END;
$$ LANGUAGE plpgsql;

