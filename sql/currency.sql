create table IF NOT EXISTS currencyRecord (
	id serial PRIMARY KEY,
	rate float NOT NULL,
	time TIMESTAMP	NOT NULL
);