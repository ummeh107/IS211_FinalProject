DROP TABLE IF EXISTS Registration;
DROP TABLE IF EXISTS Users;

CREATE TABLE Registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT,
    last_name TEXT,
    password TEXT,
    email TEXT,
    city TEXT,
    gender TEXT
);

CREATE TABLE Users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_id INTEGER,
    item INTEGER,
    amount Float,
    date DATE
);



INSERT INTO Registration
                    (first_name, last_name, password, email, city, gender)VALUES("John", "Smith", "123456", "jsmith@gmail.com", "New York", "Male");


