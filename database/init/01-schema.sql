-- Enable PostgreSQL extension required
-- for advanced booking overlap constraints.

CREATE EXTENSION IF NOT EXISTS btree_gist;