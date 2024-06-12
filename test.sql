

declare @tempstatus as VARCHAR(50)

select (case when )

/*task 1*/
alter table changelogs
add column id serial primary key;
--
create view task1 as
select c_new.issue_key, c_new.author_key, c_t.from_status as status, c_new.created_at as start_date, c_t.created_at as end_date, EXTRACT(EPOCH from (c_t.created_at-c_new.created_at)) as difference
from   (select *
		from (select c_.issue_key, c_.author_key , c_.from_status, c_.to_status, c_.created_at,
				min(case	
						when EXTRACT(EPOCH from (c_t.created_at-c_.created_at)) <= 0 then null
						else EXTRACT(EPOCH from (c_t.created_at-c_.created_at))
					end
				) as min
			
				from changelogs as c_ inner join changelogs as c_t ON c_.issue_key = c_t.issue_key and c_t.from_status = c_.to_status
				group by c_.id
				order by c_.issue_key desc) as te
		where te.min is not null) as c_new inner join changelogs as c_t 
	ON (c_new.issue_key = c_t.issue_key and c_t.from_status = c_new.to_status) and c_new.min = EXTRACT(EPOCH from (c_t.created_at-c_new.created_at))

-- OR

create view c_temp_id as
select *, row_number() over () as id
from changelogs;
	
create view task12 as
select c_new.issue_key, c_new.author_key, c_t.from_status as status, c_new.created_at as start_date, c_t.created_at as end_date, EXTRACT(EPOCH from (c_t.created_at-c_new.created_at)) as difference
from   ( select *
		from (select min(c_.issue_key) as issue_key
				, min(c_.author_key) as author_key
				, min(c_.from_status) as from_status
				, min(c_.to_status) as to_status
				, min(c_.created_at) as created_at
				, min(case	
						when EXTRACT(EPOCH from (c_t.created_at-c_.created_at)) <= 0 then null
						else EXTRACT(EPOCH from (c_t.created_at-c_.created_at))
					end
				) as min_time
				, c_.id
				from c_temp_id as c_ inner join changelogs as c_t ON c_.issue_key = c_t.issue_key and c_t.from_status = c_.to_status
				group by c_.id) as te
		where te.min_time is not null
		) as c_new inner join changelogs as c_t
	ON (c_new.issue_key = c_t.issue_key and c_t.from_status = c_new.to_status) and c_new.min_time = EXTRACT(EPOCH from (c_t.created_at-c_new.created_at));

/*done*/

--check week day
--where extract(dow from start_date) between 1 and 5
--where .status like "In progress"

-- видозмінює значення початку/кінця роботи над задачею у відповідності до обмежень щодо
-- -	робочого часу з 10:00:00 до 20:00:00
-- -	робочих днів з ПН по ПТ (ПН = 1, ПТ = 5, НД = 7)
-- Тонкощі реалізації:
-- -		у випадку початку/закінчення роботи у вихідні, значення автоматично переводиться на початок робочого дня вже з *наступного* тижня
-- - 		у випадку початку/закінчення роботи за межами визначеного робочого часу, 
--				або зменшується кількість часу за рахунок обмеження значення до однієї з границь інтервалу (нижня межа)
--				або переводить значення на наступний робочий день (верхня межа)
create view temp_task3 as
select * --, extract(isodow from start_date) as day_of_week_start, extract(isodow from end_date) as day_of_week_end
	, 	case
		when extract(isodow from start_date) not between 1 and 5 
		then date_trunc('day', start_date) + (7 - extract(isodow from start_date) + 1) * interval '1 day' + interval '10 hours'
		else case
				when extract(hour from start_date) between 10 and 20-1 then start_date
				when extract(hour from start_date) < 10 then date_trunc('day', start_date) + interval '10 hours'
				else 
					case 
						when extract(isodow from start_date) = 5 then date_trunc('day', start_date) + 3 * interval '1 day' + interval '10 hours'
						else date_trunc('day', start_date) + interval '1 day 10 hours'
					end
			end
		end as start
	, 	case
		when extract(isodow from end_date) not between 1 and 5 
		then date_trunc('day', end_date) + (7 - extract(isodow from end_date) + 1) * interval '1 day' + interval '10 hours'
		else case 
				when extract(hour from end_date) between 10 and 20-1 then end_date
				when extract(hour from end_date) >= 20 then 
					case
						when extract(isodow from end_date) = 5 then date_trunc('day', end_date) + 3 * interval '1 day' + interval '10 hours'
						else date_trunc('day', end_date) + interval '1 day 10 hours'
					end
				else date_trunc('day', end_date) + interval '10 hours'
			end
		end as end
from task12
--||
--\/
create or replace function fix_time(_date_ timestamp, out fix_date timestamp) as $$
declare
	start_week integer := 1;
	end_week integer := 5;
	start_hour integer := 10;
	end_hour integer := 20;
	start_time_interval time := interval '1 hour' * start_hour;
begin
	fix_date = 	case
					when extract(isodow from _date_) not between start_week and end_week
					then date_trunc('day', _date_) + (7 - extract(isodow from _date_) + 1) * interval '1 day' + start_time_interval
					else case
							when extract(hour from _date_) between start_hour and end_hour-1 then _date_
							when extract(hour from _date_) < start_hour then date_trunc('day', _date_) + start_time_interval
							else 
								case 
									when extract(isodow from _date_) = end_week then date_trunc('day', _date_) + (7 - extract(isodow from _date_) + 1) * interval '1 day' + start_time_interval
									else date_trunc('day', _date_) + interval '1 day' + start_time_interval
								end
						end
				end;

end;
$$ language plpgsql;


select *, extract(week from temp_task3.end) - extract(week from temp_task3.start) as week_diff
from temp_task3

-- week diff
-- interval '2 days' * (extract(week from temp_task3.end) - extract(week from temp_task3.start))
-- year diff 
-- interval '2 days' * 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start))
-- day diff
-- interval '14 hours' * (extract(day from temp_task3.end) - extract(day from temp_task3.start))
-- time diff
-- extract(epoch from (temp_task3.end - temp_task3.start 
--						- interval '14 hours' * (extract(day from temp_task3.end) - extract(day from temp_task3.start) - 2*(extract(week from temp_task3.end) - extract(week from temp_task3.start)))
--						- interval '2 days' * (extract(week from temp_task3.end) - extract(week from temp_task3.start))
--						- interval '2 days' * 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start))
--						))

select c_n.issue_key, sum(c_n.working_duration) as sum_in_progress 
from (select *
	, extract(epoch from (temp_task3.end - temp_task3.start 
						- interval '14 hours' * ( (case
														when extract(epoch from (temp_task3.end::time - temp_task3.start::time)) < 0 then extract(day from (temp_task3.end - temp_task3.start)) + 1
														else extract(day from (temp_task3.end - temp_task3.start))
													end)
													- (2*(extract(week from temp_task3.end) - extract(week from temp_task3.start) 
													+ 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start)))))
						- (interval '2 days' * (extract(week from temp_task3.end) - extract(week from temp_task3.start)
						+ 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start))))
						)) as working_duration
	from temp_task3) as c_n
where c_n.status like 'In Progress'
group by c_n.issue_key


-----------------------
/*
-- видозмінює значення початку/кінця роботи над задачею у відповідності до обмежень щодо
-- -	робочого часу з 10:00:00 до 20:00:00
-- -	робочих днів з ПН по ПТ (ПН = 1, ПТ = 5, НД = 7)
-- Тонкощі реалізації:
-- -		у випадку початку/закінчення роботи у вихідні, значення автоматично переводиться на початок робочого дня вже з *наступного* тижня
-- - 		у випадку початку/закінчення роботи за межами визначеного робочого часу, 
--				або зменшується кількість часу за рахунок обмеження значення до однієї з границь інтервалу (нижня межа)
--				або переводить значення на наступний робочий день (верхня межа)
*/
create or replace function fix_time(_date_ timestamp, out fix_date timestamp) as $$
declare
	start_week integer := 1;
	end_week integer := 5;
	start_hour integer := 10;
	end_hour integer := 20;
	start_time_interval interval := interval '1 hour' * start_hour;
begin
	fix_date = 	case
					when extract(isodow from _date_) not between start_week and end_week
					then date_trunc('day', _date_) + (7 - extract(isodow from _date_) + 1) * interval '1 day' + start_time_interval
					else case
							when extract(hour from _date_) between start_hour and end_hour-1 then _date_
							when extract(hour from _date_) < start_hour then date_trunc('day', _date_) + start_time_interval
							else 
								case 
									when extract(isodow from _date_) = end_week then date_trunc('day', _date_) + (7 - extract(isodow from _date_) + 1) * interval '1 day' + start_time_interval
									else date_trunc('day', _date_) + interval '1 day' + start_time_interval
								end
						end
				end;

end;
$$ language plpgsql;

-- визначає різницю тижнів, щоб врахувати вихідні дні
create or replace function culc_week_interval(time_start timestamp, time_end timestamp) returns integer as $$
declare
	count_of_week_in_year integer := 52;
begin
	return extract(week from time_end) - extract(week from time_start) + count_of_week_in_year * (extract(isoyear from time_end) - extract(isoyear from time_start));
end;
$$ language plpgsql;

-- week diff
-- interval '2 days' * (extract(week from temp_task3.end) - extract(week from temp_task3.start))
-- year diff 
-- interval '2 days' * 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start))
-- day diff
-- interval '14 hours' * (extract(day from temp_task3.end) - extract(day from temp_task3.start))
-- time diff
-- extract(epoch from (temp_task3.end - temp_task3.start 
--						- interval '14 hours' * (extract(day from temp_task3.end) - extract(day from temp_task3.start) - 2*(extract(week from temp_task3.end) - extract(week from temp_task3.start)))
--						- interval '2 days' * (extract(week from temp_task3.end) - extract(week from temp_task3.start))
--						- interval '2 days' * 52 * (extract(isoyear from temp_task3.end) - extract(isoyear from temp_task3.start))
--						))
create or replace function culc_time(time_start timestamp, time_end timestamp) returns integer as $$
declare
	not_working_time_interval interval := interval '14 hours';
	count_of_free_days integer := 2;
	free_day_interval interval := count_of_free_days * interval '1 day';
	week_differences integer := culc_week_interval(time_start,time_end);
begin
	return extract(epoch from (time_end - time_start
						- not_working_time_interval * ( (case
														when extract(epoch from (time_end::time - time_start::time)) < 0 
															then extract(day from (time_end - time_start)) + 1
														else extract(day from (time_end - time_start))
													end)
													- count_of_free_days * week_differences)
						- free_day_interval * week_differences
						));
end;
$$ language plpgsql;












create or replace overlap(start_date_1 timestamp, end_date_1 timestamp, start_date_2 timestamp, end_date_2 timestamp
						, out o_min_value timestamp, out o_max_value timestamp) as $$
declare
	overlap_flag boolean := (start_date_1, end_date_1) overlaps (start_date_2, end_date_2);
begin
	case 
		when not overlap_flag then o_min_value = 0, o_max_value = 0
		else 
			case
				when extract(epoch from start_date_1)
	end
end;
$$ language plpgsql;