-- 1) Общая статистика

select count(distinct order_id) count_orders,
	count(distinct(product_id, quantity)) unic_position,
	sum(revenue) total_revenue,
	avg(revenue) avg_revenue, 
	sum(quantity) total_quantity 
from fact_sales

-- 2) Анализ товаров

select dp.product_name, 
	dp.category,
	sum(fs.quantity) sum_quantity,
	sum(fs.revenue) sum_revenue,
	count(distinct fs.order_id) count_orders
from fact_sales fs
join dim_products dp on fs.product_id = dp.product_id 
group by dp.product_id, dp.product_name, dp.category 
order by sum_revenue desc

-- 3) Анализ городов

select du.city,
	count(distinct(product_id, quantity)) unic_position,
	count(distinct fs.user_id ) unic_users,
	sum(fs.revenue) total_revenue,
	round(sum(fs.revenue) / count(distinct fs.order_id), 2) avg_revenue_for_order
from fact_sales fs 
join dim_users du on fs.user_id = du.user_id 
group by du.city 
order by total_revenue desc

-- 4) Эффективность каналов

select du.channel,
	count(distinct du.user_id) unic_users,
	count(distinct fs.order_id) unic_orders,
	sum(fs.revenue) total_sum,
	round(
		sum(fs.revenue) / count(distinct fs.order_id),
		2
	) avg_check
from fact_sales fs
join dim_users du on fs.user_id = du.user_id 
group by du.channel 
order by total_sum desc

-- 5) Категории и города

select du.city, dp.category, sum(fs.revenue) total_sum
from fact_sales fs 
join dim_users du on fs.user_id = du.user_id 
join dim_products dp on fs.product_id = dp.product_id 
group by du.city, dp.category 
having count(distinct fs.order_id) >=2 and sum(fs.revenue) > 5000
order by total_sum desc

-- 6) Анализ среднего чека

select du.city, 
	round(
		sum(fs.revenue) / count(distinct fs.order_id),
		2
	) avg_check
from fact_sales fs 
join dim_users du on fs.user_id = du.user_id
group by du.city 
having sum(fs.revenue) / count(distinct fs.order_id) > (
	select sum(revenue) / count(distinct order_id )
	from fact_sales
)
order by avg_check desc

-- 7) Динамика продаж

select dd."month",
	dd."year",
	count(distinct fs.order_id) count_orders,
	sum(fs.revenue) total_revenue,
	round(
		sum(fs.revenue) / count(distinct fs.order_id),
		2
	) avg_check
from fact_sales fs
join dim_date dd on fs.date_id = dd.date_id 
group by dd."year", dd."month" 
order by dd."year", dd."month" 

-- 8) Товары выше среднего
select dp.product_name, 
	round(
		avg(fs.revenue),
		2
	) avg_price
from fact_sales fs
join dim_products dp on dp.product_id = fs.product_id 
group by dp.product_id, dp.product_name
having avg(fs.revenue) > (
	select avg(revenue) from fact_sales
) 
order by avg_price desc

-- 9) Лучшие товары в категориях

with max_category as (
	select category, max(max_revenue) max_revenue_grupp
	from (
		select dp.category, max(fs.revenue) max_revenue
		from fact_sales fs
		join dim_products dp on dp.product_id = fs.product_id 
		group by dp.category, dp.product_id
	)
	group by category
)
select dp.category, dp.product_name, mc.max_revenue_grupp
from fact_sales fs
join dim_products dp on dp.product_id = fs.product_id
join max_category mc on dp.category = mc.category 
group by dp.category, dp.product_id, dp.product_name, mc.max_revenue_grupp 
having max(fs.revenue) = mc.max_revenue_grupp
order by mc.max_revenue_grupp desc

-- 10) Покупатели без повторных покупок

select du.user_id,
	du.city,
	du.channel,
	count(distinct fs.order_id) unic_orders,
	sum(fs.revenue) total_revenue
from fact_sales fs 
join dim_users du on fs.user_id = du.user_id
group by du.user_id, du.city, du.channel
having count(distinct fs.order_id) = 1
order by total_revenue desc

-- 11) Рейтинг товаров

with product_revenue as (
	select dp.category, 
		dp.product_name,
		sum(fs.revenue) total_revenue
	from fact_sales fs
	join dim_products dp on dp.product_id = fs.product_id
	group by dp.category, dp.product_id, dp.product_name 
	order by dp.category, total_revenue
)
select *,
	rank() over (
	partition by category
	order by total_revenue desc
	)
from product_revenue

-- 12) Доля выручки

select distinct dp.product_name, 
	sum(fs.revenue) over (
	partition by dp.category, dp.product_name
	) product_revenue,
	sum(fs.revenue) over () total,
	round(
		sum(fs.revenue) over (
		partition by dp.category, dp.product_name
		) * 100 / sum(fs.revenue) over (),
		2
	) percent_from_total
from fact_sales fs
join dim_products dp on dp.product_id = fs.product_id

-- 13) Накопительная выручка

select distinct  
	dd.full_date,
	sum(fs.revenue) over(
	partition by dd.full_date 
	),
	sum(fs.revenue) over(
	order by dd.full_date 
	)
from fact_sales fs
join dim_date dd on fs.date_id = dd.date_id 
order by dd.full_date 

-- 14) Клиентская аналитика

with users_orders as (
	select du.user_id,
		count(distinct fs.order_id) unic_orders,
		sum(fs.revenue) total_revenue,
		case
			when count(distinct fs.order_id) >= 4 then 'Loyal'
			when count(distinct fs.order_id) = 1 then 'One-time'
			else 'Regular'
		end status
	from fact_sales fs 
	join dim_users du on fs.user_id = du.user_id
	group by du.user_id
	union 
	select null, 0, 0, 'Loyal'
	union 
	select null, 0, 0, 'One-time'
	union 
	select null, 0, 0, 'Regular'
)
select status,
	count(user_id) count_user,
	sum(total_revenue) sum_total
from users_orders 
group by status

-- Задание 15. Аналитический отчёт

with city_analitic as (
	select du.city,
		count(distinct fs.user_id) count_users,
		count(distinct fs.order_id) count_orders,
		sum(revenue) total_revenue,
		round(
			sum(revenue) / count(distinct fs.order_id),
			2
		) avg_check,
		sum(fs.quantity) sum_quantity
	from fact_sales fs 
	join dim_users du on fs.user_id = du.user_id
	group by du.city
)
select *,
	round(
		total_revenue / sum(total_revenue ) over(),
		4
	)frac_revenue,
	dense_rank() over(
		order by total_revenue desc
	) city_rank
from city_analitic