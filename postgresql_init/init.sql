DROP DATABASE postgres;

CREATE SCHEMA linguistics;

CREATE TABLE linguistics.dim_words (
	word_id varchar(50) PRIMARY KEY,
	word_english varchar(100),
	is_stopword boolean,
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp
	
);

CREATE TABLE linguistics.dim_sources (
	source_id varchar(50) PRIMARY KEY,
	source_name varchar(100),
	source_path varchar(200),
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp
);

CREATE TABLE linguistics.fact_word_counts (
	count_id varchar(50) PRIMARY KEY,
	source_id varchar(50),
	word_id varchar(50),
	count int,
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp
);

CREATE SCHEMA datamart;

DROP MATERIALIZED VIEW datamart.unique_words_in_source;

CREATE MATERIALIZED VIEW datamart.unique_words_in_source AS 
	SELECT
		source_id,
		source_name,
		COUNT(word_id) AS unique_word_count
	FROM (
		SELECT
			t1.source_id,
			t2.source_name,
			t1.word_id
		FROM
			linguistics.fact_word_counts AS t1
		LEFT JOIN
			linguistics.dim_sources AS t2
		ON
			t1.source_id=t2.source_id
	) AS t3
	GROUP BY
		source_id, source_name		
	;

CREATE FUNCTION refresh_unique_words_in_source()
RETURNS TRIGGER LANGUAGE plpgsql
AS $$
begin
    refresh materialized view datamart.unique_words_in_source;
    return null;
end $$;

CREATE TRIGGER refresh_unique_words_in_source_trigger
AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE 
ON linguistics.fact_word_counts FOR EACH STATEMENT 
EXECUTE PROCEDURE refresh_unique_words_in_source();

CREATE USER airflow;

GRANT ALL PRIVILEGES ON SCHEMA linguistics TO airflow;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA linguistics TO airflow;

CREATE USER read_only;

GRANT USAGE ON SCHEMA linguistics TO read_only;

GRANT USAGE ON SCHEMA datamart TO read_only;

GRANT SELECT ON ALL TABLES IN SCHEMA linguistics TO read_only;

GRANT SELECT ON ALL TABLES IN SCHEMA datamart TO read_only;




