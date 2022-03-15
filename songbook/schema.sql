DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS song;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE song (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  composer_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  author TEXT NULL,
  description TEXT NULL,
  email TEXT NULL,
  subtitle TEXT NULL,
  FOREIGN KEY (composer_id) REFERENCES user (id)
);