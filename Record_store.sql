-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema sakila
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sakila
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sakila` ;
-- -----------------------------------------------------
-- Schema RecordStore
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema RecordStore
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `RecordStore` ;
USE `RecordStore` ;

-- -----------------------------------------------------
-- Table `RecordStore`.`cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`cart` (
  `account_id` INT NOT NULL,
  `record_id` INT NOT NULL,
  `status` VARCHAR(45) NULL,
  `add_date` DATE NULL,
  `update_date` DATE NULL,
  PRIMARY KEY (`account_id`, `record_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`account` (
  `account_ID` INT NOT NULL,
  `account_name` VARCHAR(45) NULL,
  `customer_id` VARCHAR(45) NULL,
  `log_status` VARCHAR(45) NULL,
  `if_auto_log` TINYINT(1) NULL,
  PRIMARY KEY (`account_ID`),
  INDEX `fk_account_cart1_idx` (`account_ID` ASC),
  CONSTRAINT `fk_account_cart1`
    FOREIGN KEY (`account_ID`)
    REFERENCES `RecordStore`.`cart` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`customer` (
  `customer_id` INT NOT NULL,
  `account_id` INT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `phone_num` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `create_date` DATE NULL,
  `update_date` DATE NULL,
  `if_register` TINYINT(1) NULL,
  PRIMARY KEY (`customer_id`),
  INDEX `fk_customer_account_idx` (`account_id` ASC),
  CONSTRAINT `fk_customer_account`
    FOREIGN KEY (`account_id`)
    REFERENCES `RecordStore`.`account` (`account_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`cards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`cards` (
  `card_id` INT NOT NULL,
  `card_type_id` INT NULL,
  `card_type_desc` VARCHAR(45) NULL,
  `card_num` CHAR(50) NULL,
  `cvv_num` CHAR(3) NULL,
  `expiry_date` DATE NULL,
  `add_date` DATE NULL,
  `account_id` INT NOT NULL,
  PRIMARY KEY (`card_id`),
  INDEX `fk_cards_account1_idx` (`account_id` ASC),
  CONSTRAINT `fk_cards_account1`
    FOREIGN KEY (`account_id`)
    REFERENCES `RecordStore`.`account` (`account_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`order_detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`order_detail` (
  `order_id` INT NOT NULL,
  `record_id` VARCHAR(45) NULL,
  `account_id` INT NULL,
  `order_status` VARCHAR(45) NULL,
  `original_price` VARCHAR(45) NULL,
  `deal_price` VARCHAR(45) NULL,
  `order_date` DATE NULL,
  `update_date` DATE NULL,
  `payment_type` VARCHAR(45) NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_order_detail_cart1_idx` (`account_id` ASC),
  CONSTRAINT `fk_order_detail_cart1`
    FOREIGN KEY (`account_id`)
    REFERENCES `RecordStore`.`cart` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`record_detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`record_detail` (
  `record_id` INT NOT NULL,
  `record_name` VARCHAR(45) NULL,
  `record_desc` VARCHAR(45) NULL,
  `feature_id` VARCHAR(45) NOT NULL,
  `albums_id` VARCHAR(45) NOT NULL,
  `artists_id` VARCHAR(45) NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`record_id`, `genre_id`, `artists_id`, `albums_id`, `feature_id`),
  UNIQUE INDEX `record_id_UNIQUE` (`record_id` ASC),
  CONSTRAINT `fk_record_detail_cart1`
    FOREIGN KEY (`record_id`)
    REFERENCES `RecordStore`.`cart` (`record_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`sales_statistics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`sales_statistics` (
  `date` DATE NOT NULL,
  `record_id` VARCHAR(45) NULL,
  `sales_num` VARCHAR(45) NULL,
  `feature_id` JSON NULL,
  `albums_id` VARCHAR(45) NULL,
  `artists_id` VARCHAR(45) NULL,
  `genres_id` VARCHAR(45) NULL,
  `if_top_selling` TINYINT(1) NULL,
  PRIMARY KEY (`date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`reviews` (
  `review_id` INT NOT NULL,
  `customer_id` VARCHAR(45) NULL,
  `record_id` INT NULL,
  `review_desc` TEXT NULL,
  `mark` DECIMAL(10,2) NULL,
  `review_date` DATE NULL,
  PRIMARY KEY (`review_id`),
  INDEX `fk_reviews_record_detail1_idx` (`record_id` ASC),
  CONSTRAINT `fk_reviews_record_detail1`
    FOREIGN KEY (`record_id`)
    REFERENCES `RecordStore`.`record_detail` (`record_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`features`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`features` (
  `feature_id` VARCHAR(45) NOT NULL,
  `feature_desc` VARCHAR(45) NULL,
  `create_date` DATE NULL,
  `update_date` DATE NULL,
  `if_effective` TINYINT(1) NULL,
  `delete_date` DATE NULL,
  PRIMARY KEY (`feature_id`),
  CONSTRAINT `fk_features_record_detail1`
    FOREIGN KEY (`feature_id`)
    REFERENCES `RecordStore`.`record_detail` (`feature_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`artists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`artists` (
  `artist_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL,
  `age` VARCHAR(45) NULL,
  `add_date` DATE NULL,
  PRIMARY KEY (`artist_id`),
  INDEX `fk_artists_record_detail1_idx` (`artist_id` ASC),
  CONSTRAINT `fk_artists_record_detail1`
    FOREIGN KEY (`artist_id`)
    REFERENCES `RecordStore`.`record_detail` (`artists_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`genres` (
  `genre_id` INT NOT NULL,
  `genre_name` VARCHAR(45) NULL,
  `genre_desc` TEXT NULL,
  `add_date` DATE NULL,
  PRIMARY KEY (`genre_id`),
  CONSTRAINT `fk_genres_record_detail1`
    FOREIGN KEY (`genre_id`)
    REFERENCES `RecordStore`.`record_detail` (`genre_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `RecordStore`.`albums`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `RecordStore`.`albums` (
  `album_id` VARCHAR(24) NOT NULL,
  `title` VARCHAR(45) NULL,
  `artist_id` VARCHAR(45) NULL,
  `genre_id` VARCHAR(45) NULL,
  `add_date` DATE NULL,
  PRIMARY KEY (`album_id`),
  INDEX `fk_albums_record_detail1_idx` (`album_id` ASC),
  CONSTRAINT `fk_albums_record_detail1`
    FOREIGN KEY (`album_id`)
    REFERENCES `RecordStore`.`record_detail` (`albums_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `sakila` ;

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`customer_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`customer_list` (`ID` INT, `name` INT, `address` INT, `zip code` INT, `phone` INT, `city` INT, `country` INT, `notes` INT, `SID` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`film_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`film_list` (`FID` INT, `title` INT, `description` INT, `category` INT, `price` INT, `length` INT, `rating` INT, `actors` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`nicer_but_slower_film_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`nicer_but_slower_film_list` (`FID` INT, `title` INT, `description` INT, `category` INT, `price` INT, `length` INT, `rating` INT, `actors` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`staff_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`staff_list` (`ID` INT, `name` INT, `address` INT, `zip code` INT, `phone` INT, `city` INT, `country` INT, `SID` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`sales_by_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`sales_by_store` (`store` INT, `manager` INT, `total_sales` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`sales_by_film_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`sales_by_film_category` (`category` INT, `total_sales` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sakila`.`actor_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sakila`.`actor_info` (`actor_id` INT, `first_name` INT, `last_name` INT, `film_info` INT);

-- -----------------------------------------------------
-- procedure rewards_report
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE PROCEDURE `sakila`.`rewards_report` (
    IN min_monthly_purchases TINYINT UNSIGNED
    , IN min_dollar_amount_purchased DECIMAL(10,2) UNSIGNED
    , OUT count_rewardees INT
)
LANGUAGE SQL
NOT DETERMINISTIC 
READS SQL DATA
SQL SECURITY DEFINER
COMMENT 'Provides a customizable report on best customers'
proc: BEGIN
    
    DECLARE last_month_start DATE;
    DECLARE last_month_end DATE;

    /* Some sanity checks... */
    IF min_monthly_purchases = 0 THEN
        SELECT 'Minimum monthly purchases parameter must be > 0';
        LEAVE proc;
    END IF;
    IF min_dollar_amount_purchased = 0.00 THEN
        SELECT 'Minimum monthly dollar amount purchased parameter must be > $0.00';
        LEAVE proc;
    END IF;

    /* Determine start and end time periods */
    SET last_month_start = DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH);
    SET last_month_start = STR_TO_DATE(CONCAT(YEAR(last_month_start),'-',MONTH(last_month_start),'-01'),'%Y-%m-%d');
    SET last_month_end = LAST_DAY(last_month_start);

    /* 
        Create a temporary storage area for 
        Customer IDs.  
    */
    CREATE TEMPORARY TABLE tmpCustomer (customer_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY);

    /* 
        Find all customers meeting the 
        monthly purchase requirements
    */
    INSERT INTO tmpCustomer (customer_id)
    SELECT p.customer_id 
    FROM payment AS p
    WHERE DATE(p.payment_date) BETWEEN last_month_start AND last_month_end
    GROUP BY customer_id
    HAVING SUM(p.amount) > min_dollar_amount_purchased
    AND COUNT(customer_id) > min_monthly_purchases;

    /* Populate OUT parameter with count of found customers */
    SELECT COUNT(*) FROM tmpCustomer INTO count_rewardees;

    /* 
        Output ALL customer information of matching rewardees.
        Customize output as needed.
    */
    SELECT c.* 
    FROM tmpCustomer AS t   
    INNER JOIN customer AS c ON t.customer_id = c.customer_id;

    /* Clean up */
    DROP TABLE tmpCustomer;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- function get_customer_balance
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE FUNCTION `sakila`.`get_customer_balance`(p_customer_id INT, p_effective_date DATETIME) RETURNS DECIMAL(5,2)
    DETERMINISTIC
    READS SQL DATA
BEGIN

       #OK, WE NEED TO CALCULATE THE CURRENT BALANCE GIVEN A CUSTOMER_ID AND A DATE
       #THAT WE WANT THE BALANCE TO BE EFFECTIVE FOR. THE BALANCE IS:
       #   1) RENTAL FEES FOR ALL PREVIOUS RENTALS
       #   2) ONE DOLLAR FOR EVERY DAY THE PREVIOUS RENTALS ARE OVERDUE
       #   3) IF A FILM IS MORE THAN RENTAL_DURATION * 2 OVERDUE, CHARGE THE REPLACEMENT_COST
       #   4) SUBTRACT ALL PAYMENTS MADE BEFORE THE DATE SPECIFIED

  DECLARE v_rentfees DECIMAL(5,2); #FEES PAID TO RENT THE VIDEOS INITIALLY
  DECLARE v_overfees INTEGER;      #LATE FEES FOR PRIOR RENTALS
  DECLARE v_payments DECIMAL(5,2); #SUM OF PAYMENTS MADE PREVIOUSLY

  SELECT IFNULL(SUM(film.rental_rate),0) INTO v_rentfees
    FROM film, inventory, rental
    WHERE film.film_id = inventory.film_id
      AND inventory.inventory_id = rental.inventory_id
      AND rental.rental_date <= p_effective_date
      AND rental.customer_id = p_customer_id;

  SELECT IFNULL(SUM(IF((TO_DAYS(rental.return_date) - TO_DAYS(rental.rental_date)) > film.rental_duration,
        ((TO_DAYS(rental.return_date) - TO_DAYS(rental.rental_date)) - film.rental_duration),0)),0) INTO v_overfees
    FROM rental, inventory, film
    WHERE film.film_id = inventory.film_id
      AND inventory.inventory_id = rental.inventory_id
      AND rental.rental_date <= p_effective_date
      AND rental.customer_id = p_customer_id;


  SELECT IFNULL(SUM(payment.amount),0) INTO v_payments
    FROM payment

    WHERE payment.payment_date <= p_effective_date
    AND payment.customer_id = p_customer_id;

  RETURN v_rentfees + v_overfees - v_payments;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure film_in_stock
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE PROCEDURE `sakila`.`film_in_stock`(IN p_film_id INT, IN p_store_id INT, OUT p_film_count INT)
READS SQL DATA
BEGIN
     SELECT inventory_id
     FROM inventory
     WHERE film_id = p_film_id
     AND store_id = p_store_id
     AND inventory_in_stock(inventory_id);

     SELECT FOUND_ROWS() INTO p_film_count;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure film_not_in_stock
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE PROCEDURE `sakila`.`film_not_in_stock`(IN p_film_id INT, IN p_store_id INT, OUT p_film_count INT)
READS SQL DATA
BEGIN
     SELECT inventory_id
     FROM inventory
     WHERE film_id = p_film_id
     AND store_id = p_store_id
     AND NOT inventory_in_stock(inventory_id);

     SELECT FOUND_ROWS() INTO p_film_count;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- function inventory_held_by_customer
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE FUNCTION `sakila`.`inventory_held_by_customer`(p_inventory_id INT) RETURNS INT
READS SQL DATA
BEGIN
  DECLARE v_customer_id INT;
  DECLARE EXIT HANDLER FOR NOT FOUND RETURN NULL;

  SELECT customer_id INTO v_customer_id
  FROM rental
  WHERE return_date IS NULL
  AND inventory_id = p_inventory_id;

  RETURN v_customer_id;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- function inventory_in_stock
-- -----------------------------------------------------

DELIMITER $$
USE `sakila`$$


CREATE FUNCTION `sakila`.`inventory_in_stock`(p_inventory_id INT) RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE v_rentals INT;
    DECLARE v_out     INT;

    #AN ITEM IS IN-STOCK IF THERE ARE EITHER NO ROWS IN THE rental TABLE
    #FOR THE ITEM OR ALL ROWS HAVE return_date POPULATED

    SELECT COUNT(*) INTO v_rentals
    FROM rental
    WHERE inventory_id = p_inventory_id;

    IF v_rentals = 0 THEN
      RETURN TRUE;
    END IF;

    SELECT COUNT(rental_id) INTO v_out
    FROM inventory LEFT JOIN rental USING(inventory_id)
    WHERE inventory.inventory_id = p_inventory_id
    AND rental.return_date IS NULL;

    IF v_out > 0 THEN
      RETURN FALSE;
    ELSE
      RETURN TRUE;
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `sakila`.`customer_list`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`customer_list`;
USE `sakila`;
--
-- View structure for view `customer_list`
--

CREATE  OR REPLACE VIEW customer_list 
AS 
SELECT cu.customer_id AS ID, CONCAT(cu.first_name, _utf8' ', cu.last_name) AS name, a.address AS address, a.postal_code AS `zip code`,
	a.phone AS phone, city.city AS city, country.country AS country, IF(cu.active, _utf8'active',_utf8'') AS notes, cu.store_id AS SID 
FROM customer AS cu JOIN address AS a ON cu.address_id = a.address_id JOIN city ON a.city_id = city.city_id 
	JOIN country ON city.country_id = country.country_id;

-- -----------------------------------------------------
-- View `sakila`.`film_list`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`film_list`;
USE `sakila`;
--
-- View structure for view `film_list`
--

CREATE  OR REPLACE VIEW film_list 
AS 
SELECT film.film_id AS FID, film.title AS title, film.description AS description, category.name AS category, film.rental_rate AS price,
	film.length AS length, film.rating AS rating, GROUP_CONCAT(CONCAT(actor.first_name, _utf8' ', actor.last_name) SEPARATOR ', ') AS actors 
FROM category LEFT JOIN film_category ON category.category_id = film_category.category_id LEFT JOIN film ON film_category.film_id = film.film_id
        JOIN film_actor ON film.film_id = film_actor.film_id 
	JOIN actor ON film_actor.actor_id = actor.actor_id 
GROUP BY film.film_id, category.name;

-- -----------------------------------------------------
-- View `sakila`.`nicer_but_slower_film_list`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`nicer_but_slower_film_list`;
USE `sakila`;
--
-- View structure for view `nicer_but_slower_film_list`
--

CREATE  OR REPLACE VIEW nicer_but_slower_film_list 
AS 
SELECT film.film_id AS FID, film.title AS title, film.description AS description, category.name AS category, film.rental_rate AS price, 
	film.length AS length, film.rating AS rating, GROUP_CONCAT(CONCAT(CONCAT(UCASE(SUBSTR(actor.first_name,1,1)),
	LCASE(SUBSTR(actor.first_name,2,LENGTH(actor.first_name))),_utf8' ',CONCAT(UCASE(SUBSTR(actor.last_name,1,1)),
	LCASE(SUBSTR(actor.last_name,2,LENGTH(actor.last_name)))))) SEPARATOR ', ') AS actors 
FROM category LEFT JOIN film_category ON category.category_id = film_category.category_id LEFT JOIN film ON film_category.film_id = film.film_id
        JOIN film_actor ON film.film_id = film_actor.film_id
	JOIN actor ON film_actor.actor_id = actor.actor_id 
GROUP BY film.film_id, category.name;

-- -----------------------------------------------------
-- View `sakila`.`staff_list`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`staff_list`;
USE `sakila`;
--
-- View structure for view `staff_list`
--

CREATE  OR REPLACE VIEW staff_list 
AS 
SELECT s.staff_id AS ID, CONCAT(s.first_name, _utf8' ', s.last_name) AS name, a.address AS address, a.postal_code AS `zip code`, a.phone AS phone,
	city.city AS city, country.country AS country, s.store_id AS SID 
FROM staff AS s JOIN address AS a ON s.address_id = a.address_id JOIN city ON a.city_id = city.city_id 
	JOIN country ON city.country_id = country.country_id;

-- -----------------------------------------------------
-- View `sakila`.`sales_by_store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`sales_by_store`;
USE `sakila`;
--
-- View structure for view `sales_by_store`
--

CREATE  OR REPLACE VIEW sales_by_store
AS 
SELECT 
CONCAT(c.city, _utf8',', cy.country) AS store
, CONCAT(m.first_name, _utf8' ', m.last_name) AS manager
, SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN store AS s ON i.store_id = s.store_id
INNER JOIN address AS a ON s.address_id = a.address_id
INNER JOIN city AS c ON a.city_id = c.city_id
INNER JOIN country AS cy ON c.country_id = cy.country_id
INNER JOIN staff AS m ON s.manager_staff_id = m.staff_id
GROUP BY s.store_id
ORDER BY cy.country, c.city;

-- -----------------------------------------------------
-- View `sakila`.`sales_by_film_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`sales_by_film_category`;
USE `sakila`;
--
-- View structure for view `sales_by_film_category`
--
-- Note that total sales will add up to >100% because
-- some titles belong to more than 1 category
--

CREATE  OR REPLACE VIEW sales_by_film_category
AS 
SELECT 
c.name AS category
, SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN film AS f ON i.film_id = f.film_id
INNER JOIN film_category AS fc ON f.film_id = fc.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY total_sales DESC;

-- -----------------------------------------------------
-- View `sakila`.`actor_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sakila`.`actor_info`;
USE `sakila`;
--
-- View structure for view `actor_info`
--

CREATE  OR REPLACE DEFINER=CURRENT_USER SQL SECURITY INVOKER VIEW actor_info 
AS
SELECT      
a.actor_id,
a.first_name,
a.last_name,
GROUP_CONCAT(DISTINCT CONCAT(c.name, ': ',
		(SELECT GROUP_CONCAT(f.title ORDER BY f.title SEPARATOR ', ')
                    FROM sakila.film f
                    INNER JOIN sakila.film_category fc
                      ON f.film_id = fc.film_id
                    INNER JOIN sakila.film_actor fa
                      ON f.film_id = fa.film_id
                    WHERE fc.category_id = c.category_id
                    AND fa.actor_id = a.actor_id
                 )
             )
             ORDER BY c.name SEPARATOR '; ')
AS film_info
FROM sakila.actor a
LEFT JOIN sakila.film_actor fa
  ON a.actor_id = fa.actor_id
LEFT JOIN sakila.film_category fc
  ON fa.film_id = fc.film_id
LEFT JOIN sakila.category c
  ON fc.category_id = c.category_id
GROUP BY a.actor_id, a.first_name, a.last_name;
USE `sakila`;

DELIMITER $$
USE `sakila`$$

CREATE TRIGGER `ins_film` AFTER INSERT ON `film` FOR EACH ROW BEGIN
    INSERT INTO film_text (film_id, title, description)
        VALUES (new.film_id, new.title, new.description);
  END$$

USE `sakila`$$

CREATE TRIGGER `upd_film` AFTER UPDATE ON `film` FOR EACH ROW BEGIN
    IF (old.title != new.title) or (old.description != new.description)
    THEN
        UPDATE film_text
            SET title=new.title,
                description=new.description,
                film_id=new.film_id
        WHERE film_id=old.film_id;
    END IF;
  END$$

USE `sakila`$$

CREATE TRIGGER `del_film` AFTER DELETE ON `film` FOR EACH ROW BEGIN
    DELETE FROM film_text WHERE film_id = old.film_id;
  END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
