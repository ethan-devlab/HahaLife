-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: shopping
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ADDED_TO`
--

DROP TABLE IF EXISTS `ADDED_TO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ADDED_TO` (
  `CartID` char(10) NOT NULL,
  `PID` char(10) NOT NULL,
  PRIMARY KEY (`CartID`,`PID`),
  KEY `PID` (`PID`),
  CONSTRAINT `added_to_ibfk_1` FOREIGN KEY (`CartID`, `PID`) REFERENCES `SHOPPINGCART` (`CartID`, `PID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `added_to_ibfk_2` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ADDED_TO`
--

LOCK TABLES `ADDED_TO` WRITE;
/*!40000 ALTER TABLE `ADDED_TO` DISABLE KEYS */;
INSERT INTO `ADDED_TO` VALUES ('CART00001','P000000001'),('CART00008','P000000001'),('CART00002','P000000004'),('CART00003','P000000007'),('CART00004','P000000010');
/*!40000 ALTER TABLE `ADDED_TO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ADMIN`
--

DROP TABLE IF EXISTS `ADMIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ADMIN` (
  `UID` char(10) NOT NULL,
  `UName` varchar(15) NOT NULL,
  `AccStatus` varchar(10) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `PhoneNumber` char(10) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `L_Login` datetime DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ADMIN`
--

LOCK TABLES `ADMIN` WRITE;
/*!40000 ALTER TABLE `ADMIN` DISABLE KEYS */;
INSERT INTO `ADMIN` VALUES ('A000000001','Evelyn Tsai','Active','admin888','No. 101, Guangfu Rd., East Dist., Hsinchu City 300','0900123456','evelyn@example.com','2025-05-20 13:24:44'),('A000000002','George Kuo','Active','gk888888','No. 200, Jinshan Rd., Zhonghe Dist., New Taipei City 235','0977333444','george@example.com','2025-04-11 08:00:00');
/*!40000 ALTER TABLE `ADMIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `APPLICANT`
--

DROP TABLE IF EXISTS `APPLICANT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPLICANT` (
  `AppID` char(10) NOT NULL,
  `SID` char(10) DEFAULT NULL,
  `Status` varchar(15) NOT NULL,
  `Name` varchar(15) NOT NULL,
  `Email` varchar(25) DEFAULT NULL,
  `PhoneNumber` char(10) DEFAULT NULL,
  `AppDate` date NOT NULL,
  `RevComment` varchar(100) DEFAULT NULL,
  `AID` char(10) DEFAULT NULL,
  `Password` varchar(100) NOT NULL,
  PRIMARY KEY (`AppID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `PhoneNumber` (`PhoneNumber`),
  KEY `SID` (`SID`),
  KEY `AID` (`AID`),
  CONSTRAINT `applicant_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `SELLER` (`UID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `applicant_ibfk_2` FOREIGN KEY (`AID`) REFERENCES `ADMIN` (`UID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPLICANT`
--

LOCK TABLES `APPLICANT` WRITE;
/*!40000 ALTER TABLE `APPLICANT` DISABLE KEYS */;
INSERT INTO `APPLICANT` VALUES ('APP0000001',NULL,'Disapproved','Frank Yeh','frank@example.com','0977000111','2025-04-01','Incomplete documents.','A000000001','frank888'),('APP0000002',NULL,'Approved','Grace Liu','grace@example.com','0955777999','2025-04-05','Approved with conditions.','A000000002','grace123'),('APP0000003',NULL,'Pending','tester1','tester1@example.com','','2025-05-18',NULL,NULL,'Abcd@1111'),('APP0000004',NULL,'Pending','汪辰諺','d12345678@gmail.com','1234567890','2025-05-20',NULL,NULL,'Aa@12345678'),('APP0000005',NULL,'Pending','Kenny Wang','timhuang0513@gmail.com','0902077700','2025-05-20',NULL,NULL,'KKWang_0304');
/*!40000 ALTER TABLE `APPLICANT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CREATE`
--

DROP TABLE IF EXISTS `CREATE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CREATE` (
  `ShipID` char(10) NOT NULL,
  `OID` char(10) NOT NULL,
  `UptTime` datetime NOT NULL,
  `ShipStatus` varchar(15) NOT NULL,
  `TrackNumber` char(17) NOT NULL,
  `Courier` varchar(30) NOT NULL,
  PRIMARY KEY (`ShipID`),
  UNIQUE KEY `TrackNumber` (`TrackNumber`),
  KEY `OID` (`OID`),
  CONSTRAINT `create_ibfk_1` FOREIGN KEY (`OID`) REFERENCES `ORDER` (`OID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CREATE`
--

LOCK TABLES `CREATE` WRITE;
/*!40000 ALTER TABLE `CREATE` DISABLE KEYS */;
INSERT INTO `CREATE` VALUES ('SHIP000001','O000000001','2025-04-11 15:30:00','Delivered','T1234567890123456','Black Cat Delivery'),('SHIP000002','O000000002','2025-04-12 16:00:00','In Transit','T9876543210987654','HCT Logistics'),('SHIP000003','O000000003','2025-04-13 18:45:00','Delivered','T8888888888888888','FamilyMart Logistics'),('SHIP000004','O000000005','2025-04-16 14:45:00','Delivered','T2025041612345678','T-Cat'),('SHIP104725','O341104725','2025-05-20 18:07:44','Preparing','T4958757651465641','express'),('SHIP232765','O167232765','2025-05-20 18:07:21','Preparing','T9463866777574719','express'),('SHIP266859','O922266859','2025-05-20 17:37:18','Preparing','T9685928265510886','express'),('SHIP473884','O681473884','2025-05-20 17:38:05','Preparing','T5176961169582092','express'),('SHIP570985','O792570985','2025-05-20 17:27:36','Preparing','T4389415467313010','express'),('SHIP671303','O633671303','2025-05-16 23:33:09','In Transit','T3449281457791404','Family Mart'),('SHIP795833','O386795833','2025-05-20 17:27:36','Preparing','T8356426988403020','express'),('SHIP797063','O852797063','2025-05-20 17:27:36','Preparing','T9939702495025905','express'),('SHIP891530','O212891530','2025-05-20 17:27:36','Preparing','T2932194288772416','express');
/*!40000 ALTER TABLE `CREATE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GUEST`
--

DROP TABLE IF EXISTS `GUEST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GUEST` (
  `UID` char(10) NOT NULL,
  `UName` varchar(15) DEFAULT NULL,
  `AccStatus` varchar(10) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `PhoneNumber` char(10) DEFAULT NULL,
  `Email` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GUEST`
--

LOCK TABLES `GUEST` WRITE;
/*!40000 ALTER TABLE `GUEST` DISABLE KEYS */;
INSERT INTO `GUEST` VALUES ('G000000001',NULL,NULL,NULL,NULL,NULL,NULL),('G000000002',NULL,NULL,NULL,NULL,NULL,NULL),('G000000003',NULL,NULL,NULL,NULL,NULL,NULL),('G178242984','G20250520171758',NULL,NULL,NULL,NULL,NULL),('G334101093','Guest1747560716',NULL,NULL,NULL,NULL,NULL),('G363099210','G20250520171359',NULL,NULL,NULL,NULL,NULL),('G368399322','Guest1747560714',NULL,NULL,NULL,NULL,NULL),('G392556017','G20250520171744',NULL,NULL,NULL,NULL,NULL),('G671731389','G20250518173606',NULL,NULL,NULL,NULL,NULL),('G888554900','G20250520171845',NULL,NULL,NULL,NULL,NULL),('G949722903','G20250521174329',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `GUEST` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HAS_PROMO`
--

DROP TABLE IF EXISTS `HAS_PROMO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HAS_PROMO` (
  `PromoCode` varchar(6) NOT NULL,
  `PID` char(10) NOT NULL,
  PRIMARY KEY (`PromoCode`,`PID`),
  KEY `PID` (`PID`),
  CONSTRAINT `has_promo_ibfk_1` FOREIGN KEY (`PromoCode`) REFERENCES `PROMOTION` (`PromoCode`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `has_promo_ibfk_2` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HAS_PROMO`
--

LOCK TABLES `HAS_PROMO` WRITE;
/*!40000 ALTER TABLE `HAS_PROMO` DISABLE KEYS */;
INSERT INTO `HAS_PROMO` VALUES ('PC1001','P000000001'),('PC1002','P000000002'),('PC2002','P000000003'),('PC1002','P000000005'),('PC2001','P000000009'),('PC1003','P000000010');
/*!40000 ALTER TABLE `HAS_PROMO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEMBER`
--

DROP TABLE IF EXISTS `MEMBER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MEMBER` (
  `UID` char(10) NOT NULL,
  `UName` varchar(15) NOT NULL,
  `AccStatus` varchar(10) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `PhoneNumber` char(10) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `BDate` date DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `MLevel` int DEFAULT '1',
  PRIMARY KEY (`UID`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `PhoneNumber` (`PhoneNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEMBER`
--

LOCK TABLES `MEMBER` WRITE;
/*!40000 ALTER TABLE `MEMBER` DISABLE KEYS */;
INSERT INTO `MEMBER` VALUES ('M000000001','Alice Chen','Active','pass1234','No. 12, Sec. 1, Zhongxiao E. Rd., Zhongzheng Dist., Taipei City 100','0912345678','alice@example.com','2000-01-10','Female',5),('M000000002','Brian Hsu','Frozen','br!@456','No. 88, Lane 99, Minsheng Rd., Banqiao Dist., New Taipei City 220','0922333444','brian@example.com','2000-02-11','Male',3),('M000000003','Clara Huang','Inactive','clara789','No. 7, Sec. 2, Wenxin Rd., Xitun Dist., Taichung City 407','0988776655','clara@example.com','1998-03-03','Female',1),('M000000004','Daniel Ko','Active','danko123','No. 9, Wenhua Rd., Taoyuan Dist., Taoyuan City 330','0911222333','daniel@example.com','2003-05-10','Male',6),('M000000005','Emily Lin','Frozen','emilin789','No. 21, Zhongshan Rd., Hualien City 970','0921122334','emily@example.com','1995-07-03','Female',2),('M000000006','Irene Wang','Active','irene_pw','No. 168, Sec. 2, Zhonghua Rd., East Dist., Hsinchu City 300','0911122334','irene@example.com','2002-10-10','Female',6),('M000000007','Jacky Chen','Active','jacky_pw','No. 25, Chengde Rd., Datong Dist., Taipei City 103','0922567890','jacky@example.com','1999-12-25','Male',4),('M000000008','Jerry Wu','Active','Jerry_Wu1','87 ,Yizhong St., North Dist., Taichung City',NULL,'jerry_wu@gmail.com','2005-07-28','Other',1),('M000000009','D1225651','Active','Aa@12345678','台中市西屯區文華路',NULL,'d12345678@gmail.com','2005-01-01','Male',1);
/*!40000 ALTER TABLE `MEMBER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `NOTIFICATION`
--

DROP TABLE IF EXISTS `NOTIFICATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `NOTIFICATION` (
  `NID` char(10) NOT NULL,
  `MID` char(10) NOT NULL,
  `OID` char(10) DEFAULT NULL,
  `Message` text NOT NULL,
  `NotifyTime` datetime NOT NULL,
  `IsRead` tinyint(1) NOT NULL,
  PRIMARY KEY (`NID`),
  KEY `MID` (`MID`),
  KEY `OID` (`OID`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`MID`) REFERENCES `MEMBER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `notification_ibfk_2` FOREIGN KEY (`OID`) REFERENCES `ORDER` (`OID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `NOTIFICATION`
--

LOCK TABLES `NOTIFICATION` WRITE;
/*!40000 ALTER TABLE `NOTIFICATION` DISABLE KEYS */;
INSERT INTO `NOTIFICATION` VALUES ('N000000001','M000000001','O000000001','Your order O000000001 has been shipped.','2025-04-11 15:45:00',1),('N000000002','M000000002','O000000002','Your order O000000002 is now processing.','2025-04-12 09:00:00',0),('N000000003','M000000004','O000000003','Good news! Your order O000000003 has been delivered.','2025-04-13 19:00:00',1),('N000000004','M000000006','O000000006','Payment received for order O000000006. Thank you!','2025-04-16 10:00:00',1),('N000000005','M000000007',NULL,'Don’t miss our weekend flash sale—up to 50% off selected items!','2025-04-18 08:00:00',0),('N303001105','M000000001','O633671303','Your order O633671303 is now in transit. Tracking number: T3449281457791404.','2025-05-18 15:29:16',0),('N303001659','M000000001','O633671303','Your order O633671303 has been shipped.','2025-05-18 15:29:16',0),('N303001824','M000000001','O633671303','Payment for order O633671303 has been completed. Thank you!','2025-05-17 01:56:45',1);
/*!40000 ALTER TABLE `NOTIFICATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDER`
--

DROP TABLE IF EXISTS `ORDER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDER` (
  `OID` char(10) NOT NULL,
  `OStatus` varchar(10) NOT NULL,
  `SID` char(10) DEFAULT NULL,
  `Address` varchar(100) NOT NULL,
  `TotalAmount` decimal(7,2) NOT NULL,
  `MID` char(10) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL,
  PRIMARY KEY (`OID`),
  KEY `SID` (`SID`),
  KEY `MID` (`MID`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `SELLER` (`UID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`MID`) REFERENCES `MEMBER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDER`
--

LOCK TABLES `ORDER` WRITE;
/*!40000 ALTER TABLE `ORDER` DISABLE KEYS */;
INSERT INTO `ORDER` VALUES ('O000000001','Shipped','S000000001','No. 3, Fuxing S. Rd., Da’an Dist., Taipei City 106',2498.99,'M000000001','2025-04-10 10:00:00'),('O000000002','Processing','S000000003','No. 77, Sec. 1, Wenhua Rd., East Dist., Tainan City 701',2298.50,'M000000002','2025-04-11 08:30:00'),('O000000003','Delivered','S000000004','No. 77, Sec. 2, Heping Rd., Dali Dist., Taichung City 412',1098.00,'M000000004','2025-04-12 16:00:00'),('O000000004','Cancelled','S000000001','No. 15, Lane 120, Chengde Rd., Datong Dist., Taipei City 103',99.00,'M000000005','2025-04-13 11:00:00'),('O000000005','Delivered','S000000005','No. 3, Minsheng E. Rd., Xinyi Dist., Taipei City 110',5990.00,'M000000007','2025-04-15 13:00:00'),('O000000006','Processing','S000000004','No. 5, Guangfu S. Rd., Da’an Dist., Taipei City 106',1749.00,'M000000006','2025-04-16 08:00:00'),('O167232765','Processing','S000000001','407台中市西屯區文華路100號',5999.97,'M000000009','2025-05-20 18:07:21'),('O212891530','Processing','S000000003','407台中市西屯區文華路100號',2298.50,'M000000009','2025-05-20 17:27:36'),('O341104725','Processing','S000000001','407台中市西屯區文華路100號',998.00,'M000000001','2025-05-20 18:07:44'),('O386795833','Processing','S000000005','407台中市西屯區文華路100號',5990.00,'M000000009','2025-05-20 17:27:36'),('O633671303','Shipped','S000000001','407台中市西屯區文華路100號',2198.99,'M000000001','2025-05-16 23:33:09'),('O681473884','Processing','S000000003','407台中市西屯區文華路100號',26085.50,'M000000009','2025-05-20 17:38:05'),('O792570985','Processing','S000000001','407台中市西屯區文華路100號',2697.99,'M000000009','2025-05-20 17:27:36'),('O852797063','Processing','S000000004','407台中市西屯區文華路100號',2847.00,'M000000009','2025-05-20 17:27:36'),('O922266859','Processing','S000000003','407台中市西屯區文華路100號',899.50,'M000000009','2025-05-20 17:37:18'),('O925369752','Processing','S000000001','407台中市西屯區文華路100號',2198.99,'M000000001','2025-05-16 23:02:49');
/*!40000 ALTER TABLE `ORDER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDER_DETAIL`
--

DROP TABLE IF EXISTS `ORDER_DETAIL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDER_DETAIL` (
  `OID` char(10) NOT NULL,
  `PID` char(10) NOT NULL,
  `Quantity` int NOT NULL,
  `UPrice` decimal(6,2) NOT NULL,
  `Subtotal` decimal(7,2) NOT NULL,
  PRIMARY KEY (`OID`,`PID`),
  KEY `PID` (`PID`),
  CONSTRAINT `order_detail_ibfk_1` FOREIGN KEY (`OID`) REFERENCES `ORDER` (`OID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_detail_ibfk_2` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDER_DETAIL`
--

LOCK TABLES `ORDER_DETAIL` WRITE;
/*!40000 ALTER TABLE `ORDER_DETAIL` DISABLE KEYS */;
INSERT INTO `ORDER_DETAIL` VALUES ('O000000001','P000000001',1,1999.99,1999.99),('O000000001','P000000002',1,499.00,499.00),('O000000002','P000000003',2,899.50,1799.00),('O000000002','P000000004',1,1399.00,1399.00),('O000000003','P000000005',1,799.00,799.00),('O000000003','P000000006',1,299.00,299.00),('O000000004','P000000007',1,99.00,99.00),('O000000005','P000000009',1,5990.00,5990.00),('O000000006','P000000008',1,1299.00,1299.00),('O000000006','P000000010',1,450.00,450.00),('O167232765','P000000001',3,1999.99,5999.97),('O212891530','P000000003',1,899.50,899.50),('O212891530','P000000004',1,1399.00,1399.00),('O341104725','P000000002',2,499.00,998.00),('O386795833','P000000009',1,5990.00,5990.00),('O633671303','P000000001',1,1999.99,1899.99),('O633671303','P000000002',1,499.00,299.00),('O681473884','P000000003',29,899.50,26085.50),('O792570985','P000000001',1,1999.99,1999.99),('O792570985','P000000002',1,499.00,499.00),('O792570985','P000000007',1,99.00,99.00),('O792570985','P000000011',1,100.00,100.00),('O852797063','P000000005',1,799.00,799.00),('O852797063','P000000006',1,299.00,299.00),('O852797063','P000000008',1,1299.00,1299.00),('O852797063','P000000010',1,450.00,450.00),('O922266859','P000000003',1,899.50,899.50);
/*!40000 ALTER TABLE `ORDER_DETAIL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDERHISTORY`
--

DROP TABLE IF EXISTS `ORDERHISTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDERHISTORY` (
  `OHID` char(10) NOT NULL,
  `OID` char(10) NOT NULL,
  `MID` char(10) DEFAULT NULL,
  `OrderDate` datetime NOT NULL,
  `TotalAmount` decimal(7,2) NOT NULL,
  `OStatus` varchar(10) NOT NULL,
  `PayMethod` varchar(20) NOT NULL,
  PRIMARY KEY (`OHID`),
  KEY `MID` (`MID`),
  CONSTRAINT `orderhistory_ibfk_1` FOREIGN KEY (`MID`) REFERENCES `MEMBER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDERHISTORY`
--

LOCK TABLES `ORDERHISTORY` WRITE;
/*!40000 ALTER TABLE `ORDERHISTORY` DISABLE KEYS */;
INSERT INTO `ORDERHISTORY` VALUES ('OH00000001','O000000001','M000000001','2025-04-10 10:00:00',2498.99,'Shipped','Credit Card'),('OH00000002','O000000002','M000000002','2025-04-11 08:30:00',2298.50,'Processing','Bank Transfer'),('OH00000003','O000000003','M000000004','2025-04-12 16:00:00',1098.00,'Delivered','Cash On Delivery'),('OH00000004','O000000004','M000000005','2025-04-13 11:00:00',99.00,'Cancelled','Bank Transfer'),('OH00000005','O000000005','M000000007','2025-04-15 13:00:00',5990.00,'Delivered','Credit Card'),('OH00000006','O000000006','M000000006','2025-04-16 08:00:00',1749.00,'Processing','Credit Card'),('OH01671303','O633671303','M000000001','2025-05-16 23:33:09',2198.99,'Processing','ATM Transfer');
/*!40000 ALTER TABLE `ORDERHISTORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PAID_BY`
--

DROP TABLE IF EXISTS `PAID_BY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PAID_BY` (
  `PayID` char(10) NOT NULL,
  `OID` char(10) NOT NULL,
  `PayMethod` varchar(20) NOT NULL,
  `PayStatus` varchar(15) NOT NULL,
  PRIMARY KEY (`PayID`),
  KEY `OID` (`OID`),
  CONSTRAINT `paid_by_ibfk_1` FOREIGN KEY (`OID`) REFERENCES `ORDER` (`OID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PAID_BY`
--

LOCK TABLES `PAID_BY` WRITE;
/*!40000 ALTER TABLE `PAID_BY` DISABLE KEYS */;
INSERT INTO `PAID_BY` VALUES ('PAY000001','O000000001','Credit Card','Completed'),('PAY000002','O000000002','Bank Transfer','Pending'),('PAY000003','O000000003','Line Pay','Completed'),('PAY000004','O000000005','Credit Card','Completed'),('PAY104725','O341104725','MasterCard','Pending'),('PAY232765','O167232765','Cash On Delivery','Pending'),('PAY266859','O922266859','Cash On Delivery','Pending'),('PAY473884','O681473884','Cash On Delivery','Pending'),('PAY570985','O792570985','Cash On Delivery','Pending'),('PAY671303','O633671303','ATM Transfer','Completed'),('PAY795833','O386795833','Cash On Delivery','Pending'),('PAY797063','O852797063','Cash On Delivery','Pending'),('PAY891530','O212891530','Cash On Delivery','Pending');
/*!40000 ALTER TABLE `PAID_BY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `PID` char(10) NOT NULL,
  `Category` varchar(12) NOT NULL,
  `Price` decimal(6,2) NOT NULL,
  `PName` varchar(30) NOT NULL,
  `Descript` varchar(100) NOT NULL,
  `Stock` int NOT NULL,
  `SID` char(10) DEFAULT NULL,
  `ImagePath` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`PID`),
  KEY `SID` (`SID`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `SELLER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `product_chk_1` CHECK ((`Stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('P000000001','Electronics',1999.99,'Wireless Earbuds','A wireless earbuds from popular brand.',45,'S000000001','media/product_image/wireless_earbuds.jpg'),('P000000002','Books',499.00,'AI Revolution','A masterpiece of Kenny Wang',16,'S000000001','media/product_image/IMG_0303.jpeg'),('P000000003','Beauty',899.50,'Face Serum','Make your face like a new face',5,'S000000003','media/product_image/IMG_0305.jpeg'),('P000000004','Kitchen',1399.00,'Blender 9000','A powerful blender since 1950',9,'S000000003','media/product_image/IMG_0306.jpeg'),('P000000005','Clothing',799.00,'Denim Jacket','Trendy denim jacket with unisex design',24,'S000000004','media/product_image/IMG_0307.jpeg'),('P000000006','Toys',299.00,'RC Car','Remote control off-road buggy',39,'S000000004','media/product_image/IMG_0308.webp'),('P000000007','Food',99.00,'Instant Noodles 5-pack','Classic Taiwanese flavor',99,'S000000001','media/product_image/IMG_0304.jpeg'),('P000000008','Beauty',1299.00,'Aloe Soothing Gel','Soothes and hydrates skin, 300ml',39,'S000000004','media/product_image/IMG_0309.jpeg'),('P000000009','Electronics',5990.00,'Wireless Keyboard','Mechanical keyboard with RGB lighting',19,'S000000005','media/product_image/WirelessKeyboard.jpg'),('P000000010','Books',450.00,'The Art of SQL','A practical guide to database performance tuning',49,'S000000004','media/product_image/IMG_0310.jpeg'),('P000000011','test',100.00,'test','',99,'S000000001','media/product_image/Humaaans - Research.png');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCT_TAG`
--

DROP TABLE IF EXISTS `PRODUCT_TAG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUCT_TAG` (
  `Tag` varchar(10) NOT NULL,
  `PID` char(10) NOT NULL,
  PRIMARY KEY (`Tag`,`PID`),
  KEY `PID` (`PID`),
  CONSTRAINT `product_tag_ibfk_1` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCT_TAG`
--

LOCK TABLES `PRODUCT_TAG` WRITE;
/*!40000 ALTER TABLE `PRODUCT_TAG` DISABLE KEYS */;
INSERT INTO `PRODUCT_TAG` VALUES ('Gadgets','P000000001'),('Tech','P000000001'),('Education','P000000002'),('Skincare','P000000003'),('Home','P000000004'),('Fashion','P000000005'),('Fun','P000000006'),('Snack','P000000007'),('Skincare','P000000008'),('Gadgets','P000000009'),('Education','P000000010');
/*!40000 ALTER TABLE `PRODUCT_TAG` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PROMOTION`
--

DROP TABLE IF EXISTS `PROMOTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PROMOTION` (
  `PromoCode` varchar(6) NOT NULL,
  `DisAmount` int NOT NULL,
  `SID` char(10) DEFAULT NULL,
  PRIMARY KEY (`PromoCode`),
  KEY `SID` (`SID`),
  CONSTRAINT `promotion_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `SELLER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PROMOTION`
--

LOCK TABLES `PROMOTION` WRITE;
/*!40000 ALTER TABLE `PROMOTION` DISABLE KEYS */;
INSERT INTO `PROMOTION` VALUES ('cat100',102,'S000000001'),('PC1001',100,NULL),('PC1002',200,NULL),('PC1003',50,NULL),('PC2001',150,NULL),('PC2002',100,NULL);
/*!40000 ALTER TABLE `PROMOTION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REVIEW`
--

DROP TABLE IF EXISTS `REVIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REVIEW` (
  `RevID` char(10) NOT NULL,
  `PID` char(10) NOT NULL,
  `Sell_R` varchar(100) DEFAULT NULL,
  `Buy_R` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`RevID`),
  KEY `PID` (`PID`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REVIEW`
--

LOCK TABLES `REVIEW` WRITE;
/*!40000 ALTER TABLE `REVIEW` DISABLE KEYS */;
INSERT INTO `REVIEW` VALUES ('R000000001','P000000001','Great product!','Fast delivery.'),('R000000002','P000000003','Nice texture!',NULL),('R000000003','P000000005','Stylish and warm!','Delivered earlier than expected.'),('R000000004','P000000006','My kids love it!','Battery life is decent.'),('R000000005','P000000009','Responsive keys, great for gaming','Happy with the quick delivery'),('R000000006','P000000010','Clear explanations of complex topics','Highly recommend to SQL learners'),('R71303001','P000000001','No review yet.',NULL);
/*!40000 ALTER TABLE `REVIEW` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SELLER`
--

DROP TABLE IF EXISTS `SELLER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SELLER` (
  `UID` char(10) NOT NULL,
  `UName` varchar(15) NOT NULL,
  `AccStatus` varchar(10) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `PhoneNumber` char(10) DEFAULT NULL,
  `Email` varchar(25) NOT NULL,
  `SName` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`UID`),
  UNIQUE KEY `PhoneNumber` (`PhoneNumber`),
  UNIQUE KEY `SName` (`SName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SELLER`
--

LOCK TABLES `SELLER` WRITE;
/*!40000 ALTER TABLE `SELLER` DISABLE KEYS */;
INSERT INTO `SELLER` VALUES ('S000000001','Cathy Wu','Active','cat7890','No. 56, Sec. 3, Minquan E. Rd., Songshan Dist., Taipei City 105','0933111222','cathy@example.com','CathyShop'),('S000000002','David Lin','Inactive','dl!@678','No. 120, Zhonghua Rd., Gushan Dist., Kaohsiung City 804','0955667788','david@example.com','DavidMart'),('S000000003','Emma Chang','Active','emma888','No. 32, Yongkang St., East Dist., Tainan City 701','0911555777','emma@example.com','EmmaStore'),('S000000004','Felix Sun','Active','sunny456','No. 16, Guolian 5th Rd., Hualien City 970','0933344556','felix@example.com','FelixGoods'),('S000000005','Tony Chou','Active','tony_pw','No. 88, Zhongshan Rd., Banqiao Dist., New Taipei City 220','0938765432','tony@example.com','TonyTech');
/*!40000 ALTER TABLE `SELLER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SHOPPINGCART`
--

DROP TABLE IF EXISTS `SHOPPINGCART`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SHOPPINGCART` (
  `CartID` char(10) NOT NULL,
  `PID` char(10) NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`CartID`,`PID`),
  KEY `PID` (`PID`),
  CONSTRAINT `shoppingcart_ibfk_1` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SHOPPINGCART`
--

LOCK TABLES `SHOPPINGCART` WRITE;
/*!40000 ALTER TABLE `SHOPPINGCART` DISABLE KEYS */;
INSERT INTO `SHOPPINGCART` VALUES ('CART00001','P000000001',1),('CART00002','P000000004',2),('CART00003','P000000007',3),('CART00004','P000000010',1),('CART00008','P000000001',49);
/*!40000 ALTER TABLE `SHOPPINGCART` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SOLDHISTORY`
--

DROP TABLE IF EXISTS `SOLDHISTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SOLDHISTORY` (
  `SHID` char(10) NOT NULL,
  `OID` char(10) NOT NULL,
  `SID` char(10) NOT NULL,
  `PromoCode` varchar(50) DEFAULT NULL,
  `PayMethod` varchar(20) NOT NULL,
  `SDate` datetime NOT NULL,
  `TotalPrice` decimal(7,2) NOT NULL,
  `BID` char(10) NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`SHID`),
  KEY `SID` (`SID`),
  CONSTRAINT `soldhistory_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `SELLER` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SOLDHISTORY`
--

LOCK TABLES `SOLDHISTORY` WRITE;
/*!40000 ALTER TABLE `SOLDHISTORY` DISABLE KEYS */;
INSERT INTO `SOLDHISTORY` VALUES ('SH00000001','O000000001','S000000001','PC1001','Credit Card','2025-04-10 10:00:00',2498.99,'M000000001',2),('SH00000002','O000000002','S000000003',NULL,'Bank Transfer','2025-04-11 08:30:00',2298.50,'M000000002',3),('SH00000003','O000000003','S000000004','PC1002','Cash On Delivery','2025-04-12 16:00:00',1098.00,'M000000004',2),('SH00000004','O000000004','S000000001',NULL,'Bank Transfer','2025-04-13 11:00:00',99.00,'M000000005',1),('SH00000005','O000000005','S000000005','PC2001','Credit Card','2025-04-15 13:00:00',5990.00,'M000000007',1),('SH00000006','O000000006','S000000004',NULL,'Credit Card','2025-04-16 08:00:00',1749.00,'M000000006',2),('SH01671303','O633671303','S000000001','PC1001,PC1002','ATM Transfer','2025-05-16 23:33:09',2198.99,'M000000001',2);
/*!40000 ALTER TABLE `SOLDHISTORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USE_PROMO`
--

DROP TABLE IF EXISTS `USE_PROMO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USE_PROMO` (
  `PromoCode` varchar(6) NOT NULL,
  `OID` char(10) NOT NULL,
  `PID` char(10) NOT NULL,
  PRIMARY KEY (`PromoCode`,`OID`,`PID`),
  KEY `OID` (`OID`),
  KEY `PID` (`PID`),
  CONSTRAINT `use_promo_ibfk_1` FOREIGN KEY (`PromoCode`) REFERENCES `PROMOTION` (`PromoCode`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `use_promo_ibfk_2` FOREIGN KEY (`OID`) REFERENCES `ORDER` (`OID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `use_promo_ibfk_3` FOREIGN KEY (`PID`) REFERENCES `PRODUCT` (`PID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USE_PROMO`
--

LOCK TABLES `USE_PROMO` WRITE;
/*!40000 ALTER TABLE `USE_PROMO` DISABLE KEYS */;
INSERT INTO `USE_PROMO` VALUES ('PC1001','O000000001','P000000001'),('PC1002','O000000003','P000000005'),('PC2001','O000000005','P000000009'),('PC1001','O633671303','P000000001'),('PC1002','O633671303','P000000002');
/*!40000 ALTER TABLE `USE_PROMO` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-23 13:35:24
