-- Active: 1708706294364@@127.0.0.1@3306

DROP DATABASE IF EXISTS record_store;
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
  `cart#` INT Default 0,
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
  `record_id` INT NOT NULL AUTO_INCREMENT,
  `record_name` VARCHAR(45) NOT NULL,
  `artist` VARCHAR(45) NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  `img_link` VARCHAR(250),  -- Assuming the link can be up to 255 characters long
  `price` decimal(10, 2), -- Added price so that we can submit this in the forms
  `quantity` INT DEFAULT 0, -- Default quantity set to 0
  PRIMARY KEY (`record_id`)
) ENGINE = InnoDB;


INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Thriller', 'Michael Jackson', 'Pop', 'https://i.redd.it/ehrrwwfwvz411.png', 20, 100);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Back in Black', 'AC/DC', 'Rock', 'https://th.bing.com/th/id/OIP.rWVw2ui1moDt_hYlbdxidwAAAA?rs=1&pid=ImgDetMain', 20, 80);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('The Dark Side of the Moon', 'Pink Floyd', 'Progressive Rock', 'https://m.media-amazon.com/images/I/31PosC6TTdL._SX300_SY300_QL70_FMwebp_.jpg', 20, 90);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Abbey Road', 'The Beatles', 'Rock', 'https://m.media-amazon.com/images/I/91VxDWK6XUL._SY355_.jpg', 20, 110);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Rumours', 'Fleetwood Mac', 'Soft Rock', 'https://faroutmagazine.co.uk/static/uploads/2020/10/The-story-behind-Fleetwood-Macs-Rumours-cover-art.jpg', 20, 85);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Led Zeppelin IV', 'Led Zeppelin', 'Hard Rock', 'https://th.bing.com/th/id/OIP.8BOmatWcTQNvA0xQvpbGxAHaHC?w=194&h=184&c=7&r=0&o=5&dpr=1.3&pid=1.7', 20, 95);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('In Utero', 'Nirvana', 'Grunge', 'https://th.bing.com/th/id/OIP.tgcgZUruhb_FQhAIMT8pjQHaHa?w=171&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7', 20, 75);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Hotel California', 'Eagles', 'Rock', 'https://pure-music.co.uk/wp-content/uploads/2019/04/Hotel-California-Album-Cover.png', 20, 105);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('The Wall', 'Pink Floyd', 'Progressive Rock', 'https://s-media-cache-ak0.pinimg.com/originals/ee/66/17/ee66179ea3111626559a4326c394bab4.jpg', 20, 100);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Sgt. Pepper''s Lonely Hearts Club Band', 'The Beatles', 'Rock', 'https://m.media-amazon.com/images/I/61vwcOLe47L._SX300_SY300_QL70_FMwebp_.jpg', 20, 100);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Born to Run', 'Bruce Springsteen', 'Rock', 'https://m.media-amazon.com/images/I/51QxoecCysL._SY300_SX300_QL70_FMwebp_.jpg', 20, 70);

INSERT INTO record_store.records_detail (record_name, artist, genre, img_link, price, quantity) 
VALUES ('Purple Rain', 'Prince', 'Pop', 'https://th.bing.com/th/id/OIP.3Q35IUHs4EaWQlGJ55bG6wAAAA?rs=1&pid=ImgDetMain', 20, 85);


-- Table record_store.record_images

CREATE TABLE IF NOT EXISTS `record_images` (
record_id int NOT NULL,
genre varchar(45),
img_file_name varchar(55) NOT NULL

);

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
USE record_store;
SELECT * FROM orders;
INSERT INTO orders (order_id,customer_id,last_name,placement_date)
VALUES 
(10,1,'Doe', '2022-01-22'),
(11,2,'Smith', '2023-02-25'),
(12,3,'Johnson', '2022-05-23'),
(13,4,'Brown', '2021-07-22'),
(14, 5, 'Jacobson', '2020-07-22');


#Sample data, delete later



CREATE TABLE IF NOT EXISTS `john.doe@example.com_cart` (
	`record_id` int NOT NULL,
    `customer_id` int NOT NULL,
    `order_id` int NOT NULL,
    `price` numeric (6,2),
    `quantity` int NOT NULL
    );


INSERT INTO `john.doe@example.com_cart` (`record_id`,`customer_id`,`order_id`,`price`,`quantity`)
VALUES 
(1, 1, 200, 19.99,2),
(4, 1, 200, 21.99,1),
(6, 1, 200, 15.99,1),
(8, 1, 200, 18.99,1),
(7, 1, 200, 17.99,1),
(9, 1, 200, 17.99,3);

SELECT img_link from records_detail
INNER JOIN `john.doe@example.com_cart` 
ON records_detail.record_id = `john.doe@example.com_cart`.record_id;

	




SELECT * FROM records_detail;




-- Add other table definitions here...


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
