/*CREATE TABLE default_users (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 age INTEGER NOT NULL,
 username TEXT NOT NULL,
 password TEXT NOT NULL,
 email TEXT NOT NULL,
 join_date DATETIME NOT NULL
);

CREATE TABLE products (
 id INTEGER PRIMARY KEY,
 product_name TEXT NOT NULL,
 price REAL NOT NULL
);
*/

CREATE TABLE orders (
 id INTEGER PRIMARY KEY,
 user_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 quantity INTEGER NOT NULL,
 order_date DATETIME NOT NULL,
 FOREIGN KEY (user_id) REFERENCES default_users(id),
 FOREIGN KEY (product_id) REFERENCES products(id)
);