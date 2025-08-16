-- DDL for user_devices_cumulated --
create table user_devices_cumulated (
	user_id TEXT,
	browser_type TEXT,
	device_activity_datelist DATE[],
	date date, --current_date
	primary key (user_id, browser_type, date)
);

-- A DDL for `hosts_cumulated` table
create table hosts_cumulated(
	host text,
	host_activity_datelist date[],
	date date,
	primary key (host, date)
);

-- A monthly, reduced fact table DDL `host_activity_reduced`
create table host_activity_reduced(
	host text,
	month_start date,
	hit_array integer[],
	unique_visitors_array integer[],
	primary key(host, month_start)
);