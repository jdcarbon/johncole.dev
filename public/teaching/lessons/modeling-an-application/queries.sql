-- Example queries for the subscription-tracking lesson.
-- Assumes schema.sql and seed.sql have already been loaded.

PRAGMA foreign_keys = ON;

-- 1. All active subscriptions for the Operations team.
SELECT s.name, s.vendor, s.cost_minor, s.currency, s.next_renewal_date
FROM subscriptions AS s
JOIN teams AS t ON t.id = s.team_id
WHERE t.name = 'Operations'
  AND s.status = 'active'
ORDER BY s.name;

-- 2. Subscriptions renewing between 2026-11-01 and 2026-11-30 (inclusive).
SELECT t.name AS team_name, s.name AS subscription_name, s.next_renewal_date
FROM subscriptions AS s
JOIN teams AS t ON t.id = s.team_id
WHERE s.status = 'active'
  AND s.next_renewal_date BETWEEN '2026-11-01' AND '2026-11-30'
ORDER BY s.next_renewal_date;

-- 3. Total monthly recurring cost for active monthly subscriptions only.
--    (Annual subscriptions are intentionally excluded from this total.)
SELECT SUM(cost_minor) AS monthly_recurring_cost_minor
FROM subscriptions
WHERE status = 'active'
  AND billing_interval = 'monthly';

-- 4. Join across teams and subscriptions.
SELECT t.name AS team_name,
       s.name AS subscription_name,
       s.vendor,
       s.billing_interval,
       s.status
FROM teams AS t
JOIN subscriptions AS s ON s.team_id = t.id
ORDER BY t.name, s.name;
