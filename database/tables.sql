DROP DATABASE IF EXISTS bubbletea;
CREATE DATABASE bubbletea;
USE bubbletea;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `ItemID` int(11) NOT NULL,
  `ItemName` varchar(50) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Type` varchar(10) NOT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `item` (`ItemID`, `ItemName`, `Price`,`Type`) VALUES
(1,'Green Milk Tea','3.50','base'),
(2,'Milk Tea','3.50','base'),
(3,'Black tea','3.00','base'),
(4,'Green tea','3.00','base'),
(5,'Pearls','0.50','topping'),
(6,'Herbal jelly','0.8','topping'),
(7,'tea cream','0.8','topping'),
(8,'cheese cream','3.00','topping');

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
  `OrderID` int(11) NOT NULL auto_increment,
  `Base` varchar(100) NOT NULL,
  `Toppings` varchar(200) NOT NULL,
  `TotalPrice` decimal(10,2) NOT NULL,
  `Status` varchar(20) DEFAULT NULL,
   PRIMARY KEY (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


