set search_path to public

create table IF NOT EXISTS currencyRecord (
	id serial PRIMARY KEY,
	rate float NOT NULL,
	time TIMESTAMP	NOT NULL
);


select rate, time 
from currencyRecord cr
order by time DESC