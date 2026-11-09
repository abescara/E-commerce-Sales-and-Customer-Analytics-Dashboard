-- BigQuery Standard SQL. Run in a project allowed to query public datasets.
-- This defines a NEW completed-sales export. The saved historical CSV may
-- differ if its original status filter or source snapshot was different.
-- Replace the cutoff date when refreshing; record the query date in README.
SELECT
  DATE_TRUNC(DATE(oi.created_at), MONTH) AS month,
  p.category,
  COUNT(DISTINCT oi.order_id) AS total_orders,
  COUNT(oi.id) AS items_sold,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(AVG(oi.sale_price), 2) AS average_item_price
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
  ON oi.product_id = p.id
WHERE oi.status = 'Complete'
  AND oi.created_at < TIMESTAMP('2026-10-01')
  AND p.category IS NOT NULL
GROUP BY month, p.category
ORDER BY month, p.category;
