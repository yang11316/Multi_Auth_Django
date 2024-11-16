-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: django_db
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.22.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add manager table',7,'add_managertable'),(26,'Can change manager table',7,'change_managertable'),(27,'Can delete manager table',7,'delete_managertable'),(28,'Can view manager table',7,'view_managertable'),(29,'Can add register table',8,'add_registertable'),(30,'Can change register table',8,'change_registertable'),(31,'Can delete register table',8,'delete_registertable'),(32,'Can view register table',8,'view_registertable'),(33,'Can add user table',9,'add_usertable'),(34,'Can change user table',9,'change_usertable'),(35,'Can delete user table',9,'delete_usertable'),(36,'Can view user table',9,'view_usertable'),(37,'Can add node table',10,'add_nodetable'),(38,'Can change node table',10,'change_nodetable'),(39,'Can delete node table',10,'delete_nodetable'),(40,'Can view node table',10,'view_nodetable'),(41,'Can add log table',11,'add_logtable'),(42,'Can change log table',11,'change_logtable'),(43,'Can delete log table',11,'delete_logtable'),(44,'Can view log table',11,'view_logtable'),(45,'Can add software table',12,'add_softwaretable'),(46,'Can change software table',12,'change_softwaretable'),(47,'Can delete software table',12,'delete_softwaretable'),(48,'Can view software table',12,'view_softwaretable'),(49,'Can add software location',13,'add_softwarelocation'),(50,'Can change software location',13,'change_softwarelocation'),(51,'Can delete software location',13,'delete_softwarelocation'),(52,'Can view software location',13,'view_softwarelocation'),(53,'Can add regist software table',14,'add_registsoftwaretable'),(54,'Can change regist software table',14,'change_registsoftwaretable'),(55,'Can delete regist software table',14,'delete_registsoftwaretable'),(56,'Can view regist software table',14,'view_registsoftwaretable'),(57,'Can add enity table',15,'add_enitytable'),(58,'Can change enity table',15,'change_enitytable'),(59,'Can delete enity table',15,'delete_enitytable'),(60,'Can view enity table',15,'view_enitytable'),(61,'Can add register software location table',16,'add_registersoftwarelocationtable'),(62,'Can change register software location table',16,'change_registersoftwarelocationtable'),(63,'Can delete register software location table',16,'delete_registersoftwarelocationtable'),(64,'Can view register software location table',16,'view_registersoftwarelocationtable'),(65,'Can add register software table',17,'add_registersoftwaretable'),(66,'Can change register software table',17,'change_registersoftwaretable'),(67,'Can delete register software table',17,'delete_registersoftwaretable'),(68,'Can view register software table',17,'view_registersoftwaretable'),(69,'Can add kgc paramter table',18,'add_kgcparamtertable'),(70,'Can change kgc paramter table',18,'change_kgcparamtertable'),(71,'Can delete kgc paramter table',18,'delete_kgcparamtertable'),(72,'Can view kgc paramter table',18,'view_kgcparamtertable'),(73,'Can add domain table',19,'add_domaintable'),(74,'Can change domain table',19,'change_domaintable'),(75,'Can delete domain table',19,'delete_domaintable'),(76,'Can view domain table',19,'view_domaintable');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(19,'domainmanage','domaintable'),(15,'entitymanage','enitytable'),(18,'entitymanage','kgcparamtertable'),(11,'nodemanage','logtable'),(10,'nodemanage','nodetable'),(6,'sessions','session'),(16,'softwaremanage','registersoftwarelocationtable'),(17,'softwaremanage','registersoftwaretable'),(14,'softwaremanage','registsoftwaretable'),(13,'softwaremanage','softwarelocation'),(12,'softwaremanage','softwaretable'),(7,'usermanage','managertable'),(8,'usermanage','registertable'),(9,'usermanage','usertable');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-04-08 10:14:44.073684'),(2,'auth','0001_initial','2024-04-08 10:14:44.963868'),(3,'admin','0001_initial','2024-04-08 10:14:45.142430'),(4,'admin','0002_logentry_remove_auto_add','2024-04-08 10:14:45.166654'),(5,'admin','0003_logentry_add_action_flag_choices','2024-04-08 10:14:45.190204'),(6,'contenttypes','0002_remove_content_type_name','2024-04-08 10:14:45.317864'),(7,'auth','0002_alter_permission_name_max_length','2024-04-08 10:14:45.395666'),(8,'auth','0003_alter_user_email_max_length','2024-04-08 10:14:45.452107'),(9,'auth','0004_alter_user_username_opts','2024-04-08 10:14:45.474830'),(10,'auth','0005_alter_user_last_login_null','2024-04-08 10:14:45.554174'),(11,'auth','0006_require_contenttypes_0002','2024-04-08 10:14:45.561473'),(12,'auth','0007_alter_validators_add_error_messages','2024-04-08 10:14:45.585741'),(13,'auth','0008_alter_user_username_max_length','2024-04-08 10:14:45.697043'),(14,'auth','0009_alter_user_last_name_max_length','2024-04-08 10:14:45.790945'),(15,'auth','0010_alter_group_name_max_length','2024-04-08 10:14:45.837279'),(16,'auth','0011_update_proxy_permissions','2024-04-08 10:14:45.860987'),(17,'auth','0012_alter_user_first_name_max_length','2024-04-08 10:14:45.948921'),(18,'usermanage','0001_initial','2024-04-08 10:14:46.028517'),(19,'softwaremanage','0001_initial','2024-04-08 10:14:46.276143'),(20,'nodemanage','0001_initial','2024-04-08 10:14:46.381597'),(21,'entitymanage','0001_initial','2024-04-08 10:14:46.608503'),(22,'sessions','0001_initial','2024-04-08 10:14:46.664457'),(23,'nodemanage','0002_nodetable_node_port','2024-04-09 08:18:40.188203'),(24,'entitymanage','0002_kgcparamtertable','2024-04-12 03:55:36.373626'),(25,'softwaremanage','0002_registersoftwarelocationtable_registersoftwaretable_and_more','2024-04-12 03:55:36.713814'),(26,'entitymanage','0003_remove_kgcparamtertable_id_and_more','2024-04-12 03:56:24.470039'),(27,'entitymanage','0004_remove_enitytable_entity_port_and_more','2024-05-05 07:29:44.269911'),(28,'nodemanage','0003_nodetable_node_is_alive_alter_nodetable_node_ip','2024-05-05 07:29:44.663679'),(29,'softwaremanage','0003_alter_registersoftwarelocationtable_entity_ip_and_more','2024-05-05 07:29:45.052993'),(30,'softwaremanage','0004_alter_softwaretable_software_hash','2024-05-17 11:30:40.621516'),(31,'entitymanage','0005_enitytable_software_name','2024-05-17 11:46:20.191575'),(32,'domainmanage','0001_initial','2024-11-08 07:42:46.826663');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domainmanage_domaintable`
--

DROP TABLE IF EXISTS `domainmanage_domaintable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domainmanage_domaintable` (
  `domain_id` varchar(32) NOT NULL,
  `domain_ip` char(39) NOT NULL,
  `domain_port` int NOT NULL,
  PRIMARY KEY (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domainmanage_domaintable`
--

LOCK TABLES `domainmanage_domaintable` WRITE;
/*!40000 ALTER TABLE `domainmanage_domaintable` DISABLE KEYS */;
INSERT INTO `domainmanage_domaintable` VALUES ('05f7088afd7bcdd7cc818c7ebe7b56cc','192.168.3.73',8000),('98657b1d3ea5b3d5266d6961d98c1152','0.0.0.0',8000);
/*!40000 ALTER TABLE `domainmanage_domaintable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entitymanage_enitytable`
--

DROP TABLE IF EXISTS `entitymanage_enitytable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entitymanage_enitytable` (
  `entity_index` int NOT NULL AUTO_INCREMENT,
  `entity_pid` varchar(32) NOT NULL,
  `entity_parcialkey` longtext,
  `entity_porecessid` varchar(20) DEFAULT NULL,
  `entity_ip` char(39) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_alive` tinyint(1) NOT NULL,
  `node_id_id` varchar(32) NOT NULL,
  `software_id_id` varchar(32) NOT NULL,
  `user_id_id` varchar(32) NOT NULL,
  `entity_listening_port` int DEFAULT NULL,
  `entity_sending_port` int DEFAULT NULL,
  `software_name` varchar(20) NOT NULL,
  PRIMARY KEY (`entity_index`),
  KEY `entitymanage_enityta_node_id_id_0b25683e_fk_nodemanag` (`node_id_id`),
  KEY `entitymanage_enityta_software_id_id_3b83338f_fk_softwarem` (`software_id_id`),
  KEY `entitymanage_enityta_user_id_id_e709be34_fk_usermanag` (`user_id_id`),
  CONSTRAINT `entitymanage_enityta_node_id_id_0b25683e_fk_nodemanag` FOREIGN KEY (`node_id_id`) REFERENCES `nodemanage_nodetable` (`node_id`),
  CONSTRAINT `entitymanage_enityta_software_id_id_3b83338f_fk_softwarem` FOREIGN KEY (`software_id_id`) REFERENCES `softwaremanage_softwaretable` (`software_id`),
  CONSTRAINT `entitymanage_enityta_user_id_id_e709be34_fk_usermanag` FOREIGN KEY (`user_id_id`) REFERENCES `usermanage_usertable` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entitymanage_enitytable`
--

LOCK TABLES `entitymanage_enitytable` WRITE;
/*!40000 ALTER TABLE `entitymanage_enitytable` DISABLE KEYS */;
INSERT INTO `entitymanage_enitytable` VALUES (177,'d28c5d574335a1f4df5e9cda04fa953','8f52bb068a5873807e69592ebad08bb074c3a35b86b584b0466504aedbd13ba03d9c8f4ae174461dcbbe3943b4e33a8527b8fdc27d1f34e49f1788f7a5b16f49','','192.168.3.17','2024-11-06 06:59:07.596124','2024-11-11 08:18:14.846283',0,'node_id','7cd40797e81f13a61232efa8c655763e','2b0246eaa2073b1a4a374d251a3a2965',0,0,'Process1'),(179,'f215c66d45dadd63f26771c71b972b7f','4e58b0eb9b63798deb0b4f9865b72c6148a82dd7c140c4d4dd2e7dbe9b90f1cded1e5ef7eae7d3016b57817fd3ef800cbf40b38f4ea45bbc8a7d11b0a36dfac0','','192.168.3.17','2024-11-06 07:05:52.095611','2024-11-09 05:31:39.420138',0,'node_id','31961c3d8b9d46e56b3ed8712d3e6119','2b0246eaa2073b1a4a374d251a3a2965',0,0,'Process3'),(180,'de27bd642ee181341fb6cb6e04f4ab59','314049810cf43c228b5ce435dc709e10d3a521023aa3df44773c7dd9dc35038cdb72537f2791ea084b8a6962dbb6b3b29b067d3f7bf5b54899839f7558fbc94f','29904','192.168.3.67','2024-11-06 07:13:11.621834','2024-11-06 07:55:27.798957',1,'node_w','b43b8096a64401d02037789bbae20140','2b0246eaa2073b1a4a374d251a3a2965',9995,9994,'Process4'),(181,'161fcceb50e8e942602ca3147deb9379','3db4ca5b3733645b80e7260d747952bf2dca44628d18bfce41d728eb027d068a0a7ca08d9c99748e4f54c3b141ff0c4112761887c7d060b3729525386703dd96',NULL,'192.168.3.67','2024-11-06 07:13:21.607306','2024-11-06 07:55:27.803754',0,'node_w','b43b8096a64401d02037789bbae20140','2b0246eaa2073b1a4a374d251a3a2965',NULL,NULL,'Process4');
/*!40000 ALTER TABLE `entitymanage_enitytable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entitymanage_kgcparamtertable`
--

DROP TABLE IF EXISTS `entitymanage_kgcparamtertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entitymanage_kgcparamtertable` (
  `kgc_id` varchar(32) NOT NULL,
  `kgc_s` longtext NOT NULL,
  `kgc_Ppub` longtext NOT NULL,
  `kgc_q` longtext NOT NULL,
  `kgc_acc_G` longtext NOT NULL,
  `kgc_acc_publickey` longtext NOT NULL,
  `kgc_acc_cur` longtext NOT NULL,
  `kgc_acc_serectkey0` longtext NOT NULL,
  `kgc_acc_serectkey1` longtext NOT NULL,
  PRIMARY KEY (`kgc_id`),
  UNIQUE KEY `entitymanage_kgcparamtertable_kgc_id_cc3cf238_uniq` (`kgc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entitymanage_kgcparamtertable`
--

LOCK TABLES `entitymanage_kgcparamtertable` WRITE;
/*!40000 ALTER TABLE `entitymanage_kgcparamtertable` DISABLE KEYS */;
INSERT INTO `entitymanage_kgcparamtertable` VALUES ('kgc_id','9ec59bfd1247aa7a0408c2f56601b8e97dced350bb3cd94976b210232344d487','48572967456924874902545652400944683746644627328382974480484690693553514678178109081729721050495835181458537531031544594585790366838858055804589514235371350','fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141','97ef1f09dcc6e81e2c08f3c96f04710fe1d05b39ac00e6fc190de20293c7ee01','a775863f0ad44ca20035dbc8bee624ec9d65415f670e0a7b501bffb6bb298c064d977c6f3a43728ca6a4eca0c35cf0a3957c007de7b601e4302738a734c3bd43','35dc069641c8fe1de882c32e43f09acbf14fb3a2d6ab364ca18de1b31422651e19688637678850b352f645834c2eeca5783beaca6281f8e3acfcf00de63b9bfb','f04fccdf714e91d01d7d87fbb12c8826ca0aad405aeab51f72c91dbcedbd5991','b2642d67ff49bb64d5de352ddf412a0681495550ad73799772de8648ddc4df93');
/*!40000 ALTER TABLE `entitymanage_kgcparamtertable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nodemanage_logtable`
--

DROP TABLE IF EXISTS `nodemanage_logtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nodemanage_logtable` (
  `log_id` varchar(32) NOT NULL,
  `log_type` varchar(20) NOT NULL,
  `log_desc` longtext,
  `create_time` datetime(6) NOT NULL,
  `log_node_id` varchar(32) NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `nodemanage_logtable_log_node_id_60efcea4_fk_nodemanag` (`log_node_id`),
  CONSTRAINT `nodemanage_logtable_log_node_id_60efcea4_fk_nodemanag` FOREIGN KEY (`log_node_id`) REFERENCES `nodemanage_nodetable` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nodemanage_logtable`
--

LOCK TABLES `nodemanage_logtable` WRITE;
/*!40000 ALTER TABLE `nodemanage_logtable` DISABLE KEYS */;
/*!40000 ALTER TABLE `nodemanage_logtable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nodemanage_nodetable`
--

DROP TABLE IF EXISTS `nodemanage_nodetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nodemanage_nodetable` (
  `node_id` varchar(32) NOT NULL,
  `node_ip` char(39) NOT NULL,
  `node_desc` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `node_port` int NOT NULL,
  `node_is_alive` tinyint(1) NOT NULL,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nodemanage_nodetable`
--

LOCK TABLES `nodemanage_nodetable` WRITE;
/*!40000 ALTER TABLE `nodemanage_nodetable` DISABLE KEYS */;
INSERT INTO `nodemanage_nodetable` VALUES ('node_id','192.168.3.17','这是一段测试使用AP的描述','2024-04-08 21:13:59.000000','2024-11-11 08:17:14.785891',9000,1),('node_w','192.168.3.67','windows','2024-04-08 21:13:59.000000','2024-10-14 07:25:56.392331',9000,1);
/*!40000 ALTER TABLE `nodemanage_nodetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwaremanage_registersoftwarelocationtable`
--

DROP TABLE IF EXISTS `softwaremanage_registersoftwarelocationtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwaremanage_registersoftwarelocationtable` (
  `rlsoftwarelocation_index` int NOT NULL AUTO_INCREMENT,
  `node_ip` char(39) NOT NULL,
  `entity_ip` char(39) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `rsoftware_id_id` varchar(32) NOT NULL,
  PRIMARY KEY (`rlsoftwarelocation_index`),
  KEY `softwaremanage_regis_rsoftware_id_id_735dab09_fk_softwarem` (`rsoftware_id_id`),
  CONSTRAINT `softwaremanage_regis_rsoftware_id_id_735dab09_fk_softwarem` FOREIGN KEY (`rsoftware_id_id`) REFERENCES `softwaremanage_registersoftwaretable` (`rsoftware_id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwaremanage_registersoftwarelocationtable`
--

LOCK TABLES `softwaremanage_registersoftwarelocationtable` WRITE;
/*!40000 ALTER TABLE `softwaremanage_registersoftwarelocationtable` DISABLE KEYS */;
/*!40000 ALTER TABLE `softwaremanage_registersoftwarelocationtable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwaremanage_registersoftwaretable`
--

DROP TABLE IF EXISTS `softwaremanage_registersoftwaretable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwaremanage_registersoftwaretable` (
  `rsoftware_id` varchar(32) NOT NULL,
  `rsoftware_name` varchar(20) NOT NULL,
  `rsoftware_path` varchar(50) NOT NULL,
  `rsoftware_version` varchar(50) NOT NULL,
  `rsoftware_desc` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `user_id_id` varchar(32) NOT NULL,
  PRIMARY KEY (`rsoftware_id`),
  KEY `softwaremanage_regis_user_id_id_a9d09c00_fk_usermanag` (`user_id_id`),
  CONSTRAINT `softwaremanage_regis_user_id_id_a9d09c00_fk_usermanag` FOREIGN KEY (`user_id_id`) REFERENCES `usermanage_usertable` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwaremanage_registersoftwaretable`
--

LOCK TABLES `softwaremanage_registersoftwaretable` WRITE;
/*!40000 ALTER TABLE `softwaremanage_registersoftwaretable` DISABLE KEYS */;
/*!40000 ALTER TABLE `softwaremanage_registersoftwaretable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwaremanage_softwarelocation`
--

DROP TABLE IF EXISTS `softwaremanage_softwarelocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwaremanage_softwarelocation` (
  `softwarelocation_index` int NOT NULL AUTO_INCREMENT,
  `node_ip` varchar(15) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `software_id_id` varchar(32) NOT NULL,
  `entity_ip` varchar(15) NOT NULL,
  PRIMARY KEY (`softwarelocation_index`),
  KEY `softwaremanage_softw_software_id_id_fc01f4da_fk_softwarem` (`software_id_id`),
  CONSTRAINT `softwaremanage_softw_software_id_id_fc01f4da_fk_softwarem` FOREIGN KEY (`software_id_id`) REFERENCES `softwaremanage_softwaretable` (`software_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwaremanage_softwarelocation`
--

LOCK TABLES `softwaremanage_softwarelocation` WRITE;
/*!40000 ALTER TABLE `softwaremanage_softwarelocation` DISABLE KEYS */;
/*!40000 ALTER TABLE `softwaremanage_softwarelocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `softwaremanage_softwaretable`
--

DROP TABLE IF EXISTS `softwaremanage_softwaretable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `softwaremanage_softwaretable` (
  `software_id` varchar(32) NOT NULL,
  `software_version` varchar(50) NOT NULL,
  `software_name` varchar(20) NOT NULL,
  `software_hash` varchar(32) NOT NULL,
  `software_desc` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `user_id_id` varchar(32) NOT NULL,
  PRIMARY KEY (`software_id`),
  KEY `softwaremanage_softw_user_id_id_b7437601_fk_usermanag` (`user_id_id`),
  CONSTRAINT `softwaremanage_softw_user_id_id_b7437601_fk_usermanag` FOREIGN KEY (`user_id_id`) REFERENCES `usermanage_usertable` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `softwaremanage_softwaretable`
--

LOCK TABLES `softwaremanage_softwaretable` WRITE;
/*!40000 ALTER TABLE `softwaremanage_softwaretable` DISABLE KEYS */;
INSERT INTO `softwaremanage_softwaretable` VALUES ('29b35e09e61e905ab2ddf33a3d216322','1','Process2','850462563da237bafec7123c5b88f2f8','1','2024-11-06 07:04:22.025583','2024-11-06 07:04:22.025639','2b0246eaa2073b1a4a374d251a3a2965'),('31961c3d8b9d46e56b3ed8712d3e6119','1','Process3','67164e42e5ceafc672f2a0cecb0c696d','1','2024-11-06 07:05:52.090758','2024-11-06 07:05:52.090881','2b0246eaa2073b1a4a374d251a3a2965'),('7cd40797e81f13a61232efa8c655763e','1','Process1','867cea7768922345426c57ee9d1b5d49','1','2024-11-06 06:59:07.591276','2024-11-06 06:59:07.591335','2b0246eaa2073b1a4a374d251a3a2965'),('b43b8096a64401d02037789bbae20140','1','Process4','f4811a37df239128b2ffb6583d836619','1','2024-11-06 07:13:11.617003','2024-11-06 07:13:11.617060','2b0246eaa2073b1a4a374d251a3a2965');
/*!40000 ALTER TABLE `softwaremanage_softwaretable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermanage_managertable`
--

DROP TABLE IF EXISTS `usermanage_managertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermanage_managertable` (
  `manager_id` varchar(32) NOT NULL,
  `manager_name` varchar(20) NOT NULL,
  `manager_pwd` varchar(20) NOT NULL,
  `manager_phone` varchar(11) DEFAULT NULL,
  `manager_email` varchar(254) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermanage_managertable`
--

LOCK TABLES `usermanage_managertable` WRITE;
/*!40000 ALTER TABLE `usermanage_managertable` DISABLE KEYS */;
/*!40000 ALTER TABLE `usermanage_managertable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermanage_registertable`
--

DROP TABLE IF EXISTS `usermanage_registertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermanage_registertable` (
  `user_id` varchar(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_pwd` varchar(20) NOT NULL,
  `user_phone` varchar(11) DEFAULT NULL,
  `user_email` varchar(254) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermanage_registertable`
--

LOCK TABLES `usermanage_registertable` WRITE;
/*!40000 ALTER TABLE `usermanage_registertable` DISABLE KEYS */;
/*!40000 ALTER TABLE `usermanage_registertable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermanage_usertable`
--

DROP TABLE IF EXISTS `usermanage_usertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermanage_usertable` (
  `user_id` varchar(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_row` varchar(20) NOT NULL,
  `user_pwd` varchar(16) NOT NULL,
  `user_phone` varchar(11) DEFAULT NULL,
  `user_email` varchar(254) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermanage_usertable`
--

LOCK TABLES `usermanage_usertable` WRITE;
/*!40000 ALTER TABLE `usermanage_usertable` DISABLE KEYS */;
INSERT INTO `usermanage_usertable` VALUES ('0ad9e30ca539f968e662b6d505fcd276','Plant_Manager','admin','user_pwd','17899012894','PlantManager@nav.com','2024-05-16 08:04:47.644295','2024-07-04 08:45:10.228584'),('2b0246eaa2073b1a4a374d251a3a2965','Nav_Operator01','editor','user_pwd','15099783221','NavOperator@nav.com','2024-07-04 08:43:29.131256','2024-07-04 08:44:02.216097'),('bf27477a2310eac22a5b7100256b689a','Nav_Operator02','editor','user_pwd','15099783222','NavOperator02@nav.com','2024-09-22 13:17:51.294372','2024-09-22 13:17:58.015600');
/*!40000 ALTER TABLE `usermanage_usertable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-13  9:42:03
