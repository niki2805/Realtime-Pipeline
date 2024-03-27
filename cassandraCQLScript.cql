CREATE KEYSPACE IF NOT EXISTS watch_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = true;

CREATE KEYSPACE IF NOT EXISTS browse_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = true;

CREATE KEYSPACE IF NOT EXISTS search_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = true;

-- CREATE TABLE IF NOT EXISTS watch_keyspace.watch_events (event_name text, user_id int, video_id text, timestamp timestamp, ip varchar, time int, PRIMARY KEY((event_name, user_id), timestamp)) WITH CLUSTERING ORDER BY (timestamp DESC);
--
-- CREATE TABLE IF NOT EXISTS browse_keyspace.browse_events (event_name text, title_id text, user_id int, row text, timestamp timestamp, ip varchar, PRIMARY KEY((event_name, title_id), timestamp)) WITH CLUSTERING ORDER BY (timestamp DESC);
--
-- CREATE TABLE IF NOT EXISTS search_keyspace.search_events (user_id int, term text, genre text, timestamp timestamp, ip varchar, PRIMARY KEY((user_id, term, genre), timestamp)) WITH CLUSTERING ORDER BY (timestamp DESC);

CREATE TABLE IF NOT EXISTS watch_keyspace.events_count (event_name text, count int, PRIMARY KEY(event_name));

CREATE TABLE IF NOT EXISTS browse_keyspace.events_count (event_name text, count int, PRIMARY KEY(event_name));

CREATE TABLE IF NOT EXISTS search_keyspace.events_count (event_name text, count int, PRIMARY KEY(event_name));