CREATE DATABASE IF NOT EXISTS `bubbletea` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `pricing`;
CREATE TABLE IF NOT EXISTS `pricing` (
  `ItemID` INT NOT NULL AUTO_INCREMENT,
  `ItemName` varchar(50) NOT NULL,
  `Price` double NOT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pricing`
--

INSERT INTO `pricing` (`ItemID`, `ItemName`, `Price`) VALUES
(1,'Green Milk Tea with pearls' '3.50'),
(2,'Milk Tea with pearls' '3.50'),
(3,'Black tea with herbal jelly' '3.00'),
(4,'Green tea with cream' '3.00');