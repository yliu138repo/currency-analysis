set search_path to public;

create table IF NOT EXISTS currencyRecord (
	id serial PRIMARY KEY,
	rate float NOT NULL,
	time TIMESTAMP	NOT NULL
);


select rate, time 
from currencyRecord cr
order by time DESC;

SELECT *
FROM currencyRecord cr
WHERE  date_trunc('month', cr.time) <= date_trunc('month', current_timestamp) AND
date_trunc('month', cr.time) > date_trunc('month', current_timestamp - interval '1 month')
order by cr.time DESC;

SELECT *
FROM currencyRecord cr
WHERE  date_trunc('day', cr.time) <= date_trunc('day', current_timestamp) AND
date_trunc('day', cr.time) > date_trunc('day', current_timestamp - interval '3 days')
order by cr.time DESC;