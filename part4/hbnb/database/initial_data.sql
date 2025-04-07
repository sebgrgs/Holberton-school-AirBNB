-- Insert admin user (password is 'admin1234' hashed with bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    'adminadmin01',
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi'),
    ('550e8400-e29b-41d4-a716-446655440001', 'Swimming Pool'),
    ('550e8400-e29b-41d4-a716-446655440002', 'Air Conditioning');

-- Insert initial places
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
    ('660e8400-e29b-41d4-a716-446655440000', 'Cozy Apartment', 'A beautiful apartment in the city center', 100.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1'),
    ('660e8400-e29b-41d4-a716-446655440001', 'Beach House', 'Perfect getaway by the ocean', 200.00, 25.7617, -80.1918, '36c9050e-ddd3-4c3b-9731-9f487208bbc1'),
    ('660e8400-e29b-41d4-a716-446655440002', 'Mountain Cabin', 'Peaceful retreat in the mountains', 150.00, 39.5501, -105.7821, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Insert place-amenity relationships
INSERT INTO place_amenities (place_id, amenity_id) VALUES
    ('660e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440000'),
    ('660e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440002'),
    ('660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440000'),
    ('660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001'),
    ('660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440000');

-- Insert reviews
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
    ('770e8400-e29b-41d4-a716-446655440000', 'Great location and very clean!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', '660e8400-e29b-41d4-a716-446655440000'),
    ('770e8400-e29b-41d4-a716-446655440001', 'Amazing view of the ocean', 4, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', '660e8400-e29b-41d4-a716-446655440001'),
    ('770e8400-e29b-41d4-a716-446655440002', 'Perfect for a weekend getaway', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', '660e8400-e29b-41d4-a716-446655440002');