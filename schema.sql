CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);

CREATE TABLE recipes (id SERIAL PRIMARY KEY, title TEXT, description TEXT, user_id INTEGER REFERENCES users);