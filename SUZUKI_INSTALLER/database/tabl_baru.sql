/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 10.4.32-MariaDB : Database - plc_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`plc_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `plc_db`;

/*Table structure for table `plc_oee_seat_ng_ok_activity` */

DROP TABLE IF EXISTS `plc_oee_seat_ng_ok_activity`;

CREATE TABLE `plc_oee_seat_ng_ok_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(50) DEFAULT NULL,
  `station_id` varchar(50) DEFAULT NULL,
  `value` text DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_ng_ok_activity` */

/*Table structure for table `plc_oee_seat_ng_ok_master` */

DROP TABLE IF EXISTS `plc_oee_seat_ng_ok_master`;

CREATE TABLE `plc_oee_seat_ng_ok_master` (
  `device` varchar(50) NOT NULL,
  `value` varchar(50) DEFAULT '0',
  `station_id` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  UNIQUE KEY `unique_device_station` (`device`,`station_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_ng_ok_master` */

insert  into `plc_oee_seat_ng_ok_master`(`device`,`value`,`station_id`,`comment`,`update_at`) values 
('D968','1',1,'OK / NG RESULT ->GOT- QC1','2026-03-11 19:45:59'),
('D970','1',2,'OK / NG RESULT ->GOT- QC2','2026-03-11 19:48:44'),
('D972','2',3,'OK / NG RESULT ->GOT- QC3','2026-03-11 19:46:25'),
('D974','2',1,'OK / NG ITEM 1->GOT- QC1','2026-03-11 19:45:49'),
('D975','0',1,'OK / NG ITEM 2->GOT- QC1','2026-03-11 18:58:25'),
('D976','1',1,'OK / NG ITEM 3->GOT- QC1','2026-03-11 19:46:19'),
('D977','1',1,'OK / NG ITEM 4->GOT- QC1','2026-03-11 19:46:43'),
('D978','2',1,'OK / NG ITEM 5->GOT- QC1','2026-03-11 19:46:45'),
('D979','2',1,'OK / NG ITEM 6->GOT- QC1','2026-03-11 19:46:05'),
('D980','1',1,'OK / NG ITEM 7->GOT- QC1','2026-03-11 19:46:15'),
('D981','0',1,'OK / NG ITEM 8->GOT- QC1','2026-03-11 18:58:25'),
('D982','0',1,'OK / NG ITEM 9->GOT- QC1','2026-03-11 18:58:25'),
('D983','0',1,'OK / NG ITEM 10->GOT- QC1','2026-03-11 18:58:25'),
('D984','0',1,'OK / NG ITEM 11->GOT- QC1','2026-03-11 18:58:25'),
('D985','0',1,'OK / NG ITEM 12->GOT- QC1','2026-03-11 18:58:25'),
('D986','0',1,'OK / NG ITEM 13->GOT- QC1','2026-03-11 18:58:25'),
('D987','0',1,'OK / NG ITEM 14->GOT- QC1','2026-03-11 18:58:25'),
('D988','0',1,'OK / NG ITEM 15->GOT- QC1','2026-03-11 18:58:25'),
('D989','0',1,'OK / NG ITEM 16->GOT- QC1','2026-03-11 18:58:25'),
('D990','0',1,'OK / NG ITEM 17->GOT- QC1','2026-03-11 18:58:25'),
('D991','0',1,'OK / NG ITEM 18->GOT- QC1','2026-03-11 18:58:25'),
('D992','0',1,'OK / NG ITEM 19->GOT- QC1','2026-03-11 18:58:25'),
('D993','0',1,'OK / NG ITEM 20->GOT- QC1','2026-03-11 18:58:25'),
('D994','0',1,'OK / NG ITEM 21->GOT- QC1','2026-03-11 18:58:25'),
('D995','0',1,'OK / NG ITEM 22->GOT- QC1','2026-03-11 18:58:25'),
('D996','0',1,'OK / NG ITEM 23->GOT- QC1','2026-03-11 18:58:25'),
('D997','0',1,'OK / NG ITEM 24->GOT- QC1','2026-03-11 18:58:25'),
('D998','0',1,'OK / NG ITEM 25->GOT- QC1','2026-03-11 18:58:25'),
('D999','0',1,'OK / NG ITEM 26->GOT- QC1','2026-03-11 18:58:25'),
('D1000','0',1,'OK / NG ITEM 27->GOT- QC1','2026-03-11 18:58:25'),
('D1001','0',1,'OK / NG ITEM 28->GOT- QC1','2026-03-11 18:58:25'),
('D1002','0',1,'OK / NG ITEM 29->GOT- QC1','2026-03-11 18:58:25'),
('D1003','0',1,'OK / NG ITEM 30->GOT- QC1','2026-03-11 18:58:25'),
('D1004','0',1,'OK / NG ITEM 31->GOT- QC1','2026-03-11 18:58:25'),
('D1005','0',1,'OK / NG ITEM 32->GOT- QC1','2026-03-11 18:58:25'),
('D1038','0',2,'OK / NG ITEM 1->GOT- QC2','2026-03-11 18:58:25'),
('D1039','0',2,'OK / NG ITEM 2->GOT- QC2','2026-03-11 18:58:25'),
('D1040','0',2,'OK / NG ITEM 3->GOT- QC2','2026-03-11 18:58:25'),
('D1041','0',2,'OK / NG ITEM 4->GOT- QC2','2026-03-11 18:58:25'),
('D1042','0',2,'OK / NG ITEM 5->GOT- QC2','2026-03-11 18:58:25'),
('D1043','0',2,'OK / NG ITEM 6->GOT- QC2','2026-03-11 18:58:25'),
('D1044','0',2,'OK / NG ITEM 7->GOT- QC2','2026-03-11 18:58:25'),
('D1045','0',2,'OK / NG ITEM 8->GOT- QC2','2026-03-11 18:58:25'),
('D1046','0',2,'OK / NG ITEM 9->GOT- QC2','2026-03-11 18:58:25'),
('D1047','0',2,'OK / NG ITEM 10->GOT- QC2','2026-03-11 18:58:25'),
('D1048','1',2,'OK / NG ITEM 11->GOT- QC2','2026-03-11 19:50:26'),
('D1049','2',2,'OK / NG ITEM 12->GOT- QC2','2026-03-11 19:50:32'),
('D1050','0',2,'OK / NG ITEM 13->GOT- QC2','2026-03-11 18:58:25'),
('D1051','2',2,'OK / NG ITEM 14->GOT- QC2','2026-03-11 19:50:57'),
('D1052','0',2,'OK / NG ITEM 15->GOT- QC2','2026-03-11 18:58:25'),
('D1053','0',2,'OK / NG ITEM 16->GOT- QC2','2026-03-11 18:58:25'),
('D1054','0',2,'OK / NG ITEM 17->GOT- QC2','2026-03-11 18:58:25'),
('D1055','0',2,'OK / NG ITEM 18->GOT- QC2','2026-03-11 18:58:25'),
('D1056','0',2,'OK / NG ITEM 19->GOT- QC2','2026-03-11 18:58:25'),
('D1057','0',2,'OK / NG ITEM 20->GOT- QC2','2026-03-11 18:58:25'),
('D1058','0',2,'OK / NG ITEM 21->GOT- QC2','2026-03-11 18:58:25'),
('D1059','2',2,'OK / NG ITEM 22->GOT- QC2','2026-03-11 19:49:33'),
('D1060','0',2,'OK / NG ITEM 23->GOT- QC2','2026-03-11 18:58:25'),
('D1061','0',2,'OK / NG ITEM 24->GOT- QC2','2026-03-11 18:58:25'),
('D1062','0',2,'OK / NG ITEM 25->GOT- QC2','2026-03-11 18:58:25'),
('D1063','0',2,'OK / NG ITEM 26->GOT- QC2','2026-03-11 18:58:25'),
('D1064','2',2,'OK / NG ITEM 27->GOT- QC2','2026-03-11 19:50:24'),
('D1065','0',2,'OK / NG ITEM 28->GOT- QC2','2026-03-11 18:58:25'),
('D1066','0',2,'OK / NG ITEM 29->GOT- QC2','2026-03-11 18:58:25'),
('D1067','0',2,'OK / NG ITEM 30->GOT- QC2','2026-03-11 18:58:25'),
('D1068','0',2,'OK / NG ITEM 31->GOT- QC2','2026-03-11 18:58:25'),
('D1069','0',2,'OK / NG ITEM 32->GOT- QC2','2026-03-11 18:58:25'),
('D1102','0',3,'OK / NG ITEM 1->GOT- QC3','2026-03-11 18:58:25'),
('D1103','0',3,'OK / NG ITEM 2->GOT- QC3','2026-03-11 18:58:25'),
('D1104','0',3,'OK / NG ITEM 3->GOT- QC3','2026-03-11 18:58:25'),
('D1105','0',3,'OK / NG ITEM 4->GOT- QC3','2026-03-11 18:58:25'),
('D1106','0',3,'OK / NG ITEM 5->GOT- QC3','2026-03-11 18:58:25'),
('D1107','1',3,'OK / NG ITEM 6->GOT- QC3','2026-03-11 19:49:39'),
('D1108','0',3,'OK / NG ITEM 7->GOT- QC3','2026-03-11 18:58:25'),
('D1109','0',3,'OK / NG ITEM 8->GOT- QC3','2026-03-11 18:58:25'),
('D1110','0',3,'OK / NG ITEM 9->GOT- QC3','2026-03-11 18:58:25'),
('D1111','0',3,'OK / NG ITEM 10->GOT- QC3','2026-03-11 18:58:25'),
('D1112','1',3,'OK / NG ITEM 11->GOT- QC3','2026-03-11 19:51:29'),
('D1113','0',3,'OK / NG ITEM 12->GOT- QC3','2026-03-11 18:58:25'),
('D1114','0',3,'OK / NG ITEM 13->GOT- QC3','2026-03-11 18:58:25'),
('D1115','0',3,'OK / NG ITEM 14->GOT- QC3','2026-03-11 18:58:25'),
('D1116','0',3,'OK / NG ITEM 15->GOT- QC3','2026-03-11 18:58:25'),
('D1117','0',3,'OK / NG ITEM 16->GOT- QC3','2026-03-11 18:58:25'),
('D1118','0',3,'OK / NG ITEM 17->GOT- QC3','2026-03-11 18:58:25'),
('D1119','0',3,'OK / NG ITEM 18->GOT- QC3','2026-03-11 18:58:25'),
('D1120','0',3,'OK / NG ITEM 19->GOT- QC3','2026-03-11 18:58:25'),
('D1121','0',3,'OK / NG ITEM 20->GOT- QC3','2026-03-11 18:58:25'),
('D1122','0',3,'OK / NG ITEM 21->GOT- QC3','2026-03-11 18:58:25'),
('D1123','0',3,'OK / NG ITEM 22->GOT- QC3','2026-03-11 18:58:25'),
('D1124','0',3,'OK / NG ITEM 23->GOT- QC3','2026-03-11 18:58:25'),
('D1125','0',3,'OK / NG ITEM 24->GOT- QC3','2026-03-11 18:58:25'),
('D1126','0',3,'OK / NG ITEM 25->GOT- QC3','2026-03-11 18:58:25'),
('D1127','0',3,'OK / NG ITEM 26->GOT- QC3','2026-03-11 18:58:25'),
('D1128','0',3,'OK / NG ITEM 27->GOT- QC3','2026-03-11 18:58:25'),
('D1129','0',3,'OK / NG ITEM 28->GOT- QC3','2026-03-11 18:58:25'),
('D1130','0',3,'OK / NG ITEM 29->GOT- QC3','2026-03-11 18:58:25'),
('D1131','0',3,'OK / NG ITEM 30->GOT- QC3','2026-03-11 18:58:25'),
('D1132','0',3,'OK / NG ITEM 31->GOT- QC3','2026-03-11 18:58:25'),
('D1133','0',3,'OK / NG ITEM 32->GOT- QC3','2026-03-11 18:58:25');

/*Table structure for table `plc_oee_seat_result_activity` */

DROP TABLE IF EXISTS `plc_oee_seat_result_activity`;

CREATE TABLE `plc_oee_seat_result_activity` (
  `device` varchar(50) DEFAULT NULL,
  `station_id` varchar(50) DEFAULT NULL,
  `seq` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `dest` varchar(50) DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_result_activity` */

/*Table structure for table `plc_oee_seat_result_detail` */

DROP TABLE IF EXISTS `plc_oee_seat_result_detail`;

CREATE TABLE `plc_oee_seat_result_detail` (
  `device` varchar(50) NOT NULL,
  `value` varchar(50) DEFAULT '0',
  `station_id` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  UNIQUE KEY `unique_device_station` (`device`,`station_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_result_detail` */

insert  into `plc_oee_seat_result_detail`(`device`,`value`,`station_id`,`comment`,`update_at`) values 
('D1170','0',1,'SEQ->GOT- QC1','2026-03-11 18:58:25'),
('D1172','0',1,'MODEL->GOT- QC1','2026-03-11 18:58:25'),
('D1175','2897',1,'DEST->GOT- QC1','2026-03-11 19:50:08'),
('D1177','0',1,'GRADE->GOT- QC1','2026-03-11 18:58:25'),
('D1184','0',2,'SEQ->GOT- QC2','2026-03-11 18:58:25'),
('D1186','0',2,'MODEL->GOT- QC2','2026-03-11 18:58:25'),
('D1189','9772',2,'DEST->GOT- QC2','2026-03-11 19:49:31'),
('D1191','0',2,'GRADE->GOT- QC2','2026-03-11 18:58:25'),
('D1198','0',3,'SEQ->GOT- QC3','2026-03-11 18:58:25'),
('D1200','0',3,'MODEL->GOT- QC3','2026-03-11 18:58:25'),
('D1203','0',3,'DEST->GOT- QC3','2026-03-11 18:58:25'),
('D1205','1922',3,'GRADE->GOT- QC3','2026-03-11 19:50:16'),
('D1207','65',3,'A#->GOT- QC3','2026-03-11 19:49:41');

/*Table structure for table `plc_oee_seat_text_input` */

DROP TABLE IF EXISTS `plc_oee_seat_text_input`;

CREATE TABLE `plc_oee_seat_text_input` (
  `device` varchar(50) NOT NULL,
  `value` varchar(50) DEFAULT '0',
  `station_id` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  UNIQUE KEY `unique_device_station` (`device`,`station_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_text_input` */

insert  into `plc_oee_seat_text_input`(`device`,`value`,`station_id`,`comment`,`update_at`) values 
('D1250','0',1,'TEXT INPUT ITEM 1->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1270','0',1,'TEXT INPUT ITEM 3->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1290','0',1,'TEXT INPUT ITEM 5->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1310','0',1,'TEXT INPUT ITEM 7->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1330','0',1,'TEXT INPUT ITEM 9->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1350','0',1,'TEXT INPUT ITEM 11->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1370','0',1,'TEXT INPUT ITEM 13->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1390','0',1,'TEXT INPUT ITEM 15->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1410','0',1,'TEXT INPUT ITEM 17->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1430','0',1,'TEXT INPUT ITEM 19->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1450','0',1,'TEXT INPUT ITEM 21->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1470','0',1,'TEXT INPUT ITEM 23->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1490','0',1,'TEXT INPUT ITEM 25->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1510','0',1,'TEXT INPUT ITEM 27->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1530','0',1,'TEXT INPUT ITEM 29->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1550','0',1,'TEXT INPUT ITEM 31->GOT- QC1  AUX','2026-03-11 18:58:25'),
('D1570','70',2,'TEXT INPUT ITEM 1->GOT- QC2  AUX','2026-03-11 19:49:55'),
('D1590','0',2,'TEXT INPUT ITEM 3->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1610','0',2,'TEXT INPUT ITEM 5->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1630','0',2,'TEXT INPUT ITEM 7->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1650','0',2,'TEXT INPUT ITEM 9->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1670','0',2,'TEXT INPUT ITEM 11->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1690','0',2,'TEXT INPUT ITEM 13->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1710','0',2,'TEXT INPUT ITEM 15->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1730','0',2,'TEXT INPUT ITEM 17->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1750','0',2,'TEXT INPUT ITEM 19->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1770','0',2,'TEXT INPUT ITEM 21->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1790','0',2,'TEXT INPUT ITEM 23->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1810','0',2,'TEXT INPUT ITEM 25->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1830','0',2,'TEXT INPUT ITEM 27->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1850','60',2,'TEXT INPUT ITEM 29->GOT- QC2  AUX','2026-03-11 19:48:36'),
('D1870','0',2,'TEXT INPUT ITEM 31->GOT- QC2  AUX','2026-03-11 18:58:25'),
('D1890','0',3,'TEXT INPUT ITEM 1->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D1910','0',3,'TEXT INPUT ITEM 3->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D1930','0',3,'TEXT INPUT ITEM 5->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D1950','0',3,'TEXT INPUT ITEM 7->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D1970','0',3,'TEXT INPUT ITEM 9->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D1990','0',3,'TEXT INPUT ITEM 11->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2010','0',3,'TEXT INPUT ITEM 13->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2030','0',3,'TEXT INPUT ITEM 15->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2050','0',3,'TEXT INPUT ITEM 17->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2070','0',3,'TEXT INPUT ITEM 19->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2090','93',3,'TEXT INPUT ITEM 21->GOT- QC3  AUX','2026-03-11 19:48:42'),
('D2110','40',3,'TEXT INPUT ITEM 23->GOT- QC3  AUX','2026-03-11 19:48:28'),
('D2130','0',3,'TEXT INPUT ITEM 25->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2150','0',3,'TEXT INPUT ITEM 27->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2170','0',3,'TEXT INPUT ITEM 29->GOT- QC3  AUX','2026-03-11 18:58:25'),
('D2190','0',3,'TEXT INPUT ITEM 31->GOT- QC3  AUX','2026-03-11 18:58:25');

/*Table structure for table `plc_oee_seat_text_input_activity` */

DROP TABLE IF EXISTS `plc_oee_seat_text_input_activity`;

CREATE TABLE `plc_oee_seat_text_input_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(50) DEFAULT NULL,
  `station_id` varchar(50) DEFAULT NULL,
  `value` text DEFAULT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `plc_oee_seat_text_input_activity` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
