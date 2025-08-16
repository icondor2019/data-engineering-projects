A cumulative query to generate `device_activity_datelist` from `events` --
insert into user_devices_cumulated
with deduped_devices as (
select
	*,
	row_number() over (partition by d.device_id, browser_type ) as row_num
from devices as d
)
, events_devices as ( 
select
	e.*,
	dd.*
from events e 
inner join deduped_devices as dd
on e.device_id = dd.device_id
where e.user_id is not null
and dd.browser_type is not null
and dd.row_num = 1
)
, yesterday as (
select 
	* 
from user_devices_cumulated
where date = date('2023-01-30')
)
, today as (
select
	cast(user_id as text) as user_id,
	browser_type, 
	date(cast(event_time as timestamp)) as today_date,
	count(1) as num_events
	from events_devices
	where DATE(CAST(event_time as TIMESTAMP)) = DATE('2023-01-31')
    GROUP BY 1,2,3
)
select
	COALESCE(t.user_id, y.user_id) as user_id,
	COALESCE(t.browser_type, y.browser_type) as browser_type,
	case 
		when y.device_activity_datelist is null then array[t.today_date]
		when t.today_date is null then y.device_activity_datelist
		else array[t.today_date] || y.device_activity_datelist
		end as device_activity_datelist
	,
	COALESCE(t.today_date, y.date + interval '1 day') as date
from today t
full outer join yesterday y
on t.user_id = y.user_id
and t.browser_type = y.browser_type;


-- A `datelist_int` generation query. Convert the `device_activity_datelist` column into a `datelist_int` column 
with users as (
select * from user_devices_cumulated
where date = DATE('2023-01-31')
)
,series as (
	select 
		* 
	from generate_series(date('2023-01-01'), date('2023-01-31'), interval '1 day') 
	as generated_date
)
, place_holder_ints as (
select 
	case 
		when device_activity_datelist @> array [date(generated_date)] 
		then cast(pow(2,32 - (date - date(generated_date))) as bigint)
		else 0 
	end as placeholder_int_value 
		,* 
from users
cross join series
)
select 
	user_id,
	browser_type,
	device_activity_datelist,
	cast(cast(sum(placeholder_int_value) as bigint) as bit(32)) as datelist_in
from place_holder_ints
where user_id = '9446887345398050000'
group by user_id, 2,3
;
