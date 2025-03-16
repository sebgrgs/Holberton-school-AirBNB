-- Test SELECT queries
SELECT * FROM users WHERE is_admin = TRUE;
SELECT * FROM amenities;

-- Test INSERT queries
INSERT INTO users (id, first_name, last_name, email, password)
VALUES (
    UUID(),
    'Test',
    'User',
    'test@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPakkBQfAUjIG'
);

-- Test UPDATE queries
UPDATE users 
SET first_name = 'Updated'
WHERE email = 'test@example.com';

-- Test DELETE queries
DELETE FROM users 
WHERE email = 'test@example.com';

-- Test relationships
-- Insert a place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    UUID(),
    'Test Place',
    'Test Description',
    100.00,
    40.7128,
    -74.0060,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- Get all places with their owners
SELECT places.*, users.first_name, users.last_name 
FROM places 
JOIN users ON places.owner_id = users.id;