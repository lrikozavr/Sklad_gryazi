

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
	--якщо різниці немає, одразу виводить нуль
	--(додано, через велику кількість нульових* задач)
	if time_start = time_end then return 0.0;
	end if;

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









create or replace function overlap_interval(start_date_1 timestamp, end_date_1 timestamp, start_date_2 timestamp, end_date_2 timestamp) returns record as $$
declare
	o_min_value timestamp;
	o_max_value timestamp;
	result record;
begin
	
		if start_date_2 between start_date_1 and end_date_1 
		then o_min_value := start_date_2;
		else o_min_value := start_date_1;
		end if;
		if end_date_2 between start_date_1 and end_date_1 
		then o_max_value := end_date_2;
		else o_max_value := end_date_1;
		end if;
		
		select o_min_value, o_max_value into result;		
		return result;
end;
$$ language plpgsql;




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
	--якщо різниці немає, одразу виводить нуль
	--(додано, через велику кількість нульових* задач)
	if time_start = time_end then return 0.0;
	end if;

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

create table overlap_interval_table (
	start_date timestamp without time zone,
	end_date timestamp without time zone
);

create or replace function overlap_interval() returns setof bigint as $$
declare
	temp_flag_index_weight integer := 0;
	first_record_flag integer := 0;
	temp_record record;
	record_id_array integer[];
	temp_record_id_array integer;
	i record;
begin
	create temp table temp_index (
		id 					integer,
		date 				timestamp without time zone,
		flag_index 			integer
		--flag_index_weight 	integer
		);

	raise notice 'start table 1';

-- створюємо таблицю і відмічаємо початок і кінець
	for i in (select *, row_number() over () as id from overlap_interval_table
		) loop
		--insert into temp_index values (,'',,)
		insert into temp_index values (i.id,i.start_date,1);
		insert into temp_index values (i.id,i.end_date,-1);
--		raise notice 'start table 1 %', i.id;
	end loop;

	create temp table temp_index_weight (
		id 					integer,
		date 				timestamp without time zone,
		flag_index 			integer,
		flag_index_weight 	integer
		);

	raise notice 'end table 1';
	-- рахуємо які саме інтервали нашаровуються
	for i in (select * from temp_index order by date asc) loop
		--додай запобіжник, щоб не було значень -1
		--а він взагалі треба?
		insert into temp_index_weight values (i.id,i.date,i.flag_index,i.flag_index + temp_flag_index_weight);
		temp_flag_index_weight := i.flag_index + temp_flag_index_weight;
	end loop;
	raise notice 'end table 2';
	--
	create temp table temp_result (
		id 			integer,
		date_start 	timestamp without time zone,
		date_end 	timestamp without time zone,
		deep 		integer
	);
	--
	raise notice 'start of loop %', clock_timestamp();
	for i in (select * from temp_index_weight) loop
		if first_record_flag = 0 then first_record_flag = 1; temp_record = i; continue;
		else 
			-- перевірка початку/кінця інтервалу
			case 
				when temp_record.flag_index = 1 then record_id_array := array_append(record_id_array,temp_record.id);
				when temp_record.flag_index = -1 then record_id_array := array_remove(record_id_array,temp_record.id);
				else raise notice 'flag_index column have upexpected value %', temp_record.id;
			end case;

			-- перевірка на інтервал з порожнім часом
			if temp_record.flag_index_weight = 0 then temp_record = i; continue; end if;

			--?
			foreach temp_record_id_array in array record_id_array loop
				--insert into temp_result values (temp_record_id_array,temp_record.date,i.date,abs(temp_record.flag_index_weight));
				insert into temp_result values (temp_record_id_array,temp_record.date,i.date,temp_record.flag_index_weight);
			end loop;
			
			temp_record = i;
		end if;

		--exit when i.flag_index = -1;

--		перевірка наявності значення в масиві
--		= any (record_id_array);
	end loop;
	
	raise notice 'end of loop %', clock_timestamp();
	-- вивід підрахунку часу для кожної задачі, за правилом, ділення на загальну кількість перетинання
	return query (select
		sum(culc_time(fix_time(date_start),fix_time(date_end))/deep) as work_duration from temp_result group by id order by id asc);
	
	drop table temp_result;
	drop table temp_index;
	drop table temp_index_weight;
end;
$$ language plpgsql;


create or replace function working_culc() returns void as $$
declare
	i text;
begin
	create table working_table (
	issue_key text,
	author_key text, 
	start_date timestamp without time zone,
	end_date timestamp without time zone, 
	work_duration bigint, 
	price real
	);
	
	for i in (select distinct author_key from task12) loop
		raise notice '%', i;
		create view temp_author as
		select * 
		from task12
		where task12.author_key = i and status = 'In Progress';

		truncate table overlap_interval_table;
		insert into overlap_interval_table (start_date, end_date)
		select start_date, end_date
		from temp_author;

		insert into working_table (issue_key, author_key, start_date, end_date, work_duration, price)
		select ori.issue_key, ori.author_key, ori.start_date, ori.end_date, ov.work_duration, (case when (ori.author_key like 'JIRAUSER%') then 1 else 2 end)
		from (select row_number() over () as id, work_duration
				from overlap_interval()) as ov inner join (select row_number() over () as id, * from temp_author) as ori ON ov.id = ori.id;
		
		drop view temp_author;
	end loop;

end;
$$ language plpgsql;