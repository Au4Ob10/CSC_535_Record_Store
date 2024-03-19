-- Active: 1708706294364@@127.0.0.1@3306

drop schema record_store;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';





-- Schema record_store
CREATE SCHEMA IF NOT EXISTS `record_store`;
USE `record_store`;

-- Table record_store.carts
CREATE TABLE IF NOT EXISTS `record_store`.`carts` (
  `order_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `record_id` INT NULL,
  `status` VARCHAR(45) NULL,
  `add_date` DATE NULL,
  `update_date` DATE NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE = InnoDB;


INSERT INTO carts (order_id, customer_id,record_id,status,add_date,update_date)
VALUES
(10,1,1000,"fulfilled",'2022-01-22','2022-01-23'),
(11,2,1001,"fulfilled",'2023-02-25','2022-02-26'),
(12,3,1002,"fulfilled",'2022-05-23','2022-05-24'),
(13,4,1003,"fulfilled",'2021-07-22','2022-07-23');



-- Table record_store.account
CREATE TABLE IF NOT EXISTS `record_store`.`account` (
`account_id` INT NOT NULL,
  `account_name` VARCHAR(45) NULL,
  `customer_id` VARCHAR(45) NULL,
  `log_status` VARCHAR(45) NULL,
  `if_auto_log` TINYINT(1) NULL,
  PRIMARY KEY (`account_id`)
) ENGINE = InnoDB;
select * from account;
-- Table record_store.customer
CREATE TABLE IF NOT EXISTS `record_store`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `passw` VARCHAR(45) NULL,
  `phone_num` varchar(20) NOT NULL,
  `if_register` TINYINT(1) NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE = InnoDB;

INSERT INTO customer (first_name, last_name, email, passw, phone_num, if_register)
VALUES
    ('John', 'Doe', 'john.doe@example.com','0000', '123-456-7890', 1),
    ('Jane', 'Smith', 'jane.smith@example.com','0001', '987-654-3210', 1),
    ('Alice', 'Johnson', 'alice.johnson@example.com','0002', '555-555-5555', 1);

select * from customer;
-- Table record_store.records_detail

CREATE TABLE IF NOT EXISTS `record_store`.`records_detail` (
  `record_id` INT NOT NULL,
  `record_name` VARCHAR(45) NOT NULL,
  `artist` VARCHAR(45) NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE = InnoDB;

INSERT INTO records_detail (record_id,record_name,artist,genre)
VALUES
(1000,"2112","Rush","Rock"),
(1001,"Evol","Sonic Youth", "Punk-Rock"),
(1002,"Mothership","Led Zeppelin","Classic Rock"),
(1003,"Dark Side of the Moon","Pink Floyd","Classic Rock");

-- Table record_store.address

CREATE TABLE IF NOT EXISTS `address` (
  `customer_id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) NOT NULL,
  `address2` varchar(50),
  `city` varchar(50) NOT NULL,
  `state` varchar(25) NOT NULL,
  `postal_code` int NOT NULL,
 
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;
select * from address;
-- Table record_store.staff

CREATE TABLE IF NOT EXISTS `staff_list` (
  `staff_id` tinyint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `staff_credentials` (
  `staff_id` tinyint NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `password` varchar(40) NOT NULL,
  `email` varchar(50) NOT NULL,
  `isadmin` tinyint NOT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB;
insert into staff_credentials(username,password,email,isadmin)
Values ('admin','admin','recordstore@gmail.com', 1);
select * from staff_credentials;


CREATE TABLE IF NOT EXISTS `orders` (
`order_id` int NOT NULL,
`customer_id` int NOT NULL,
`last_name` varchar(35) NOT NULL,
`placement_date` DATE NOT NULL
)  ENGINE=InnoDB;

INSERT INTO orders (order_id,customer_id,last_name,placement_date)
VALUES 
(10,1,'Doe', '2022-01-22'),
(11,2,'Smith', '2023-02-25'),
(12,3,'Johnson', '2022-05-23'),
(13,4,'Brown', '2021-07-22');





-- Add other table definitions here...


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

