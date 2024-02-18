CREATE DATABASE records_store;
USE records_store;

CREATE TABLE records_list (
record_id varchar(30) primary key,
title varchar(100),
artist varchar(100),
price decimal (4,2),
genre varchar(100)
);

CREATE TABLE records_stats (
record_id varchar(30) primary key,
unit_sales int,
rating decimal (2,1),

);

CREATE TABLE current_transactions (
transaction_id varchar(15) primary key,
customer_id varchar(30),
last_name char(30),
sales_total decimal(10,2),
tender_type char(15)
);

CREATE TABLE transaction_history(
transaction_id varchar(15) primary key,
customer_id varchar(30),
sales_total decimal(10,2),
tender_type char(15)
);

CREATE TABLE customers(
customer_id varchar(15) primary key,
first_name char(30),
last_name char(30)
);

CREATE TABLE employees(
employee_id varchar(15) primary key,
emp_position char(40),
first_name char(30),
last_name char(30)
);



