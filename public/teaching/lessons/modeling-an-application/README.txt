Modeling a Real-World Application — supporting files
====================================================

schema.sql                   Base SQLite schema
seed.sql                     Fictional sample data
queries.sql                  Example queries from the lesson
schema_with_canceled_at.sql  Exercise A extension

Create a local database:

  sqlite3 subscriptions.db < schema.sql
  sqlite3 subscriptions.db < seed.sql
  sqlite3 subscriptions.db < queries.sql
