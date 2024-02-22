
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- Schema sakila
CREATE SCHEMA IF NOT EXISTS `sakila`;
USE `sakila`;

-- Table sakila.carts
CREATE TABLE IF NOT EXISTS `sakila`.`carts` (
  `account_id` INT NOT NULL,
  `record_id` INT NULL,
  `status` VARCHAR(45) NULL,
  `add_date` DATE NULL,
  `update_date` DATE NULL,
  PRIMARY KEY (`account_id`)
) ENGINE = InnoDB;

-- Table sakila.account
CREATE TABLE IF NOT EXISTS `sakila`.`account` (
  `account_id` INT NOT NULL,
  `account_name` VARCHAR(45) NULL,
  `customer_id` VARCHAR(45) NULL,
  `log_status` VARCHAR(45) NULL,
  `if_auto_log` TINYINT(1) NULL,
  PRIMARY KEY (`account_id`),
  CONSTRAINT `fk_account_carts1` FOREIGN KEY (`account_id`)
    REFERENCES `sakila`.`carts` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Table sakila.customer
CREATE TABLE IF NOT EXISTS `sakila`.`customer` (
  `customer_id` INT NOT NULL,
  `account_id` INT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `phone_num` VARCHAR(45) NULL,
  `address` VARCHAR(255) NULL,
  `create_date` DATE NULL,
  `update_date` DATE NULL,
  `account_account_id` INT NOT NULL,
  `if_register` TINYINT(1) NULL,
  PRIMARY KEY (`customer_id`),
  INDEX `fk_customer_account1_idx` (`account_account_id` ASC),
  CONSTRAINT `fk_customer_account1` FOREIGN KEY (`account_account_id`)
    REFERENCES `sakila`.`account` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Table sakila.records_detail
CREATE TABLE IF NOT EXISTS `sakila`.`records_detail` (
  `record_id` INT NOT NULL,
  `record_name` VARCHAR(45) NULL,
  `record_desc` VARCHAR(45) NULL,
  `feature_id_list` VARCHAR(45) NOT NULL,
  `albums_id` VARCHAR(45) NOT NULL,
  `artists_id` VARCHAR(45) NOT NULL,
  `genres_id` VARCHAR(45) NOT NULL,
  `carts_account_id` INT NOT NULL,
  PRIMARY KEY (`record_id`, `feature_id_list`, `albums_id`, `artists_id`, `genres_id`, `carts_account_id`),
  INDEX `fk_records_detail_carts1_idx` (`carts_account_id` ASC),
  CONSTRAINT `fk_records_detail_carts1` FOREIGN KEY (`carts_account_id`)
    REFERENCES `sakila`.`carts` (`account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Add other table definitions here...

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
