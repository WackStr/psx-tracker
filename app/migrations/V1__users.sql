CREATE TABLE t_user (
    id SERIAL PRIMARY KEY,  -- auto-incrementing primary key
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,  -- Email must be unique
    password VARCHAR(255) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Automatically set to current time
    CONSTRAINT users_email_unique UNIQUE(email)  -- This will automatically create a unique index on email
);

-- Add indexes to improve query performance
CREATE INDEX idx_users_first_name ON t_user(first_name);
CREATE INDEX idx_users_last_name ON t_user(last_name);
CREATE INDEX idx_users_created_on ON t_user(created_on);
