CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar(50) NOT NULL UNIQUE,
    password varchar(20) NOT NULL
);


INSERT INTO user(email, password) VALUES ('satyakighosh65@gmail.com', 'admin123')