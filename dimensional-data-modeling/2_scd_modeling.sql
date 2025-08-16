-- Slow Changing Dimensions (SCD) Modeling Example

-- 1. Populate actors table
insert into actors
with last_year as (
	select * from actors
	where current_year = 1974
	),
current_year AS (
    SELECT
        actorid,
        actor,
        year,
        array_agg(
            row(film, votes, rating, filmid)::film_struct
        ) AS films,
        avg(rating) as year_rating
    FROM actor_films
    WHERE year = 1975
    GROUP BY actorid, actor, year
)
select
coalesce(cy.actorid, ly.actorid) as actorid,
coalesce(cy.actor, ly.actor) as actor,
CASE 
    WHEN ly.films IS NULL THEN 
        cy.films
    WHEN cy.films IS NULL THEN 
        ly.films
    ELSE 
        ly.films || cy.films
END AS films,
case
	when cy.year is not null then(
	case
	when coalesce(cy.year_rating) > 8 then 'star'
	when coalesce(cy.year_rating) > 7 then 'good'
	when coalesce(cy.year_rating) > 6 then 'average'
else 'bad' end)::quality_class
else ly.quality_class end as quality_class,
cy.year is not null as is_active,
1975 as current_year
from last_year as ly
full outer join current_year as cy
	on cy.actorid = ly.actorid
;

-- 2. Backfill query to populate actors_history_scd
insert into actors_history_scd
with streak_started as (
	select actor,
	current_year,
	quality_class,
	is_active,
	lag(quality_class, 1) over (partition by actor order by current_year) <> quality_class
	or lag(quality_class, 1) over(partition by actor order by current_year) is null
	as did_change,
	lag(is_active, 1) over (partition by actor order by current_year) <> is_active
	or lag(is_active, 1) over(partition by actor order by current_year) is null
	as did_change_activity
	from actors
)
,streak_identified as (
	select
		actor,
		current_year,
		quality_class,
		is_active,
		sum(case when did_change then 1 else 0 end) over (partition by actor order by current_year) as streak_identifier
		,sum(case when did_change_activity then 1 else 0 end) over (partition by actor order by current_year) as streak_identifier_activity
	from streak_started
)
,aggregated as (
	select 
		actor,
		quality_class,
		is_active,
		streak_identifier,
		streak_identifier_activity,
		min(current_year) as start_date,
		max(current_year) as end_date
	from streak_identified
	group by 1,2,3,4,5
)
select 
actor,
quality_class,
is_active,
start_date,
end_date
from aggregated