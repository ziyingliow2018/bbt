DROP DATABASE IF EXISTS bubbletea;
CREATE DATABASE bubbletea;
USE bubbletea;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `pricing`;
CREATE TABLE IF NOT EXISTS `pricing` (
  `ItemID` int(11) NOT NULL auto_increment,
  `ItemName` varchar(50) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `pricing` (`ItemID`, `ItemName`, `Price`) VALUES
(1,'Green Milk Tea with pearls','3.50'),
(2,'Milk Tea with pearls','3.50'),
(3,'Black tea with herbal jelly','3.00'),
(4,'Green tea with cream','3.00');

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `OrderID` int(11) NOT NULL auto_increment,
  `Base` varchar(100) NOT NULL,
  `DateTime` TIMESTAMP,
  `Toppings` varchar(200) NOT NULL,
  `TotalPrice` decimal(10,2) NOT NULL,
  `Status` varchar(20) DEFAULT NULL,
   PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


