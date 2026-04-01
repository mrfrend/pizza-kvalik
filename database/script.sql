CREATE DATABASE pizzeria_db;
USE pizzeria_db;

-- =====================
-- ROLES
-- =====================
CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO roles (role_name) VALUES
('guest'),
('client'),
('operator'),
('manager'),
('admin');


-- =====================
-- USERS
-- =====================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    contact_info VARCHAR(255),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

INSERT INTO users (username, password_hash, role_id, contact_info) VALUES
('ivan', 'hash1', 2, 'ivan@mail.com'),
('operator1', 'hash2', 3, 'kitchen@mail.com'),
('admin1', 'hash3', 5, 'admin@mail.com');


-- =====================
-- MENU ITEMS
-- =====================
CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image VARCHAR(255) NULL
);

INSERT INTO menu_items (name, description, price, category, image) VALUES
('Маргарита', 'Томат, сыр', 500.00, 'pizza', 'Маргарита.jpg'),
('Пепперони', 'Колбаса, сыр', 650.00, 'pizza', 'Пепперони.jpg'),
('Цезарь', 'Курица, салат', 450.00, 'salad', 'Цезарь с курицей.jpg');


-- =====================
-- ORDERS
-- =====================
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Ожидает приготовления',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO orders (user_id, total_amount, status) VALUES
(1, 1150.00, 'Готово'),
(1, 500.00, 'Ожидает приготовления'),
(1, 650.00, 'Доставляется');


-- =====================
-- ORDER ITEMS
-- =====================
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

INSERT INTO order_items (order_id, item_id, quantity) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 1, 1);


-- =====================
-- PAYMENTS
-- =====================
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

INSERT INTO payments (order_id, amount, payment_method) VALUES
(1, 1150.00, 'card'),
(2, 500.00, 'cash'),
(3, 650.00, 'card');


-- =====================
-- REVIEWS
-- =====================
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

INSERT INTO reviews (user_id, item_id, rating, comment) VALUES
(1, 1, 5, 'Очень вкусно'),
(1, 2, 4, 'Норм'),
(1, 3, 3, 'Средне');


-- =====================
-- SPECIAL OFFERS
-- =====================
CREATE TABLE special_offers (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    discount_percentage DECIMAL(5,2),
    valid_from DATE,
    valid_to DATE
);

INSERT INTO special_offers (name, description, discount_percentage, valid_from, valid_to) VALUES
('Скидка 10%', 'На все пиццы', 10, '2026-01-01', '2026-12-31'),
('Комбо', 'Пицца + напиток', 15, '2026-03-01', '2026-04-01'),
('Happy Hour', 'Скидка днем', 20, '2026-03-10', '2026-03-20');

DELIMITER $$
CREATE FUNCTION get_order_sum(p_order_id INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE sum_order DECIMAL(10, 2) DEFAULT 0;
    SET sum_order = (
        SELECT SUM(quantity * price)
        FROM order_items
        JOIN menu_items ON order_items.item_id = menu_items.item_id
        WHERE order_id = p_order_id
    );

    RETURN sum_order;

END $$

DELIMITER ;


CREATE VIEW order_stats AS
SELECT status, COUNT(*) AS orders_amount  
FROM orders
GROUP BY status;
