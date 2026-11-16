-- Subscription tracking schema for the classroom example.
-- Run with: sqlite3 subscriptions.db < schema.sql

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
    -- Store money as integer minor units (for example, cents).
    cost_minor INTEGER NOT NULL CHECK (cost_minor >= 0),
    currency TEXT NOT NULL CHECK (length(currency) = 3),
    billing_interval TEXT NOT NULL CHECK (
        billing_interval IN ('monthly', 'annual')
    ),
    next_renewal_date TEXT NOT NULL CHECK (
        next_renewal_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    ),
    status TEXT NOT NULL CHECK (status IN ('active', 'canceled')),
    FOREIGN KEY (team_id) REFERENCES teams (id)
);

CREATE INDEX idx_subscriptions_team ON subscriptions (team_id);
CREATE INDEX idx_subscriptions_renewal ON subscriptions (next_renewal_date);
