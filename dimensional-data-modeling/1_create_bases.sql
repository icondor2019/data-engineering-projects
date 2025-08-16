-- Client types for dimensional data modeling example
create type film_struct as (
film TEXT,
votes INTEGER,
rating real,
filmid TEXT
);

create type quality_class as 
ENUM('bad', 'average', 'good', 'star');

-- Table to hold actors data year by year
create table actors (
actorid TEXT,
actor TEXT,
films film_struct[],
quality_class quality_class,
is_active BOOLEAN,
current_year INTEGER,
primary KEY(actorid, current_year));

create table actors_history_scd
(
	actor TEXT,
	quality_class quality_class,
	is_active BOOLEAN,
	start_date INTEGER,
	end_date INTEGER,
	primary key(actor, start_date) 
)