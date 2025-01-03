-- Create the user if it doesn't exist
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user') THEN
      CREATE USER "user" WITH PASSWORD 'password';
   END IF;
END
$$;

-- Create the database if it doesn't exist
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'dbname') THEN
      CREATE DATABASE dbname;
   END IF;
END
$$;

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE dbname TO "user";
