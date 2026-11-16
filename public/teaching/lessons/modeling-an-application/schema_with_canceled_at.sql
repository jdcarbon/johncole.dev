-- Exercise A solution sketch: record when a subscription was canceled.
-- This replaces the base subscriptions definition for the extended model.

PRAGMA foreign_keys = ON;

CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    vendor TEXT NOT NULL,
    name TEXT NOT NULL,
    cost_minor INTEGER NOT NULL CHECK (cost_minor >= 0),
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    billing_interval TEXT NOT NULL CHECK (
        billing_interval IN ('monthly', 'annual')
    ),
    next_renewal_date TEXT NOT NULL CHECK (
        next_renewal_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    ),
    status TEXT NOT NULL CHECK (status IN ('active', 'canceled')),
    canceled_at TEXT CHECK (
        canceled_at IS NULL
        OR canceled_at GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    ),
    FOREIGN KEY (team_id) REFERENCES teams (id),
    CHECK (
        (status = 'active' AND canceled_at IS NULL)
        OR (status = 'canceled' AND canceled_at IS NOT NULL)
    )
);
