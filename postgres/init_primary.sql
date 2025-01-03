-- Create a replication user
CREATE ROLE replication_user WITH REPLICATION LOGIN PASSWORD 'replication_password';
SELECT pg_create_physical_replication_slot('replication_slot');

CREATE USER "user" WITH PASSWORD 'password';

-- Grant connection privileges to the replication user (if needed)
GRANT CONNECT ON DATABASE postgres TO replication_user;
GRANT CONNECT ON DATABASE postgres TO "user";

-- Modify necessary configuration parameters for replication
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET wal_keep_size = '64MB';
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET hot_standby = on;

-- CREATE TABLE phonebook(phone VARCHAR(32), firstname VARCHAR(32), lastname VARCHAR(32), address VARCHAR(64));
-- INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7891', 'John3', 'Doe1', 'North America');
-- INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7892', 'John2', 'Doe2', 'North America');
-- INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7893', 'John1', 'Doe2', 'North America');
-- Reload PostgreSQL configuration to apply changes
SELECT pg_reload_conf();
