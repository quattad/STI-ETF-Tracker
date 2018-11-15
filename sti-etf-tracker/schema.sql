DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS stock;

-- create table that stores usernames and passwords
CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);

-- create table that stores the stocks that a user owns
CREATE TABLE stock(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, stock_name TEXT NOT NULL, stock_ticker TEXT NOT NULL, stock_quantity INTEGER NOT NULL);