
CREATE DATABASE IF NOT EXISTS onlineshop;


USE onlineshop;


DROP TABLE IF EXISTS PrivateCustomers;
DROP TABLE IF EXISTS CompanyCustomers;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Electronics;
DROP TABLE IF EXISTS Clothing;
DROP TABLE IF EXISTS Book;

-- =====================================
-- CUSTOMER TABLES
-- =====================================

CREATE TABLE Customers (
    id_customer INT AUTO_INCREMENT PRIMARY KEY,
    type        VARCHAR(20),
    name        VARCHAR(100),
    address     VARCHAR(255),
    email       VARCHAR(100),
    phone       VARCHAR(20),
    password    VARCHAR(255)
);

CREATE TABLE PrivateCustomers (
    id_customer INT PRIMARY KEY,
    birthdate   VARCHAR(10),
    FOREIGN KEY (id_customer)
        REFERENCES Customers(id_customer)
        ON DELETE CASCADE
);

CREATE TABLE CompanyCustomers (
    id_customer INT PRIMARY KEY,
    company_id  VARCHAR(20),
    FOREIGN KEY (id_customer)
        REFERENCES Customers(id_customer)
        ON DELETE CASCADE
);

-- =====================================
-- PRODUCT TABLES
-- =====================================

CREATE TABLE Electronics (
    id_electronic  INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255),
    price          DECIMAL(10,2),
    weight         DECIMAL(10,2),
    brand          VARCHAR(100),
    warranty_years INT
);

CREATE TABLE Clothing (
    id_cloth INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(255),
    price    DECIMAL(10,2),
    weight   DECIMAL(10,2),
    size     VARCHAR(20),
    color    VARCHAR(50)
);

CREATE TABLE Book (
    id_book    INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255),
    price      DECIMAL(10,2),
    weight     DECIMAL(10,2),
    author     VARCHAR(100),
    page_count INT
);