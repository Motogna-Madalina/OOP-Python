CREATE DATABASE IF NOT EXISTS shop_warenwelt;
USE shop_warenwelt;

CREATE TABLE customer (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100)  NOT NULL,
    address   VARCHAR(255)  NOT NULL,
    email     VARCHAR(100)  NOT NULL UNIQUE,
    phone     VARCHAR(30)   NOT NULL,
    password  VARCHAR(255)  NOT NULL
);

CREATE TABLE private_customer (
    customer_id  INT PRIMARY KEY,
    birthdate    DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);

CREATE TABLE company_customer (
    customer_id  INT PRIMARY KEY,
    company_id   VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);

CREATE TABLE product (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(150)   NOT NULL,
    price   DECIMAL(10,2)  NOT NULL,
    weight  DECIMAL(10,3)  NOT NULL
);

CREATE TABLE electronic (
    product_id      INT PRIMARY KEY,
    brand           VARCHAR(100) NOT NULL,
    warranty_years  INT          NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE clothing (
    product_id  INT PRIMARY KEY,
    size        VARCHAR(20) NOT NULL,
    color       VARCHAR(50) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE book (
    product_id  INT PRIMARY KEY,
    author      VARCHAR(150) NOT NULL,
    pages       INT          NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);