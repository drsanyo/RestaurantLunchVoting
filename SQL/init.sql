CREATE DATABASE RestaurantLunchVoting;
CREATE USER docker WITH PASSWORD 'docker';

ALTER ROLE docker SET client_encoding TO 'utf8';
ALTER ROLE docker SET default_transaction_isolation TO 'read committed';
ALTER ROLE docker SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE RestaurantLunchVoting TO docker;