CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, role INTEGER);

CREATE TABLE recipes (id SERIAL PRIMARY KEY, title TEXT, instructions TEXT, user_id INTEGER REFERENCES users);
