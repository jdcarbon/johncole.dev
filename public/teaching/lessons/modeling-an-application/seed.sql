-- Fictional sample data for the subscription-tracking lesson.
-- Run after schema.sql: sqlite3 subscriptions.db < seed.sql

PRAGMA foreign_keys = ON;

INSERT INTO teams (id, name) VALUES
    (1, 'Operations'),
    (2, 'Marketing');

INSERT INTO subscriptions (
    id,
    team_id,
    vendor,
    name,
    cost_minor,
    currency,
    billing_interval,
    next_renewal_date,
    status
) VALUES
    (1, 1, 'CloudHost', 'App Hosting', 4900, 'USD', 'monthly', '2026-12-01', 'active'),
    (2, 1, 'MailCo', 'Transactional Email', 2900, 'USD', 'monthly', '2026-11-20', 'active'),
    (3, 1, 'SecureKey', 'SSO Add-on', 12000, 'USD', 'annual', '2027-03-15', 'active'),
    (4, 2, 'DesignKit', 'Asset Library', 3900, 'USD', 'monthly', '2026-11-28', 'active'),
    (5, 2, 'AdReach', 'Campaign Analytics', 9900, 'USD', 'monthly', '2026-10-05', 'canceled'),
    (6, 2, 'WriteWell', 'Copy Assistant', 15000, 'USD', 'annual', '2027-01-10', 'active');
