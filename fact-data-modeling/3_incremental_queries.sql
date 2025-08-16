-- The incremental query to generate `host_activity_datelist`
insert into hosts_cumulated
with yesterday as (
select 
	* 
from hosts_cumulated
where date = DATE('2023-01-01')
)
, today as (
	select
	cast(host as TEXT) as host,
	DATE(CAST(event_time as TIMESTAMP)) as today_date,
	count(1) as num_events
	from events
	where DATE(CAST(event_time as TIMESTAMP)) = DATE('2023-01-01')
    AND user_id IS NOT NULL
    GROUP BY 1,2
)
select
	COALESCE(t.host, y.host) as user_id,
	case 
		when y.host_activity_datelist is null then array[t.today_date]
		when t.today_date is null then y.host_activity_datelist
		else array[t.today_date] || y.host_activity_datelist
		end as host_activity_datelist
	,
	COALESCE(t.today_date, y.date + interval '1 day') as date -- se intenta que este campo tenga la fecha del dia, 
from today t
full outer join yesterday y
on t.host = y.host;


-- An incremental query that loads `host_activity_reduced`
insert into host_activity_reduced
with daily_aggregate as (
	select
		host,
		date(event_time) as date,
		count(1) as num_site_hits,
		count(distinct user_id) as unique_visitors
	from events
	where date(event_time) = date('2023-01-02')
	and user_id is not null
	group by host, 2
)
, yesterday_array as (
	select 
		*
	from host_activity_reduced
	where month_start = date('2023-01-01')
)
select
	coalesce(da.host, ya.host) as host,
	coalesce(ya.month_start, date_trunc('month', da.date)) as monthly_start,
	case
		when ya.hit_array is not null 
			then ya.hit_array || array[coalesce(da.num_site_hits,0)]
		when ya.hit_array is null
			then array_fill(0, array[coalesce(date - date(date_trunc('month', date)), 0)]) || 
			array[coalesce(da.num_site_hits, 0)]
		end as hit_array,
	case
		when ya.unique_visitors_array is not null 
			then ya.unique_visitors_array || array[coalesce(da.unique_visitors,0)]
		when ya.unique_visitors_array is null
			then array_fill(0, array[coalesce(date - date(date_trunc('month', date)), 0)]) || 
			array[coalesce(da.unique_visitors, 0)]
		end as unique_visitors_array
from daily_aggregate da
full outer join yesterday_array ya
	on da.host = ya.host
on conflict (host, month_start)
do update set hit_array = EXCLUDED.hit_array,
	unique_visitors_array = EXCLUDED.unique_visitors_array;
