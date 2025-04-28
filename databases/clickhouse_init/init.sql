CREATE TABLE warehouse.dim_words (
	word_id varchar(50),
	word_english varchar(100),
	is_stopword boolean,
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp,
 	PRIMARY KEY(word_id)
	
);

CREATE TABLE warehouse.dim_sources (
	source_id varchar(50) ,
	source_title varchar(100),
	source_path varchar(200),
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp,
 	PRIMARY KEY(source_id)
);

CREATE TABLE warehouse.fact_word_counts (
	count_id varchar(50) ,
	source_id varchar(50),
	word_id varchar(50),
	count int,
	created_at timestamp,
	updated_at timestamp,
	deleted_at timestamp,
 	PRIMARY KEY(source_id)
)
ENGINE = ReplacingMergeTree(created_at)
ORDER BY(source_id, word_id);

CREATE DATABASE datamart;

CREATE TABLE datamart.individual_word_counts (
	count_id varchar(50),
	source_path varchar(200),
	source_title varchar(100),
	word_english varchar(100),
	is_stopword boolean,
	count int,
	PRIMARY KEY(source_path)
)
ENGINE = ReplacingMergeTree()
ORDER BY(source_path, word_english);

CREATE MATERIALIZED VIEW individual_word_counts_mv TO datamart.individual_word_counts AS
SELECT count_id, source_path, source_title, word_english, is_stopword, count FROM warehouse.fact_word_counts A
LEFT JOIN warehouse.dim_sources B
ON A.source_id = B.source_id
LEFT JOIN warehouse.dim_words C
ON A.word_id = C.word_id
ORDER BY(source_path, source_title, count);   

CREATE TABLE datamart.count_unique_non_stopwords (
	source_path varchar(200),
	source_title varchar(100),
	unique_word_count int,
	PRIMARY KEY(source_path)
)
ENGINE = ReplacingMergeTree()
ORDER BY(source_path);

CREATE MATERIALIZED VIEW count_unique_non_stopwords_mv TO datamart.count_unique_non_stopwords AS
SELECT source_path, source_title, count(word_english) AS unique_word_count FROM (

	SELECT source_path, source_title, word_english
	FROM datamart.individual_word_counts
	WHERE NOT is_stopword 
)
 GROUP BY(source_path, source_title);