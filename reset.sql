-- Drop the database if it exists
DROP DATABASE IF EXISTS hbnb_dev_db;

-- Create the database
CREATE DATABASE hbnb_dev_db;

-- Use the new database
USE hbnb_dev_db;

-- Optionally, you can also create the user and grant privileges again
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
