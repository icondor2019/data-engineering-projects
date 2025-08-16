-- incremental query for actors_history_scd

CREATE TYPE actor_scd_type AS (
                    quality_class quality_class,
                    is_active boolean,
                    start_date INTEGER,
                    end_date INTEGER
                    );

with last_year_scd as (
	select * from actors_history_scd
	where start_date = 1975
	and end_date = 1975
)
, historical_scd as (
	select
		actor,
		quality_class,
		is_active,
		start_date,
		end_date
	from actors_history_scd
	where start_date < 1975
	and end_date < 1975
)
, this_year_data as (
	select * from actors 
	where current_year = 1976
)
, unchanged_records as (
	select 
		ty.actor,
		ty.quality_class,
		ty.is_active,
		ly.start_date,
		ty.current_year as end_date
	from this_year_data as ty
	join last_year_scd as ly
		on ly.actor = ty.actor
	where ty.quality_class = ly.quality_class
	and ty.is_active = ly.is_active
)
, changed_records as (
	select
	ty.actor,
	unnest(array[row(ly.quality_class, ly.is_active, ly.start_date, ly.end_date)::actor_scd_type,
				row(ty.quality_class, ty.is_active, ty.current_year, ty.current_year)::actor_scd_type
				]) as records
	from this_year_data as ty
	left join last_year_scd as ly
		on ly.actor = ty.actor
	where (ty.quality_class <> ly.quality_class or  ty.is_active <> ly.is_active)
)
, unnested_changed_records as (
	select
		actor,
		(records::actor_scd_type).quality_class,
		(records::actor_scd_type).is_active,
		(records::actor_scd_type).start_date,
		(records::actor_scd_type).end_date
		from changed_records
)
, new_records as (
select 
	ty.actor,
	ty.quality_class,
	ty.is_active,
	ty.current_year as start_date,
	ty.current_year as end_date
	from this_year_data ty
	left join last_year_scd ly
	on ty.actor = ly.actor
	where ly.actor is null
)
select 
*, 
1976 as current_year
from (
	select * from historical_scd
	union all
	select * from unchanged_records
	union all
	select * from unnested_changed_records
	union all
	select * from new_records
) as alias
;