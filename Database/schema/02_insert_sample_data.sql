INSERT INTO categories (category_name, description)
VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Clothing', 'Clothes and fashion products'),
    ('Home & Kitchen', 'Products for home and kitchen'),
    ('Books', 'Books and educational materials'),
    ('Sports', 'Sports and fitness products');

-- Insert sample products
INSERT INTO products
(product_name, description, price, stock_quantity, category_id)
VALUES
('Wireless Headphones', 'Bluetooth wireless headphones', 4500.00, 25, 1),
('Smart Watch', 'Fitness and smart notification watch', 6500.00, 15, 1),
('Men T-Shirt', 'Cotton casual t-shirt', 1800.00, 40, 2),
('Kitchen Blender', 'Electric kitchen blender', 5500.00, 10, 3),
('Python Programming Book', 'Beginner to advanced Python programming', 2500.00, 20, 4),
('Running Shoes', 'Comfortable sports running shoes', 7000.00, 12, 5);

-- Insert sample customers
INSERT INTO customers
(first_name, last_name, email, phone, city, country)
VALUES
('Ali', 'Khan', 'ali.khan@example.com', '03001234567', 'Karachi', 'Pakistan'),
('Ahmed', 'Raza', 'ahmed.raza@example.com', '03111234567', 'Lahore', 'Pakistan'),
('Sara', 'Ahmed', 'sara.ahmed@example.com', '03221234567', 'Islamabad', 'Pakistan'),
('Hassan', 'Ali', 'hassan.ali@example.com', '03331234567', 'Sukkur', 'Pakistan'),
('Ayesha', 'Khan', 'ayesha.khan@example.com', '03441234567', 'Hyderabad', 'Pakistan');

-- Insert sample orders
INSERT INTO orders
(customer_id, order_date, status, total_amount)
VALUES
(1, '2026-09-01 10:30:00', 'Completed', 4500.00),
(2, '2026-09-02 14:15:00', 'Completed', 8300.00),
(3, '2026-09-03 16:45:00', 'Pending', 5500.00),
(4, '2026-09-04 11:20:00', 'Shipped', 7000.00),
(5, '2026-09-05 18:10:00', 'Completed', 2500.00);

-- Insert sample order items
INSERT INTO order_items
(order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 4500.00),
(2, 2, 1, 6500.00),
(2, 3, 1, 1800.00),
(3, 4, 1, 5500.00),
(4, 6, 1, 7000.00),
(5, 5, 1, 2500.00);

-- Insert sample payments
INSERT INTO payments
(order_id, payment_method, payment_status, amount, payment_date)
VALUES
(1, 'Credit Card', 'Paid', 4500.00, '2026-09-01 10:35:00'),
(2, 'Cash on Delivery', 'Paid', 8300.00, '2026-09-02 14:20:00'),
(3, 'Bank Transfer', 'Pending', 5500.00, '2026-09-03 16:50:00'),
(4, 'Credit Card', 'Paid', 7000.00, '2026-09-04 11:25:00'),
(5, 'Cash on Delivery', 'Paid', 2500.00, '2026-09-05 18:15:00');