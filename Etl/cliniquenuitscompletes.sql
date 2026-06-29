-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: cliniquev3
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appareil`
--

DROP TABLE IF EXISTS `appareil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil` (
  `id_appareil` int NOT NULL AUTO_INCREMENT,
  `modele` varchar(100) NOT NULL,
  `numero_serie` varchar(100) DEFAULT NULL,
  `fabricant` varchar(100) DEFAULT NULL,
  `date_installation` date DEFAULT NULL,
  `statut` varchar(20) NOT NULL DEFAULT 'actif',
  `localisation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_appareil`),
  UNIQUE KEY `numero_serie` (`numero_serie`),
  CONSTRAINT `appareil_chk_1` CHECK ((`statut` in (_utf8mb4'actif',_utf8mb4'maintenance',_utf8mb4'hors service')))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil`
--

LOCK TABLES `appareil` WRITE;
/*!40000 ALTER TABLE `appareil` DISABLE KEYS */;
INSERT INTO `appareil` VALUES (1,'Natus Embla N7000','SN-PSG-001','Natus Medical','2018-03-01','actif','Salle PSG 1'),(2,'Natus Embla N7000','SN-PSG-002','Natus Medical','2018-03-01','actif','Salle PSG 2'),(3,'Natus Embla N7000','SN-PSG-003','Natus Medical','2019-06-15','actif','Salle PSG 3'),(4,'Somnoscreen Plus','SN-PSG-004','Somnomedics','2020-01-10','actif','Salle PSG 4'),(5,'Somnoscreen Plus','SN-PSG-005','Somnomedics','2020-01-10','maintenance','Salle PSG 5'),(6,'Natus Embla N7000','SN-PSG-006','Natus Medical','2021-04-01','actif','RÃ©serve'),(7,'Alice 6 LDx','SN-PSG-007','Philips','2021-09-01','actif','RÃ©serve'),(8,'Alice 6 LDx','SN-PSG-008','Philips','2022-02-01','actif','RÃ©serve'),(9,'Somnoscreen Plus','SN-PSG-009','Somnomedics','2022-07-01','actif','RÃ©serve'),(10,'Natus Embla N7000','SN-PSG-010','Natus Medical','2023-01-01','actif','RÃ©serve'),(11,'AirSense 11','SN-CPAP-001','ResMed','2021-01-15','actif','Domicile patient'),(12,'AirSense 11','SN-CPAP-002','ResMed','2021-03-01','actif','Domicile patient'),(13,'AirSense 11','SN-CPAP-003','ResMed','2021-06-01','actif','Domicile patient'),(14,'DreamStation 2','SN-CPAP-004','Philips Respironics','2021-09-01','actif','Domicile patient'),(15,'DreamStation 2','SN-CPAP-005','Philips Respironics','2021-09-01','actif','Domicile patient'),(16,'AirSense 11','SN-CPAP-006','ResMed','2022-01-01','actif','Domicile patient'),(17,'AirSense 11','SN-CPAP-007','ResMed','2022-03-01','actif','Domicile patient'),(18,'DreamStation 2','SN-CPAP-008','Philips Respironics','2022-06-01','actif','Domicile patient'),(19,'AirSense 11','SN-CPAP-009','ResMed','2022-09-01','actif','Domicile patient'),(20,'AirSense 11','SN-CPAP-010','ResMed','2023-01-01','actif','Domicile patient'),(21,'DreamStation 2','SN-CPAP-011','Philips Respironics','2023-03-01','actif','Domicile patient'),(22,'AirSense 11','SN-CPAP-012','ResMed','2023-06-01','actif','Domicile patient'),(23,'AirSense 11','SN-CPAP-013','ResMed','2024-01-15','actif','Domicile patient'),(24,'AirSense 11','SN-CPAP-014','ResMed','2023-03-10','actif','Domicile patient'),(25,'DreamStation 2','SN-CPAP-015','Philips Respironics','2023-04-20','actif','Domicile patient'),(26,'AirSense 11','SN-CPAP-016','ResMed','2022-11-20','actif','Domicile patient'),(27,'AirSense 11','SN-CPAP-017','ResMed','2022-12-25','actif','Domicile patient'),(28,'DreamStation 2','SN-CPAP-018','Philips Respironics','2023-06-20','actif','Domicile patient'),(29,'AirSense 11','SN-CPAP-019','ResMed','2023-07-20','actif','Domicile patient'),(30,'AirSense 11','SN-CPAP-020','ResMed','2025-05-25','actif','Domicile patient');
/*!40000 ALTER TABLE `appareil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareil_cpap`
--

DROP TABLE IF EXISTS `appareil_cpap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil_cpap` (
  `id_appareil` int NOT NULL,
  `id_patient` int DEFAULT NULL COMMENT 'Patient auquel l appareil est attribuÃ©',
  `pression_initiale` decimal(4,1) DEFAULT NULL,
  `type_masque` varchar(50) DEFAULT NULL COMMENT 'nasal / facial / narinaire',
  `taille_masque` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_appareil`),
  KEY `fk_cpap_patient` (`id_patient`),
  CONSTRAINT `fk_appareil_cpap` FOREIGN KEY (`id_appareil`) REFERENCES `appareil` (`id_appareil`),
  CONSTRAINT `fk_cpap_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `appareil_cpap_chk_1` CHECK ((`pression_initiale` between 4 and 25))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil_cpap`
--

LOCK TABLES `appareil_cpap` WRITE;
/*!40000 ALTER TABLE `appareil_cpap` DISABLE KEYS */;
INSERT INTO `appareil_cpap` VALUES (11,NULL,8.0,'nasal','M'),(12,1,9.0,'facial','L'),(13,2,10.0,'nasal','M'),(14,NULL,10.0,'facial','M'),(15,NULL,8.5,'narinaire','M'),(16,NULL,9.5,'nasal','L'),(17,NULL,7.0,'facial','S'),(18,NULL,11.0,'nasal','M'),(19,NULL,8.0,'narinaire','S'),(20,NULL,9.0,'nasal','M'),(21,NULL,10.5,'facial','L'),(22,NULL,8.5,'nasal','M'),(23,NULL,8.0,'narinaire','S'),(24,NULL,9.0,'facial','L'),(25,NULL,10.0,'facial','M'),(26,NULL,10.0,'facial','XL'),(27,NULL,11.0,'facial','L'),(28,NULL,8.0,'nasal','M'),(29,NULL,9.0,'nasal','M'),(30,NULL,7.5,'narinaire','S');
/*!40000 ALTER TABLE `appareil_cpap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareil_psg`
--

DROP TABLE IF EXISTS `appareil_psg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appareil_psg` (
  `id_appareil` int NOT NULL,
  `version_firmware` varchar(50) DEFAULT NULL,
  `type_montage` varchar(50) DEFAULT NULL COMMENT 'complet / ambulatoire',
  PRIMARY KEY (`id_appareil`),
  CONSTRAINT `fk_appareil_psg` FOREIGN KEY (`id_appareil`) REFERENCES `appareil` (`id_appareil`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareil_psg`
--

LOCK TABLES `appareil_psg` WRITE;
/*!40000 ALTER TABLE `appareil_psg` DISABLE KEYS */;
INSERT INTO `appareil_psg` VALUES (1,'4.2.1','complet'),(2,'4.2.1','complet'),(3,'4.2.3','complet'),(4,'3.1.0','ambulatoire'),(5,'3.1.0','ambulatoire'),(6,'4.3.0','complet'),(7,'2.5.1','complet'),(8,'2.5.1','complet'),(9,'3.2.0','ambulatoire'),(10,'4.3.1','complet');
/*!40000 ALTER TABLE `appareil_psg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bilan_mensuel_cpap`
--

DROP TABLE IF EXISTS `bilan_mensuel_cpap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bilan_mensuel_cpap` (
  `id_bilan` int NOT NULL AUTO_INCREMENT,
  `id_appareil` int NOT NULL,
  `annee` int NOT NULL,
  `mois` int NOT NULL,
  `duree_moy_h` decimal(4,2) DEFAULT NULL,
  `compliance_pct` decimal(5,2) DEFAULT NULL,
  `iah_residuel_moy` decimal(5,2) DEFAULT NULL,
  `fuites_moy` decimal(6,2) DEFAULT NULL,
  `nb_jours_utilises` int DEFAULT NULL,
  `nb_jours_non_utilises` int DEFAULT NULL,
  PRIMARY KEY (`id_bilan`),
  UNIQUE KEY `id_appareil` (`id_appareil`,`annee`,`mois`),
  KEY `idx_bilan_appareil_date` (`id_appareil`,`annee`,`mois`),
  CONSTRAINT `fk_bilan_appareil` FOREIGN KEY (`id_appareil`) REFERENCES `appareil_cpap` (`id_appareil`),
  CONSTRAINT `bilan_mensuel_cpap_chk_1` CHECK ((`annee` >= 2000)),
  CONSTRAINT `bilan_mensuel_cpap_chk_2` CHECK ((`mois` between 1 and 12)),
  CONSTRAINT `bilan_mensuel_cpap_chk_3` CHECK ((`compliance_pct` between 0 and 100)),
  CONSTRAINT `bilan_mensuel_cpap_chk_4` CHECK ((`nb_jours_utilises` >= 0)),
  CONSTRAINT `bilan_mensuel_cpap_chk_5` CHECK ((`nb_jours_non_utilises` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilan_mensuel_cpap`
--

LOCK TABLES `bilan_mensuel_cpap` WRITE;
/*!40000 ALTER TABLE `bilan_mensuel_cpap` DISABLE KEYS */;
/*!40000 ALTER TABLE `bilan_mensuel_cpap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comorbidite`
--

DROP TABLE IF EXISTS `comorbidite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comorbidite` (
  `id_comorbidite` int NOT NULL AUTO_INCREMENT,
  `libelle` varchar(100) NOT NULL,
  `categorie` varchar(50) DEFAULT NULL COMMENT 'cardiovasculaire / mÃ©tabolique / respiratoire / psychiatrique / autre',
  PRIMARY KEY (`id_comorbidite`),
  UNIQUE KEY `libelle` (`libelle`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comorbidite`
--

LOCK TABLES `comorbidite` WRITE;
/*!40000 ALTER TABLE `comorbidite` DISABLE KEYS */;
INSERT INTO `comorbidite` VALUES (1,'Hypertension artÃ©rielle (HTA)','cardiovasculaire'),(2,'DiabÃ¨te de type 2','mÃ©tabolique'),(3,'ObÃ©sitÃ©','mÃ©tabolique'),(4,'Insuffisance cardiaque','cardiovasculaire'),(5,'Fibrillation auriculaire','cardiovasculaire'),(6,'BPCO','respiratoire'),(7,'Asthme','respiratoire'),(8,'HypothyroÃ¯die','mÃ©tabolique'),(9,'DÃ©pression','psychiatrique'),(10,'AnxiÃ©tÃ©','psychiatrique'),(11,'Reflux gastro-oesophagien (RGO)','autre'),(12,'Syndrome mÃ©tabolique','mÃ©tabolique'),(13,'Insuffisance rÃ©nale chronique','autre'),(14,'DyslipidÃ©mie','mÃ©tabolique'),(15,'Accident vasculaire cÃ©rÃ©bral (AVC)','cardiovasculaire');
/*!40000 ALTER TABLE `comorbidite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation`
--

DROP TABLE IF EXISTS `consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultation` (
  `id_consultation` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_medecin` int NOT NULL,
  `date_consultation` date NOT NULL,
  `motif` varchar(255) DEFAULT NULL,
  `compte_rendu` text,
  PRIMARY KEY (`id_consultation`),
  KEY `fk_consul_medecin` (`id_medecin`),
  KEY `idx_consul_patient` (`id_patient`,`date_consultation`),
  CONSTRAINT `fk_consul_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_consul_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation`
--

LOCK TABLES `consultation` WRITE;
/*!40000 ALTER TABLE `consultation` DISABLE KEYS */;
INSERT INTO `consultation` VALUES (1,1,1,'2024-09-15','Ronflements sÃ©vÃ¨res, apnÃ©es observÃ©es par conjointe, somnolence au volant','Homme 56 ans, maÃ§on. IMC 35.8. Fumeur 15 PA. HTA sous traitement. Epworth 17/24. Tension 148/94. Suspicion SAHOS sÃ©vÃ¨re. Risque professionnel conduite engins. PSG complet prescrit en urgence relative.'),(2,1,1,'2024-10-08','Bilan prÃ©-PSG â€” suivi clinique jour J','Patient revu en consultation le jour de la nuit d Ã©tude. Tension 146/92. Poids 99.4kg. Somnolence diurne persistante. Pas de contre-indication. Installation PSG prÃ©vue Ã  21h00.'),(3,2,2,'2024-10-10','Fatigue chronique, ronflements occasionnels, cÃ©phalÃ©es matinales','Femme 44 ans, comptable. IMC 27.4. Non fumeuse. AnxiÃ©tÃ© traitÃ©e. Epworth 9/24. RGO connu. Fatigue matinale invalidante. Polygraphie ambulatoire prescrite pour Ã©liminer SAHOS.'),(4,2,2,'2024-11-05','Bilan prÃ©-polygraphie â€” suivi clinique jour J','Patiente revue en consultation le jour de l enregistrement. Poids 72.8kg. Tension 118/74. Pas de contre-indication. Installation polygraphie prÃ©vue Ã  22h00.');
/*!40000 ALTER TABLE `consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deces_patient`
--

DROP TABLE IF EXISTS `deces_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deces_patient` (
  `id_patient` int NOT NULL,
  `date_deces` date NOT NULL,
  `cause_principale` varchar(255) NOT NULL,
  `cause_secondaire` varchar(255) DEFAULT NULL,
  `lien_apnee` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_patient`),
  CONSTRAINT `fk_deces_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deces_patient`
--

LOCK TABLES `deces_patient` WRITE;
/*!40000 ALTER TABLE `deces_patient` DISABLE KEYS */;
/*!40000 ALTER TABLE `deces_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evenement_respiratoire`
--

DROP TABLE IF EXISTS `evenement_respiratoire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evenement_respiratoire` (
  `id_evenement` int NOT NULL AUTO_INCREMENT,
  `id_nuit` int NOT NULL,
  `type_evenement` varchar(50) NOT NULL,
  `debut_sec` int NOT NULL,
  `fin_sec` int NOT NULL,
  `duree_sec` int GENERATED ALWAYS AS ((`fin_sec` - `debut_sec`)) STORED,
  `severite` varchar(20) DEFAULT NULL,
  `decibels` decimal(5,2) DEFAULT NULL,
  `spo2_avant` decimal(5,2) DEFAULT NULL,
  `spo2_apres` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_evenement`),
  KEY `idx_evenement_nuit` (`id_nuit`),
  KEY `idx_evenement_type` (`type_evenement`),
  CONSTRAINT `fk_evenement_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `evenement_respiratoire_chk_1` CHECK ((`type_evenement` in (_utf8mb4'apnÃ©e obstructive',_utf8mb4'apnÃ©e centrale',_utf8mb4'hypopnÃ©e',_utf8mb4'RERA'))),
  CONSTRAINT `evenement_respiratoire_chk_2` CHECK ((`debut_sec` >= 0)),
  CONSTRAINT `evenement_respiratoire_chk_3` CHECK ((`severite` in (_utf8mb4'lÃ©gÃ¨re',_utf8mb4'modÃ©rÃ©e',_utf8mb4'sÃ©vÃ¨re'))),
  CONSTRAINT `evenement_respiratoire_chk_4` CHECK ((`spo2_avant` between 0 and 100)),
  CONSTRAINT `evenement_respiratoire_chk_5` CHECK ((`spo2_apres` between 0 and 100)),
  CONSTRAINT `evenement_respiratoire_chk_6` CHECK ((`fin_sec` > `debut_sec`))
) ENGINE=InnoDB AUTO_INCREMENT=799 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evenement_respiratoire`
--

LOCK TABLES `evenement_respiratoire` WRITE;
/*!40000 ALTER TABLE `evenement_respiratoire` DISABLE KEYS */;
INSERT INTO `evenement_respiratoire` (`id_evenement`, `id_nuit`, `type_evenement`, `debut_sec`, `fin_sec`, `severite`, `decibels`, `spo2_avant`, `spo2_apres`) VALUES (455,1,'apnÃ©e obstructive',90,155,'sÃ©vÃ¨re',69.80,94.80,80.00),(456,1,'apnÃ©e obstructive',162,204,'sÃ©vÃ¨re',73.60,95.30,75.30),(457,1,'hypopnÃ©e',272,305,'modÃ©rÃ©e',54.40,95.50,88.70),(458,1,'apnÃ©e obstructive',323,382,'sÃ©vÃ¨re',76.00,95.20,78.00),(459,1,'RERA',405,457,'lÃ©gÃ¨re',42.50,95.60,93.60),(460,1,'apnÃ©e obstructive',500,530,'sÃ©vÃ¨re',70.40,95.10,81.30),(461,1,'apnÃ©e obstructive',604,661,'sÃ©vÃ¨re',66.50,95.20,77.10),(462,1,'apnÃ©e obstructive',668,728,'sÃ©vÃ¨re',69.70,94.60,78.70),(463,1,'apnÃ©e obstructive',764,823,'sÃ©vÃ¨re',71.70,95.20,76.20),(464,1,'hypopnÃ©e',858,911,'modÃ©rÃ©e',54.50,95.50,87.50),(465,1,'hypopnÃ©e',951,976,'modÃ©rÃ©e',55.40,95.60,85.60),(466,1,'apnÃ©e obstructive',1033,1068,'sÃ©vÃ¨re',70.60,94.70,76.80),(467,1,'RERA',1096,1142,'lÃ©gÃ¨re',42.00,95.70,93.70),(468,1,'apnÃ©e obstructive',1216,1254,'sÃ©vÃ¨re',72.80,94.60,78.10),(469,1,'apnÃ©e obstructive',1341,1390,'sÃ©vÃ¨re',69.50,95.00,79.50),(470,1,'apnÃ©e obstructive',1452,1499,'sÃ©vÃ¨re',70.20,94.70,80.90),(471,1,'apnÃ©e obstructive',1543,1570,'sÃ©vÃ¨re',68.00,94.80,78.40),(472,1,'apnÃ©e obstructive',1597,1656,'sÃ©vÃ¨re',68.40,95.00,79.00),(473,1,'apnÃ©e obstructive',1680,1729,'sÃ©vÃ¨re',75.90,94.80,81.80),(474,1,'apnÃ©e obstructive',1803,1846,'sÃ©vÃ¨re',72.60,94.70,79.00),(475,1,'hypopnÃ©e',1890,1954,'modÃ©rÃ©e',58.10,95.50,85.20),(476,1,'apnÃ©e obstructive',2017,2046,'sÃ©vÃ¨re',72.10,94.90,81.30),(477,1,'apnÃ©e obstructive',2139,2178,'sÃ©vÃ¨re',68.90,95.20,79.20),(478,1,'hypopnÃ©e',2228,2258,'modÃ©rÃ©e',56.10,95.50,87.50),(479,1,'apnÃ©e obstructive',2289,2320,'sÃ©vÃ¨re',72.80,95.10,79.60),(480,1,'apnÃ©e obstructive',2386,2440,'sÃ©vÃ¨re',74.40,95.10,81.30),(481,1,'apnÃ©e obstructive',2447,2495,'sÃ©vÃ¨re',72.50,94.80,78.10),(482,1,'hypopnÃ©e',2534,2581,'modÃ©rÃ©e',57.50,95.50,85.40),(483,1,'apnÃ©e centrale',2644,2686,'modÃ©rÃ©e',40.10,95.30,87.50),(484,1,'apnÃ©e obstructive',2724,2753,'sÃ©vÃ¨re',67.30,95.00,81.80),(485,1,'apnÃ©e obstructive',2805,2840,'sÃ©vÃ¨re',71.30,95.30,80.80),(486,1,'hypopnÃ©e',2871,2911,'modÃ©rÃ©e',55.50,95.50,86.90),(487,1,'RERA',2961,3010,'lÃ©gÃ¨re',46.00,95.70,92.00),(488,1,'apnÃ©e obstructive',3067,3132,'sÃ©vÃ¨re',67.20,95.40,76.00),(489,1,'hypopnÃ©e',3152,3191,'modÃ©rÃ©e',59.80,95.50,87.90),(490,1,'apnÃ©e obstructive',3214,3242,'sÃ©vÃ¨re',75.80,95.40,80.60),(491,1,'apnÃ©e obstructive',3328,3355,'sÃ©vÃ¨re',69.70,95.20,75.10),(492,1,'apnÃ©e obstructive',3385,3435,'sÃ©vÃ¨re',71.40,94.90,79.70),(493,1,'apnÃ©e obstructive',3503,3541,'sÃ©vÃ¨re',72.70,95.00,80.80),(494,1,'apnÃ©e obstructive',3586,3647,'sÃ©vÃ¨re',75.40,94.60,76.60),(495,1,'apnÃ©e obstructive',3731,3787,'sÃ©vÃ¨re',66.30,95.30,78.90),(496,1,'apnÃ©e obstructive',3803,3857,'sÃ©vÃ¨re',75.20,94.70,75.40),(497,1,'apnÃ©e centrale',3893,3926,'modÃ©rÃ©e',43.80,95.40,87.90),(498,1,'apnÃ©e obstructive',3993,4053,'sÃ©vÃ¨re',70.10,94.60,81.60),(499,1,'apnÃ©e obstructive',4072,4134,'sÃ©vÃ¨re',69.00,94.90,75.70),(500,1,'apnÃ©e obstructive',4155,4217,'sÃ©vÃ¨re',74.90,94.60,78.20),(501,1,'apnÃ©e centrale',4270,4309,'modÃ©rÃ©e',42.70,95.30,89.80),(502,1,'apnÃ©e obstructive',4330,4363,'sÃ©vÃ¨re',70.20,95.20,76.10),(503,1,'apnÃ©e obstructive',4428,4458,'sÃ©vÃ¨re',70.10,94.60,78.40),(504,1,'apnÃ©e obstructive',4482,4514,'sÃ©vÃ¨re',70.10,95.40,75.20),(505,1,'apnÃ©e obstructive',4599,4634,'sÃ©vÃ¨re',69.70,94.90,81.70),(506,1,'apnÃ©e obstructive',4674,4726,'sÃ©vÃ¨re',74.60,94.60,79.80),(507,1,'apnÃ©e obstructive',4748,4797,'sÃ©vÃ¨re',71.40,95.40,77.50),(508,1,'apnÃ©e obstructive',4840,4894,'sÃ©vÃ¨re',70.00,94.70,75.90),(509,1,'apnÃ©e centrale',4942,5002,'modÃ©rÃ©e',43.90,95.20,89.00),(510,1,'apnÃ©e obstructive',5017,5042,'sÃ©vÃ¨re',72.40,95.00,75.10),(511,1,'hypopnÃ©e',5102,5134,'modÃ©rÃ©e',58.70,95.30,85.50),(512,1,'apnÃ©e obstructive',5191,5250,'sÃ©vÃ¨re',71.60,94.60,80.40),(513,1,'apnÃ©e obstructive',5330,5382,'sÃ©vÃ¨re',68.10,94.70,81.10),(514,1,'apnÃ©e obstructive',5455,5480,'sÃ©vÃ¨re',69.30,94.60,81.30),(515,1,'hypopnÃ©e',5541,5582,'modÃ©rÃ©e',54.00,95.50,85.60),(516,1,'apnÃ©e obstructive',5602,5638,'sÃ©vÃ¨re',67.30,94.70,76.20),(517,1,'apnÃ©e centrale',5705,5736,'modÃ©rÃ©e',42.60,95.00,87.00),(518,1,'apnÃ©e obstructive',5789,5833,'sÃ©vÃ¨re',73.90,94.70,77.30),(519,1,'apnÃ©e centrale',5862,5919,'modÃ©rÃ©e',39.20,95.00,89.20),(520,1,'apnÃ©e obstructive',5935,5969,'sÃ©vÃ¨re',71.30,95.20,78.30),(521,1,'RERA',6028,6063,'lÃ©gÃ¨re',45.90,95.60,91.30),(522,1,'apnÃ©e obstructive',6132,6190,'sÃ©vÃ¨re',71.00,95.40,75.30),(523,1,'apnÃ©e obstructive',6260,6286,'sÃ©vÃ¨re',73.80,95.30,78.70),(524,1,'apnÃ©e obstructive',6384,6432,'sÃ©vÃ¨re',70.60,95.40,75.40),(525,1,'hypopnÃ©e',6554,6594,'modÃ©rÃ©e',56.90,95.40,87.70),(526,1,'apnÃ©e obstructive',6720,6776,'sÃ©vÃ¨re',70.90,95.30,75.50),(527,1,'apnÃ©e obstructive',6802,6861,'sÃ©vÃ¨re',66.80,95.00,75.50),(528,1,'apnÃ©e obstructive',6882,6915,'sÃ©vÃ¨re',68.80,95.10,78.80),(529,1,'apnÃ©e obstructive',6941,7001,'sÃ©vÃ¨re',69.30,95.40,78.70),(530,1,'apnÃ©e obstructive',7062,7120,'sÃ©vÃ¨re',70.50,95.00,75.70),(531,1,'apnÃ©e obstructive',7152,7204,'sÃ©vÃ¨re',73.00,95.30,79.60),(532,1,'apnÃ©e obstructive',7226,7285,'sÃ©vÃ¨re',73.70,95.10,76.50),(533,1,'apnÃ©e obstructive',7308,7345,'sÃ©vÃ¨re',70.50,94.70,77.40),(534,1,'RERA',7408,7458,'lÃ©gÃ¨re',44.30,95.50,91.30),(535,1,'apnÃ©e obstructive',7464,7512,'sÃ©vÃ¨re',70.30,95.10,77.60),(536,1,'apnÃ©e obstructive',7550,7608,'sÃ©vÃ¨re',67.50,95.30,75.50),(537,1,'apnÃ©e centrale',7623,7663,'modÃ©rÃ©e',43.80,95.00,87.30),(538,1,'hypopnÃ©e',7697,7743,'modÃ©rÃ©e',58.40,95.50,87.20),(539,1,'apnÃ©e obstructive',7793,7853,'sÃ©vÃ¨re',71.90,95.00,77.30),(540,1,'apnÃ©e obstructive',7866,7905,'sÃ©vÃ¨re',67.20,94.80,79.70),(541,1,'apnÃ©e obstructive',7954,8019,'sÃ©vÃ¨re',73.50,95.30,80.00),(542,1,'apnÃ©e obstructive',8081,8110,'sÃ©vÃ¨re',75.70,95.00,77.50),(543,1,'apnÃ©e obstructive',8124,8170,'sÃ©vÃ¨re',71.80,94.70,79.60),(544,1,'apnÃ©e obstructive',8219,8259,'sÃ©vÃ¨re',68.20,94.60,80.90),(545,1,'apnÃ©e obstructive',8301,8357,'sÃ©vÃ¨re',69.70,95.20,79.00),(546,1,'apnÃ©e obstructive',8411,8444,'sÃ©vÃ¨re',74.10,95.30,81.80),(547,1,'apnÃ©e obstructive',8489,8550,'sÃ©vÃ¨re',74.20,95.10,79.50),(548,1,'apnÃ©e obstructive',8584,8624,'sÃ©vÃ¨re',66.30,95.30,80.80),(549,1,'apnÃ©e obstructive',8639,8690,'sÃ©vÃ¨re',68.70,94.70,79.90),(550,1,'apnÃ©e obstructive',8747,8778,'sÃ©vÃ¨re',69.10,94.80,75.00),(551,1,'apnÃ©e obstructive',8820,8867,'sÃ©vÃ¨re',74.70,95.00,77.80),(552,1,'hypopnÃ©e',8927,8981,'modÃ©rÃ©e',54.90,95.50,85.10),(553,1,'apnÃ©e obstructive',9002,9030,'sÃ©vÃ¨re',73.50,94.70,77.90),(554,1,'apnÃ©e obstructive',9056,9087,'sÃ©vÃ¨re',69.40,94.80,80.10),(555,1,'apnÃ©e obstructive',9178,9224,'sÃ©vÃ¨re',73.80,95.00,75.60),(556,1,'apnÃ©e obstructive',9235,9266,'sÃ©vÃ¨re',66.50,94.60,79.30),(557,1,'apnÃ©e obstructive',9335,9372,'sÃ©vÃ¨re',72.70,94.70,79.60),(558,1,'apnÃ©e obstructive',9414,9447,'sÃ©vÃ¨re',70.90,94.90,76.90),(559,1,'apnÃ©e obstructive',9500,9542,'sÃ©vÃ¨re',73.50,94.60,78.00),(560,1,'hypopnÃ©e',9584,9613,'modÃ©rÃ©e',55.70,95.50,86.90),(561,1,'apnÃ©e obstructive',9651,9711,'sÃ©vÃ¨re',72.70,94.50,77.80),(562,1,'apnÃ©e obstructive',9774,9833,'sÃ©vÃ¨re',72.00,94.50,77.10),(563,1,'apnÃ©e obstructive',9863,9893,'sÃ©vÃ¨re',68.10,94.60,76.80),(564,1,'RERA',9909,9949,'lÃ©gÃ¨re',43.60,95.30,93.20),(565,1,'apnÃ©e obstructive',10010,10066,'sÃ©vÃ¨re',67.80,94.80,79.90),(566,1,'hypopnÃ©e',10116,10166,'modÃ©rÃ©e',57.00,95.50,88.20),(567,1,'apnÃ©e obstructive',10175,10210,'sÃ©vÃ¨re',66.70,95.30,75.30),(568,1,'apnÃ©e centrale',10254,10303,'modÃ©rÃ©e',38.10,95.40,89.60),(569,1,'hypopnÃ©e',10339,10393,'modÃ©rÃ©e',57.50,95.40,87.80),(570,1,'apnÃ©e obstructive',10443,10503,'sÃ©vÃ¨re',70.20,94.60,75.10),(571,1,'apnÃ©e obstructive',10590,10633,'sÃ©vÃ¨re',69.20,95.20,79.30),(572,1,'apnÃ©e obstructive',10694,10722,'sÃ©vÃ¨re',74.30,95.30,75.60),(573,1,'apnÃ©e obstructive',10752,10811,'sÃ©vÃ¨re',74.40,94.70,79.10),(574,1,'apnÃ©e obstructive',10837,10882,'sÃ©vÃ¨re',71.20,94.90,77.20),(575,1,'apnÃ©e obstructive',10943,11005,'sÃ©vÃ¨re',69.40,94.80,76.20),(576,1,'apnÃ©e obstructive',11011,11069,'sÃ©vÃ¨re',71.10,94.60,78.60),(577,1,'hypopnÃ©e',11092,11149,'modÃ©rÃ©e',59.40,95.30,87.90),(578,1,'apnÃ©e obstructive',11176,11212,'sÃ©vÃ¨re',74.20,95.20,76.70),(579,1,'apnÃ©e obstructive',11292,11321,'sÃ©vÃ¨re',67.50,94.70,79.20),(580,1,'apnÃ©e centrale',11363,11403,'modÃ©rÃ©e',43.30,95.30,87.50),(581,1,'apnÃ©e obstructive',11440,11501,'sÃ©vÃ¨re',73.70,94.90,80.30),(582,1,'apnÃ©e obstructive',11514,11577,'sÃ©vÃ¨re',73.60,94.90,81.50),(583,1,'apnÃ©e obstructive',11618,11648,'sÃ©vÃ¨re',71.60,95.10,79.40),(584,1,'apnÃ©e obstructive',11710,11772,'sÃ©vÃ¨re',74.60,95.10,76.10),(585,1,'apnÃ©e obstructive',11814,11859,'sÃ©vÃ¨re',66.70,94.90,77.10),(586,1,'apnÃ©e obstructive',11885,11923,'sÃ©vÃ¨re',68.70,94.60,78.60),(587,1,'apnÃ©e obstructive',11948,11993,'sÃ©vÃ¨re',69.10,94.90,75.40),(588,1,'hypopnÃ©e',12027,12077,'modÃ©rÃ©e',59.00,95.20,88.50),(589,1,'apnÃ©e obstructive',12129,12173,'sÃ©vÃ¨re',74.60,95.10,78.50),(590,1,'apnÃ©e obstructive',12191,12220,'sÃ©vÃ¨re',70.60,95.00,80.50),(591,1,'apnÃ©e obstructive',12326,12390,'sÃ©vÃ¨re',75.00,94.90,80.70),(592,1,'hypopnÃ©e',12471,12509,'modÃ©rÃ©e',57.90,95.30,86.90),(593,1,'apnÃ©e obstructive',12577,12610,'sÃ©vÃ¨re',67.50,94.60,75.70),(594,1,'apnÃ©e obstructive',12659,12688,'sÃ©vÃ¨re',75.00,94.80,80.00),(595,1,'apnÃ©e obstructive',12714,12762,'sÃ©vÃ¨re',71.00,94.70,76.70),(596,1,'apnÃ©e obstructive',12826,12879,'sÃ©vÃ¨re',70.40,94.90,78.70),(597,1,'apnÃ©e obstructive',12900,12944,'sÃ©vÃ¨re',67.60,94.80,77.00),(598,1,'apnÃ©e obstructive',12954,13012,'sÃ©vÃ¨re',70.10,94.80,79.20),(599,1,'hypopnÃ©e',13054,13114,'modÃ©rÃ©e',58.70,95.50,85.30),(600,1,'apnÃ©e obstructive',13171,13202,'sÃ©vÃ¨re',66.90,95.10,77.00),(601,1,'apnÃ©e obstructive',13221,13254,'sÃ©vÃ¨re',73.20,95.10,81.30),(602,1,'apnÃ©e obstructive',13330,13361,'sÃ©vÃ¨re',74.70,94.80,79.10),(603,1,'hypopnÃ©e',13391,13425,'modÃ©rÃ©e',54.80,95.30,88.90),(604,1,'apnÃ©e obstructive',13473,13536,'sÃ©vÃ¨re',73.00,94.90,79.20),(605,1,'RERA',13557,13603,'lÃ©gÃ¨re',46.70,95.50,92.10),(606,1,'hypopnÃ©e',13675,13740,'modÃ©rÃ©e',58.70,95.50,87.70),(607,1,'apnÃ©e obstructive',13806,13834,'sÃ©vÃ¨re',74.30,95.20,79.80),(608,1,'apnÃ©e obstructive',13928,13980,'sÃ©vÃ¨re',71.30,95.10,78.00),(609,1,'apnÃ©e obstructive',14088,14121,'sÃ©vÃ¨re',69.60,94.80,76.30),(610,1,'hypopnÃ©e',14149,14190,'modÃ©rÃ©e',55.30,95.60,86.90),(611,1,'apnÃ©e obstructive',14254,14307,'sÃ©vÃ¨re',68.30,94.60,75.50),(612,1,'apnÃ©e obstructive',14339,14391,'sÃ©vÃ¨re',74.40,94.60,80.40),(613,1,'hypopnÃ©e',14399,14431,'modÃ©rÃ©e',59.00,95.60,85.20),(614,1,'apnÃ©e obstructive',14508,14542,'sÃ©vÃ¨re',69.40,95.20,75.90),(615,1,'RERA',14594,14642,'lÃ©gÃ¨re',43.90,95.40,93.50),(616,1,'apnÃ©e obstructive',14671,14705,'sÃ©vÃ¨re',73.70,95.20,76.20),(617,1,'apnÃ©e obstructive',14750,14777,'sÃ©vÃ¨re',70.40,94.90,79.70),(618,1,'apnÃ©e obstructive',14865,14892,'sÃ©vÃ¨re',68.40,94.90,77.00),(619,1,'apnÃ©e obstructive',14939,14977,'sÃ©vÃ¨re',73.50,94.90,78.70),(620,1,'apnÃ©e obstructive',15007,15038,'sÃ©vÃ¨re',69.10,95.20,78.30),(621,1,'apnÃ©e obstructive',15118,15178,'sÃ©vÃ¨re',74.40,94.80,81.60),(622,1,'apnÃ©e obstructive',15208,15259,'sÃ©vÃ¨re',75.80,94.90,77.00),(623,1,'apnÃ©e obstructive',15290,15324,'sÃ©vÃ¨re',69.80,95.00,81.80),(624,1,'apnÃ©e obstructive',15372,15412,'sÃ©vÃ¨re',74.20,95.20,76.00),(625,1,'apnÃ©e obstructive',15457,15493,'sÃ©vÃ¨re',68.50,95.10,81.10),(626,1,'apnÃ©e obstructive',15507,15533,'sÃ©vÃ¨re',71.50,94.60,80.90),(627,1,'hypopnÃ©e',15622,15668,'modÃ©rÃ©e',59.10,95.30,88.10),(628,1,'apnÃ©e obstructive',15708,15759,'sÃ©vÃ¨re',68.70,95.30,76.00),(629,1,'apnÃ©e obstructive',15765,15805,'sÃ©vÃ¨re',70.40,95.40,76.60),(630,1,'apnÃ©e obstructive',15856,15887,'sÃ©vÃ¨re',70.50,94.80,75.20),(631,1,'apnÃ©e obstructive',15965,15992,'sÃ©vÃ¨re',66.50,95.00,76.70),(632,1,'apnÃ©e obstructive',16016,16055,'sÃ©vÃ¨re',75.90,94.80,75.20),(633,1,'apnÃ©e obstructive',16109,16163,'sÃ©vÃ¨re',75.30,95.30,79.50),(634,1,'apnÃ©e obstructive',16187,16226,'sÃ©vÃ¨re',73.90,94.60,77.00),(635,1,'hypopnÃ©e',16281,16318,'modÃ©rÃ©e',59.00,95.50,85.60),(636,1,'apnÃ©e obstructive',16389,16431,'sÃ©vÃ¨re',73.10,94.90,75.00),(637,1,'apnÃ©e centrale',16448,16490,'modÃ©rÃ©e',38.60,95.10,89.50),(638,1,'RERA',16535,16592,'lÃ©gÃ¨re',44.70,95.70,92.60),(639,1,'apnÃ©e obstructive',16617,16676,'sÃ©vÃ¨re',67.10,94.80,77.10),(640,1,'apnÃ©e obstructive',16690,16716,'sÃ©vÃ¨re',66.50,94.90,80.60),(641,1,'apnÃ©e obstructive',16778,16819,'sÃ©vÃ¨re',70.60,94.60,81.30),(642,1,'apnÃ©e obstructive',16856,16897,'sÃ©vÃ¨re',72.00,94.50,78.60),(643,1,'apnÃ©e obstructive',16961,17024,'sÃ©vÃ¨re',68.40,94.60,78.00),(644,1,'apnÃ©e obstructive',17046,17091,'sÃ©vÃ¨re',72.10,94.70,77.90),(645,1,'apnÃ©e obstructive',17114,17171,'sÃ©vÃ¨re',72.60,94.60,81.80),(646,1,'apnÃ©e obstructive',17203,17264,'sÃ©vÃ¨re',66.70,95.00,78.60),(647,1,'apnÃ©e obstructive',17314,17341,'sÃ©vÃ¨re',75.90,95.00,77.70),(648,1,'apnÃ©e obstructive',17389,17414,'sÃ©vÃ¨re',70.70,95.10,81.90),(649,1,'apnÃ©e obstructive',17483,17542,'sÃ©vÃ¨re',68.50,94.50,80.50),(650,1,'apnÃ©e obstructive',17551,17588,'sÃ©vÃ¨re',69.40,95.20,79.40),(651,1,'apnÃ©e obstructive',17666,17695,'sÃ©vÃ¨re',73.70,95.20,77.30),(652,1,'apnÃ©e obstructive',17734,17780,'sÃ©vÃ¨re',66.40,95.00,80.70),(653,1,'apnÃ©e obstructive',17824,17856,'sÃ©vÃ¨re',67.80,95.20,78.30),(654,1,'apnÃ©e obstructive',17898,17942,'sÃ©vÃ¨re',73.00,95.10,80.70),(655,1,'apnÃ©e obstructive',17973,18024,'sÃ©vÃ¨re',66.60,95.20,78.20),(656,1,'apnÃ©e obstructive',18070,18113,'sÃ©vÃ¨re',68.90,94.50,76.40),(657,1,'apnÃ©e obstructive',18147,18184,'sÃ©vÃ¨re',66.40,95.30,78.60),(658,1,'apnÃ©e centrale',18245,18294,'modÃ©rÃ©e',44.90,95.20,87.80),(659,1,'hypopnÃ©e',18327,18363,'modÃ©rÃ©e',58.50,95.30,86.40),(660,1,'apnÃ©e obstructive',18401,18445,'sÃ©vÃ¨re',73.80,95.30,77.30),(661,1,'apnÃ©e obstructive',18481,18506,'sÃ©vÃ¨re',67.20,94.80,81.20),(662,1,'apnÃ©e obstructive',18572,18610,'sÃ©vÃ¨re',73.40,95.30,77.70),(663,1,'apnÃ©e obstructive',18666,18728,'sÃ©vÃ¨re',75.70,94.90,78.50),(664,1,'apnÃ©e obstructive',18743,18788,'sÃ©vÃ¨re',75.20,95.00,80.60),(665,1,'apnÃ©e obstructive',18839,18892,'sÃ©vÃ¨re',73.30,94.60,79.20),(666,1,'apnÃ©e obstructive',18913,18970,'sÃ©vÃ¨re',74.20,95.00,77.20),(667,1,'apnÃ©e obstructive',19008,19043,'sÃ©vÃ¨re',66.80,95.10,77.10),(668,1,'apnÃ©e obstructive',19085,19128,'sÃ©vÃ¨re',72.00,94.90,79.80),(669,1,'RERA',19175,19240,'lÃ©gÃ¨re',43.80,95.30,93.60),(670,1,'apnÃ©e obstructive',19270,19300,'sÃ©vÃ¨re',69.50,95.40,76.90),(671,1,'apnÃ©e obstructive',19347,19387,'sÃ©vÃ¨re',75.80,95.40,75.50),(672,1,'apnÃ©e obstructive',19439,19478,'sÃ©vÃ¨re',72.40,94.80,80.60),(673,1,'apnÃ©e centrale',19484,19518,'modÃ©rÃ©e',42.80,95.40,87.40),(674,1,'apnÃ©e obstructive',19618,19658,'sÃ©vÃ¨re',72.10,95.20,75.20),(675,1,'RERA',19696,19760,'lÃ©gÃ¨re',42.30,95.70,92.10),(676,1,'apnÃ©e obstructive',19851,19916,'sÃ©vÃ¨re',69.80,95.00,79.20),(677,1,'apnÃ©e obstructive',19932,19981,'sÃ©vÃ¨re',72.80,95.40,77.60),(678,1,'apnÃ©e obstructive',19999,20039,'sÃ©vÃ¨re',73.60,95.00,78.70),(679,1,'apnÃ©e obstructive',20122,20147,'sÃ©vÃ¨re',70.00,95.10,76.70),(680,1,'apnÃ©e obstructive',20201,20232,'sÃ©vÃ¨re',67.10,95.20,78.50),(681,1,'apnÃ©e obstructive',20255,20294,'sÃ©vÃ¨re',69.90,95.00,76.80),(682,1,'apnÃ©e obstructive',20354,20412,'sÃ©vÃ¨re',68.60,94.90,82.00),(683,1,'apnÃ©e obstructive',20428,20488,'sÃ©vÃ¨re',68.90,95.30,78.40),(684,1,'apnÃ©e obstructive',20524,20556,'sÃ©vÃ¨re',67.20,95.30,78.20),(685,1,'apnÃ©e centrale',20619,20673,'modÃ©rÃ©e',44.30,95.20,87.30),(686,1,'apnÃ©e obstructive',20700,20760,'sÃ©vÃ¨re',72.80,95.30,77.20),(687,1,'apnÃ©e centrale',20786,20839,'modÃ©rÃ©e',40.40,95.00,88.60),(688,1,'hypopnÃ©e',20861,20918,'modÃ©rÃ©e',59.30,95.50,87.80),(689,1,'apnÃ©e obstructive',20947,21007,'sÃ©vÃ¨re',75.30,95.10,80.60),(690,1,'RERA',21047,21082,'lÃ©gÃ¨re',44.50,95.40,91.60),(691,1,'apnÃ©e obstructive',21117,21172,'sÃ©vÃ¨re',67.40,95.20,75.20),(692,1,'apnÃ©e centrale',21221,21261,'modÃ©rÃ©e',41.90,95.10,89.40),(693,1,'apnÃ©e obstructive',21303,21345,'sÃ©vÃ¨re',71.50,95.10,75.60),(694,1,'apnÃ©e obstructive',21373,21431,'sÃ©vÃ¨re',69.10,95.40,80.00),(695,1,'apnÃ©e centrale',21447,21487,'modÃ©rÃ©e',41.70,95.30,89.50),(696,1,'apnÃ©e obstructive',21554,21583,'sÃ©vÃ¨re',66.70,95.40,79.50),(697,1,'apnÃ©e obstructive',21617,21657,'sÃ©vÃ¨re',70.50,95.10,77.40),(698,1,'apnÃ©e obstructive',21733,21778,'sÃ©vÃ¨re',74.80,95.20,79.50),(699,1,'apnÃ©e obstructive',21877,21916,'sÃ©vÃ¨re',67.80,95.40,78.00),(700,1,'apnÃ©e obstructive',21978,22012,'sÃ©vÃ¨re',75.10,94.50,75.90),(701,1,'apnÃ©e obstructive',22048,22077,'sÃ©vÃ¨re',67.50,94.60,77.30),(702,1,'apnÃ©e obstructive',22139,22185,'sÃ©vÃ¨re',73.10,94.80,81.60),(703,1,'apnÃ©e obstructive',22199,22250,'sÃ©vÃ¨re',74.90,95.30,76.80),(704,1,'apnÃ©e obstructive',22301,22352,'sÃ©vÃ¨re',72.40,95.00,75.90),(705,1,'apnÃ©e obstructive',22414,22476,'sÃ©vÃ¨re',69.00,95.00,78.50),(706,1,'hypopnÃ©e',22494,22520,'modÃ©rÃ©e',55.00,95.60,85.60),(707,1,'apnÃ©e obstructive',22555,22616,'sÃ©vÃ¨re',72.60,95.10,79.20),(708,1,'apnÃ©e obstructive',22668,22693,'sÃ©vÃ¨re',74.40,95.00,80.80),(709,1,'apnÃ©e obstructive',22743,22787,'sÃ©vÃ¨re',66.30,94.50,79.50),(710,1,'apnÃ©e obstructive',22817,22868,'sÃ©vÃ¨re',71.80,95.10,80.40),(711,1,'apnÃ©e obstructive',22915,22974,'sÃ©vÃ¨re',70.20,95.10,78.50),(712,1,'apnÃ©e obstructive',22984,23023,'sÃ©vÃ¨re',72.30,94.80,81.70),(713,1,'hypopnÃ©e',23066,23108,'modÃ©rÃ©e',56.90,95.50,87.70),(714,1,'apnÃ©e obstructive',23149,23175,'sÃ©vÃ¨re',69.00,94.60,75.40),(715,1,'hypopnÃ©e',23251,23301,'modÃ©rÃ©e',56.60,95.40,85.80),(716,1,'apnÃ©e obstructive',23345,23399,'sÃ©vÃ¨re',72.10,94.80,80.00),(717,1,'apnÃ©e obstructive',23411,23475,'sÃ©vÃ¨re',73.30,95.30,81.80),(718,1,'hypopnÃ©e',23498,23548,'modÃ©rÃ©e',54.80,95.30,87.20),(719,1,'apnÃ©e obstructive',23557,23583,'sÃ©vÃ¨re',69.20,94.90,76.90),(720,1,'apnÃ©e obstructive',23645,23697,'sÃ©vÃ¨re',68.50,94.60,77.00),(721,1,'apnÃ©e centrale',23732,23786,'modÃ©rÃ©e',40.70,95.20,87.70),(722,1,'apnÃ©e obstructive',23827,23868,'sÃ©vÃ¨re',74.70,94.60,77.30),(723,1,'apnÃ©e centrale',23915,23953,'modÃ©rÃ©e',42.00,95.10,89.30),(724,1,'apnÃ©e obstructive',24016,24062,'sÃ©vÃ¨re',71.00,95.00,78.50),(725,1,'apnÃ©e obstructive',24076,24125,'sÃ©vÃ¨re',69.10,94.50,81.60),(726,1,'apnÃ©e obstructive',24159,24210,'sÃ©vÃ¨re',71.10,95.40,76.50),(727,1,'apnÃ©e obstructive',24255,24285,'sÃ©vÃ¨re',69.50,94.50,78.50),(728,1,'apnÃ©e obstructive',24319,24378,'sÃ©vÃ¨re',74.80,95.10,78.30),(729,1,'apnÃ©e centrale',24412,24459,'modÃ©rÃ©e',41.80,95.30,88.30),(730,1,'apnÃ©e obstructive',24526,24555,'sÃ©vÃ¨re',74.80,95.20,80.30),(731,1,'apnÃ©e obstructive',24609,24636,'sÃ©vÃ¨re',69.70,94.90,79.00),(732,1,'apnÃ©e obstructive',24666,24706,'sÃ©vÃ¨re',67.90,95.00,75.50),(733,1,'apnÃ©e obstructive',24772,24798,'sÃ©vÃ¨re',71.00,95.20,77.00),(734,1,'apnÃ©e obstructive',24831,24871,'sÃ©vÃ¨re',75.90,95.10,75.80),(735,1,'apnÃ©e obstructive',24938,24970,'sÃ©vÃ¨re',75.80,94.90,80.60),(736,2,'hypopnÃ©e',90,114,'lÃ©gÃ¨re',44.00,97.50,91.40),(737,2,'hypopnÃ©e',563,586,'lÃ©gÃ¨re',43.20,97.30,90.30),(738,2,'hypopnÃ©e',867,883,'lÃ©gÃ¨re',42.30,97.10,89.50),(739,2,'hypopnÃ©e',1322,1341,'lÃ©gÃ¨re',44.80,97.20,90.70),(740,2,'hypopnÃ©e',1650,1673,'lÃ©gÃ¨re',45.10,97.20,90.80),(741,2,'hypopnÃ©e',2069,2085,'lÃ©gÃ¨re',43.00,97.50,91.30),(742,2,'hypopnÃ©e',2450,2469,'lÃ©gÃ¨re',43.80,97.20,91.70),(743,2,'hypopnÃ©e',2751,2772,'lÃ©gÃ¨re',45.20,97.40,89.30),(744,2,'hypopnÃ©e',3311,3329,'lÃ©gÃ¨re',46.90,97.20,91.00),(745,2,'hypopnÃ©e',3592,3613,'lÃ©gÃ¨re',47.90,97.30,91.60),(746,2,'hypopnÃ©e',3983,3996,'lÃ©gÃ¨re',46.40,97.30,88.10),(747,2,'RERA',4523,4545,'lÃ©gÃ¨re',38.90,97.70,95.60),(748,2,'hypopnÃ©e',4859,4880,'lÃ©gÃ¨re',46.70,97.30,91.20),(749,2,'hypopnÃ©e',5353,5365,'lÃ©gÃ¨re',45.50,97.10,90.80),(750,2,'hypopnÃ©e',5706,5728,'lÃ©gÃ¨re',45.70,97.40,88.70),(751,2,'hypopnÃ©e',5917,5938,'lÃ©gÃ¨re',46.10,97.00,92.30),(752,2,'hypopnÃ©e',6344,6368,'lÃ©gÃ¨re',42.70,97.00,89.40),(753,2,'RERA',6853,6873,'lÃ©gÃ¨re',37.60,97.60,94.80),(754,2,'hypopnÃ©e',7137,7153,'lÃ©gÃ¨re',46.60,97.50,91.90),(755,2,'hypopnÃ©e',7593,7614,'lÃ©gÃ¨re',46.40,97.00,88.60),(756,2,'hypopnÃ©e',8002,8027,'lÃ©gÃ¨re',43.20,97.20,91.00),(757,2,'hypopnÃ©e',8393,8406,'lÃ©gÃ¨re',45.20,97.20,88.80),(758,2,'RERA',8756,8774,'lÃ©gÃ¨re',40.60,97.40,94.70),(759,2,'hypopnÃ©e',9098,9120,'lÃ©gÃ¨re',46.60,97.40,90.90),(760,2,'hypopnÃ©e',9547,9561,'lÃ©gÃ¨re',46.20,97.30,88.90),(761,2,'hypopnÃ©e',9982,10005,'lÃ©gÃ¨re',43.50,97.30,89.00),(762,2,'RERA',10484,10506,'lÃ©gÃ¨re',40.90,97.40,94.60),(763,2,'hypopnÃ©e',10836,10861,'lÃ©gÃ¨re',43.20,97.40,89.40),(764,2,'RERA',11159,11171,'lÃ©gÃ¨re',38.40,97.70,95.60),(765,2,'hypopnÃ©e',11507,11524,'lÃ©gÃ¨re',43.60,97.10,91.00),(766,2,'hypopnÃ©e',12073,12086,'lÃ©gÃ¨re',44.30,97.50,91.70),(767,2,'hypopnÃ©e',12444,12462,'lÃ©gÃ¨re',47.70,97.40,89.30),(768,2,'hypopnÃ©e',12869,12894,'lÃ©gÃ¨re',43.70,97.40,89.60),(769,2,'hypopnÃ©e',13236,13258,'lÃ©gÃ¨re',44.70,97.10,90.20),(770,2,'hypopnÃ©e',13524,13543,'lÃ©gÃ¨re',43.20,97.30,92.20),(771,2,'hypopnÃ©e',13944,13959,'lÃ©gÃ¨re',46.20,97.10,90.80),(772,2,'hypopnÃ©e',14397,14418,'lÃ©gÃ¨re',45.50,97.10,91.00),(773,2,'hypopnÃ©e',14718,14740,'lÃ©gÃ¨re',45.20,97.30,88.20),(774,2,'hypopnÃ©e',15057,15069,'lÃ©gÃ¨re',44.50,97.40,88.50),(775,2,'hypopnÃ©e',15435,15455,'lÃ©gÃ¨re',46.60,97.00,90.50),(776,2,'hypopnÃ©e',15904,15920,'lÃ©gÃ¨re',47.60,97.20,92.20),(777,2,'hypopnÃ©e',16311,16334,'lÃ©gÃ¨re',47.30,97.20,88.90),(778,2,'hypopnÃ©e',16822,16834,'lÃ©gÃ¨re',47.80,97.20,90.90),(779,2,'hypopnÃ©e',17177,17198,'lÃ©gÃ¨re',47.40,97.00,90.60),(780,2,'hypopnÃ©e',17420,17443,'lÃ©gÃ¨re',45.20,97.40,92.20),(781,2,'hypopnÃ©e',17782,17802,'lÃ©gÃ¨re',47.50,97.10,92.00),(782,2,'RERA',18196,18214,'lÃ©gÃ¨re',37.70,97.70,96.00),(783,2,'hypopnÃ©e',18787,18812,'lÃ©gÃ¨re',44.40,97.20,92.20),(784,2,'hypopnÃ©e',19190,19209,'lÃ©gÃ¨re',47.80,97.50,91.90),(785,2,'hypopnÃ©e',19559,19581,'lÃ©gÃ¨re',42.10,97.30,88.50),(786,2,'hypopnÃ©e',19978,19997,'lÃ©gÃ¨re',47.90,97.10,92.50),(787,2,'hypopnÃ©e',20274,20290,'lÃ©gÃ¨re',45.30,97.20,92.20),(788,2,'hypopnÃ©e',20647,20663,'lÃ©gÃ¨re',47.10,97.20,88.90),(789,2,'hypopnÃ©e',21177,21196,'lÃ©gÃ¨re',42.70,97.10,90.10),(790,2,'hypopnÃ©e',21448,21463,'lÃ©gÃ¨re',43.50,97.10,91.30),(791,2,'hypopnÃ©e',21827,21841,'lÃ©gÃ¨re',46.70,97.30,91.40),(792,2,'RERA',22252,22273,'lÃ©gÃ¨re',37.70,97.60,95.80),(793,2,'hypopnÃ©e',22732,22746,'lÃ©gÃ¨re',47.00,97.30,88.40),(794,2,'hypopnÃ©e',23106,23122,'lÃ©gÃ¨re',46.00,97.10,88.60),(795,2,'hypopnÃ©e',23417,23442,'lÃ©gÃ¨re',43.90,97.10,89.20),(796,2,'hypopnÃ©e',23835,23859,'lÃ©gÃ¨re',43.40,97.40,92.30),(797,2,'RERA',24110,24135,'lÃ©gÃ¨re',38.20,97.60,94.00),(798,2,'hypopnÃ©e',24576,24599,'lÃ©gÃ¨re',45.90,97.30,88.30);
/*!40000 ALTER TABLE `evenement_respiratoire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infirmier`
--

DROP TABLE IF EXISTS `infirmier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `infirmier` (
  `id_personnel` int NOT NULL,
  `diplome` varchar(100) DEFAULT NULL,
  `experience_ans` int DEFAULT NULL,
  PRIMARY KEY (`id_personnel`),
  CONSTRAINT `fk_infirmier_personnel` FOREIGN KEY (`id_personnel`) REFERENCES `personnel` (`id_personnel`),
  CONSTRAINT `infirmier_chk_1` CHECK ((`experience_ans` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infirmier`
--

LOCK TABLES `infirmier` WRITE;
/*!40000 ALTER TABLE `infirmier` DISABLE KEYS */;
INSERT INTO `infirmier` VALUES (8,'IDE',8),(9,'IDE',7),(10,'IDE',6),(11,'IDE',5),(12,'IDE',4),(13,'IDE',3),(14,'IDE',2),(15,'IDE',1);
/*!40000 ALTER TABLE `infirmier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medecin`
--

DROP TABLE IF EXISTS `medecin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medecin` (
  `id_personnel` int NOT NULL,
  `specialite` varchar(100) NOT NULL,
  `numero_rpps` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_personnel`),
  UNIQUE KEY `numero_rpps` (`numero_rpps`),
  CONSTRAINT `fk_medecin_personnel` FOREIGN KEY (`id_personnel`) REFERENCES `personnel` (`id_personnel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medecin`
--

LOCK TABLES `medecin` WRITE;
/*!40000 ALTER TABLE `medecin` DISABLE KEYS */;
INSERT INTO `medecin` VALUES (1,'MÃ©decine du sommeil','RPPS10011001'),(2,'MÃ©decine du sommeil','RPPS10022002'),(3,'MÃ©decine du sommeil','RPPS10033003'),(4,'MÃ©decine du sommeil','RPPS10044004'),(5,'Pneumologie','RPPS10055005'),(6,'Cardiologie','RPPS10066006'),(7,'Endocrinologie','RPPS10077007');
/*!40000 ALTER TABLE `medecin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nuit_etude`
--

DROP TABLE IF EXISTS `nuit_etude`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nuit_etude` (
  `id_nuit` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_superviseur` int NOT NULL COMMENT 'Infirmier superviseur',
  `id_medecin` int NOT NULL,
  `id_appareil_psg` int NOT NULL,
  `date_nuit` date NOT NULL,
  `type_etude` varchar(50) NOT NULL,
  `notes_techniques` text,
  PRIMARY KEY (`id_nuit`),
  KEY `fk_nuit_superviseur` (`id_superviseur`),
  KEY `fk_nuit_medecin` (`id_medecin`),
  KEY `fk_nuit_appareil_psg` (`id_appareil_psg`),
  KEY `idx_nuit_patient` (`id_patient`,`date_nuit`),
  CONSTRAINT `fk_nuit_appareil_psg` FOREIGN KEY (`id_appareil_psg`) REFERENCES `appareil_psg` (`id_appareil`),
  CONSTRAINT `fk_nuit_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_nuit_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `fk_nuit_superviseur` FOREIGN KEY (`id_superviseur`) REFERENCES `infirmier` (`id_personnel`),
  CONSTRAINT `nuit_etude_chk_1` CHECK ((`type_etude` in (_utf8mb4'polysomnographie',_utf8mb4'polygraphie',_utf8mb4'titration CPAP')))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nuit_etude`
--

LOCK TABLES `nuit_etude` WRITE;
/*!40000 ALTER TABLE `nuit_etude` DISABLE KEYS */;
INSERT INTO `nuit_etude` VALUES (1,1,8,1,1,'2024-10-08','polysomnographie','Installation 21h00. Patient coopÃ©rant malgrÃ© apprÃ©hension. Calibration capteurs 21h45. Endormissement 22h12. Ronflements trÃ¨s intenses dÃ¨s onset sommeil. Recalibration SpO2 Ã  01h30. RÃ©veil naturel 06h28. Signal complet 7h16 exploitable. Fichier brut : signal_psg_patient_severe.csv'),(2,2,9,2,4,'2024-11-05','polygraphie','Enregistrement ambulatoire posÃ© en consultation Ã  17h30. Patiente rentrÃ©e Ã  domicile. DÃ©marrage automatique 22h00. Latence endormissement estimÃ©e 38 min. Signal de bonne qualitÃ©. Retour appareil le lendemain matin. Fichier brut : signal_psg_patient_leger.csv');
/*!40000 ALTER TABLE `nuit_etude` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id_patient` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_naissance` date NOT NULL,
  `sexe` char(1) NOT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `numero_secu` varchar(20) DEFAULT NULL,
  `imc_initial` decimal(4,1) DEFAULT NULL,
  `fumeur` tinyint(1) DEFAULT '0',
  `pa_tabac` int DEFAULT NULL COMMENT 'Paquets-annÃ©es au diagnostic',
  `consommation_alcool` varchar(50) DEFAULT NULL COMMENT 'aucune / occasionnelle / rÃ©guliÃ¨re / excessive',
  `profession` varchar(100) DEFAULT NULL,
  `niveau_activite` varchar(50) DEFAULT NULL COMMENT 'sÃ©dentaire / modÃ©rÃ© / actif',
  `date_creation_dpi` date NOT NULL DEFAULT (curdate()),
  `actif` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_patient`),
  UNIQUE KEY `numero_secu` (`numero_secu`),
  CONSTRAINT `patient_chk_1` CHECK ((`sexe` in (_utf8mb4'M',_utf8mb4'F')))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'Tessier','Bernard','1968-07-15','M','3 rue des Tonneliers, Arles','0611445588','bernard.tessier@gmail.com','1 68 07 13 058 114',35.8,1,15,'occasionnelle','MaÃ§on','modÃ©rÃ©','2024-09-10',1),(2,'Vernet','Isabelle','1980-03-28','F','14 allÃ©e des Platanes, Tarascon','0622556699','isabelle.vernet@sfr.fr','2 80 03 13 142 225',27.4,0,0,'aucune','Comptable','modÃ©rÃ©','2024-10-05',1);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_comorbidite`
--

DROP TABLE IF EXISTS `patient_comorbidite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_comorbidite` (
  `id_patient` int NOT NULL,
  `id_comorbidite` int NOT NULL,
  `date_diagnostic` date DEFAULT NULL,
  PRIMARY KEY (`id_patient`,`id_comorbidite`),
  KEY `fk_pc_comorbidite` (`id_comorbidite`),
  CONSTRAINT `fk_pc_comorbidite` FOREIGN KEY (`id_comorbidite`) REFERENCES `comorbidite` (`id_comorbidite`),
  CONSTRAINT `fk_pc_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_comorbidite`
--

LOCK TABLES `patient_comorbidite` WRITE;
/*!40000 ALTER TABLE `patient_comorbidite` DISABLE KEYS */;
INSERT INTO `patient_comorbidite` VALUES (1,1,'2019-04-12'),(1,3,'2020-08-20'),(1,14,'2021-03-15'),(2,10,'2022-06-18'),(2,11,'2023-09-22');
/*!40000 ALTER TABLE `patient_comorbidite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel`
--

DROP TABLE IF EXISTS `personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel` (
  `id_personnel` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_embauche` date DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `actif` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_personnel`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel`
--

LOCK TABLES `personnel` WRITE;
/*!40000 ALTER TABLE `personnel` DISABLE KEYS */;
INSERT INTO `personnel` VALUES (1,'Estri','Thomas','2015-09-01','0611223344','thomas.estrii@clinique-sommeil-arles.fr',1),(2,'Faure','Isabelle','2017-03-15','0622334455','isabelle.faure@clinique-sommeil-arles.fr',1),(3,'Nakamura','Kenji','2019-06-01','0633445566','kenji.nakamura@clinique-sommeil-arles.fr',1),(4,'Bencherif','Samia','2020-01-10','0644556677','samia.bencherif@clinique-sommeil-arles.fr',1),(5,'Garnier','Laurent','2016-04-01','0655667788','laurent.garnier@clinique-sommeil-arles.fr',1),(6,'Moreau','Claire','2018-09-01','0666778899','claire.moreau@clinique-sommeil-arles.fr',1),(7,'Dupuis','Marc','2021-02-01','0677889900','marc.dupuis@clinique-sommeil-arles.fr',1),(8,'Roux','Nathalie','2016-01-01','0688990011','nathalie.roux@clinique-sommeil-arles.fr',1),(9,'Martin','Sophie','2017-06-01','0699001122','sophie.martin@clinique-sommeil-arles.fr',1),(10,'Bernard','CÃ©line','2018-03-01','0611223355','celine.bernard@clinique-sommeil-arles.fr',1),(11,'Petit','AurÃ©lie','2019-09-01','0622334466','aurelie.petit@clinique-sommeil-arles.fr',1),(12,'Leroy','Marine','2020-04-01','0633445577','marine.leroy@clinique-sommeil-arles.fr',1),(13,'Simon','Julie','2021-01-01','0644556688','julie.simon@clinique-sommeil-arles.fr',1),(14,'Michel','Fatima','2022-06-01','0655667799','fatima.michel@clinique-sommeil-arles.fr',1),(15,'Lefebvre','Amandine','2023-01-01','0666778800','amandine.lefebvre@clinique-sommeil-arles.fr',1);
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription_nuit`
--

DROP TABLE IF EXISTS `prescription_nuit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription_nuit` (
  `id_prescription` int NOT NULL AUTO_INCREMENT,
  `id_consultation` int NOT NULL,
  `id_nuit` int DEFAULT NULL,
  `motif_prescription` varchar(255) DEFAULT NULL,
  `urgence` varchar(20) NOT NULL DEFAULT 'normale',
  PRIMARY KEY (`id_prescription`),
  KEY `fk_prescription_consul` (`id_consultation`),
  KEY `fk_prescription_nuit` (`id_nuit`),
  CONSTRAINT `fk_prescription_consul` FOREIGN KEY (`id_consultation`) REFERENCES `consultation` (`id_consultation`),
  CONSTRAINT `fk_prescription_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `prescription_nuit_chk_1` CHECK ((`urgence` in (_utf8mb4'normale',_utf8mb4'urgente')))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription_nuit`
--

LOCK TABLES `prescription_nuit` WRITE;
/*!40000 ALTER TABLE `prescription_nuit` DISABLE KEYS */;
INSERT INTO `prescription_nuit` VALUES (1,2,1,'Suspicion SAHOS sÃ©vÃ¨re â€” risque professionnel conduite','urgente'),(2,4,2,'Suspicion SAHOS lÃ©ger â€” fatigue chronique invalidante','normale');
/*!40000 ALTER TABLE `prescription_nuit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resultat_nuit`
--

DROP TABLE IF EXISTS `resultat_nuit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultat_nuit` (
  `id_resultat` int NOT NULL AUTO_INCREMENT,
  `id_nuit` int NOT NULL,
  `id_medecin_validateur` int NOT NULL,
  `date_validation` date NOT NULL,
  `iah` decimal(5,2) DEFAULT NULL COMMENT 'Index ApnÃ©e-HypopnÃ©e â€” Ã©vÃ©nements/heure',
  `spo2_min` decimal(5,2) DEFAULT NULL,
  `spo2_moy` decimal(5,2) DEFAULT NULL,
  `spo2_mediane` decimal(5,2) DEFAULT NULL,
  `nb_apnees` int DEFAULT NULL,
  `nb_hypopnees` int DEFAULT NULL,
  `nb_rera` int DEFAULT NULL,
  `nb_microeveils` int DEFAULT NULL,
  `duree_sommeil_min` int DEFAULT NULL,
  `duree_hypoxie_min` int DEFAULT NULL,
  `position_dominante` varchar(20) DEFAULT NULL,
  `duree_apnee_moy_sec` int DEFAULT NULL,
  `duree_apnee_max_sec` int DEFAULT NULL,
  `decibels_max` decimal(5,2) DEFAULT NULL,
  `decibels_moy` decimal(5,2) DEFAULT NULL,
  `nb_ronflements_forts` int DEFAULT NULL,
  `severite_iah` varchar(20) GENERATED ALWAYS AS ((case when (`iah` < 5) then _utf8mb4'normal' when (`iah` < 15) then _utf8mb4'lÃ©ger' when (`iah` < 30) then _utf8mb4'modÃ©rÃ©' else _utf8mb4'sÃ©vÃ¨re' end)) STORED,
  `commentaire_medical` text,
  PRIMARY KEY (`id_resultat`),
  UNIQUE KEY `id_nuit` (`id_nuit`),
  KEY `fk_resultat_medecin` (`id_medecin_validateur`),
  KEY `idx_resultat_iah` (`iah`),
  CONSTRAINT `fk_resultat_medecin` FOREIGN KEY (`id_medecin_validateur`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_resultat_nuit` FOREIGN KEY (`id_nuit`) REFERENCES `nuit_etude` (`id_nuit`),
  CONSTRAINT `resultat_nuit_chk_1` CHECK ((`iah` >= 0)),
  CONSTRAINT `resultat_nuit_chk_10` CHECK ((`duree_hypoxie_min` >= 0)),
  CONSTRAINT `resultat_nuit_chk_11` CHECK ((`position_dominante` in (_utf8mb4'dorsale',_utf8mb4'latÃ©rale',_utf8mb4'ventrale',_utf8mb4'mixte'))),
  CONSTRAINT `resultat_nuit_chk_12` CHECK ((`duree_apnee_moy_sec` >= 0)),
  CONSTRAINT `resultat_nuit_chk_13` CHECK ((`duree_apnee_max_sec` >= 0)),
  CONSTRAINT `resultat_nuit_chk_14` CHECK ((`nb_ronflements_forts` >= 0)),
  CONSTRAINT `resultat_nuit_chk_2` CHECK ((`spo2_min` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_3` CHECK ((`spo2_moy` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_4` CHECK ((`spo2_mediane` between 0 and 100)),
  CONSTRAINT `resultat_nuit_chk_5` CHECK ((`nb_apnees` >= 0)),
  CONSTRAINT `resultat_nuit_chk_6` CHECK ((`nb_hypopnees` >= 0)),
  CONSTRAINT `resultat_nuit_chk_7` CHECK ((`nb_rera` >= 0)),
  CONSTRAINT `resultat_nuit_chk_8` CHECK ((`nb_microeveils` >= 0)),
  CONSTRAINT `resultat_nuit_chk_9` CHECK ((`duree_sommeil_min` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resultat_nuit`
--

LOCK TABLES `resultat_nuit` WRITE;
/*!40000 ALTER TABLE `resultat_nuit` DISABLE KEYS */;
/*!40000 ALTER TABLE `resultat_nuit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suivi_cpap_jour`
--

DROP TABLE IF EXISTS `suivi_cpap_jour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suivi_cpap_jour` (
  `id_suivi` int NOT NULL AUTO_INCREMENT,
  `id_appareil` int NOT NULL,
  `date_jour` date NOT NULL,
  `duree_utilisation_h` decimal(4,2) DEFAULT NULL,
  `iah_residuel` decimal(5,2) DEFAULT NULL,
  `fuites_l_min` decimal(6,2) DEFAULT NULL,
  `nb_evenements` int DEFAULT NULL,
  `qualite_donnee` varchar(20) NOT NULL DEFAULT 'bonne',
  PRIMARY KEY (`id_suivi`),
  UNIQUE KEY `id_appareil` (`id_appareil`,`date_jour`),
  KEY `idx_suivi_cpap_date` (`date_jour`),
  KEY `idx_suivi_cpap_appareil` (`id_appareil`,`date_jour`),
  CONSTRAINT `fk_suivi_cpap_appareil` FOREIGN KEY (`id_appareil`) REFERENCES `appareil_cpap` (`id_appareil`),
  CONSTRAINT `suivi_cpap_jour_chk_1` CHECK ((`duree_utilisation_h` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_2` CHECK ((`iah_residuel` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_3` CHECK ((`fuites_l_min` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_4` CHECK ((`nb_evenements` >= 0)),
  CONSTRAINT `suivi_cpap_jour_chk_5` CHECK ((`qualite_donnee` in (_utf8mb4'bonne',_utf8mb4'dÃ©gradÃ©e',_utf8mb4'manquante')))
) ENGINE=InnoDB AUTO_INCREMENT=442 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suivi_cpap_jour`
--

LOCK TABLES `suivi_cpap_jour` WRITE;
/*!40000 ALTER TABLE `suivi_cpap_jour` DISABLE KEYS */;
/*!40000 ALTER TABLE `suivi_cpap_jour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suivi_patient`
--

DROP TABLE IF EXISTS `suivi_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suivi_patient` (
  `id_suivi` int NOT NULL AUTO_INCREMENT,
  `id_patient` int NOT NULL,
  `id_medecin` int NOT NULL,
  `date_suivi` date NOT NULL,
  `poids` decimal(5,2) DEFAULT NULL,
  `imc` decimal(4,1) DEFAULT NULL,
  `tension_systolique` int DEFAULT NULL,
  `tension_diastolique` int DEFAULT NULL,
  `statut_tabac` varchar(50) DEFAULT NULL COMMENT 'fumeur / sevrage en cours / arrÃªtÃ© / non-fumeur',
  `notes_evolution` text,
  `statut_patient` varchar(20) NOT NULL DEFAULT 'actif',
  PRIMARY KEY (`id_suivi`),
  KEY `fk_suivi_patient_patient` (`id_patient`),
  KEY `fk_suivi_patient_medecin` (`id_medecin`),
  CONSTRAINT `fk_suivi_patient_medecin` FOREIGN KEY (`id_medecin`) REFERENCES `medecin` (`id_personnel`),
  CONSTRAINT `fk_suivi_patient_patient` FOREIGN KEY (`id_patient`) REFERENCES `patient` (`id_patient`),
  CONSTRAINT `suivi_patient_chk_1` CHECK ((`statut_patient` in (_utf8mb4'actif',_utf8mb4'perdu de vue',_utf8mb4'dÃ©cÃ©dÃ©')))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suivi_patient`
--

LOCK TABLES `suivi_patient` WRITE;
/*!40000 ALTER TABLE `suivi_patient` DISABLE KEYS */;
INSERT INTO `suivi_patient` VALUES (15,1,1,'2024-10-08',99.40,35.6,146,92,'fumeur','Bilan prÃ©-PSG. Somnolence sÃ©vÃ¨re Epworth 17/24. HTA mal contrÃ´lÃ©e. Patient informÃ© du dÃ©roulement de la nuit. ArrÃªt tabac recommandÃ©.','actif'),(16,2,2,'2024-11-05',72.80,27.4,118,74,'non-fumeur','Bilan prÃ©-polygraphie. Fatigue matinale. AnxiÃ©tÃ© stable sous traitement. Patiente coopÃ©rante. Pas de contre-indication.','actif');
/*!40000 ALTER TABLE `suivi_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'cliniquev3'
--

--
-- Dumping routines for database 'cliniquev3'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_creer_resultat_nuit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_creer_resultat_nuit`(
    IN p_id_nuit INT,
    IN p_spo2_min DECIMAL(5,2),
    IN p_spo2_moy DECIMAL(5,2),
    IN p_spo2_mediane DECIMAL(5,2),
    IN p_duree_hypoxie_min DECIMAL(6,2),
    IN p_position_dominante VARCHAR(20),
    IN p_decibels_max DECIMAL(5,2),
    IN p_decibels_moy DECIMAL(5,2),
    IN p_nb_ronflements_forts INT
)
BEGIN
    DECLARE v_nb_apnees INT DEFAULT 0;
    DECLARE v_nb_hypopnees INT DEFAULT 0;
    DECLARE v_nb_rera INT DEFAULT 0;
    DECLARE v_nb_microeveils INT DEFAULT 0;
    DECLARE v_duree_apnee_moy INT DEFAULT NULL;
    DECLARE v_duree_apnee_max INT DEFAULT NULL;
    DECLARE v_position VARCHAR(20);

    SET v_position = CASE
        WHEN LOWER(p_position_dominante) LIKE '%dors%' THEN 'dorsale'
        WHEN LOWER(p_position_dominante) LIKE '%lat%' THEN 'latÃ©rale'
        WHEN LOWER(p_position_dominante) LIKE '%vent%' THEN 'ventrale'
        ELSE 'mixte'
    END;

    -- RÃ©cupÃ©ration complÃ¨te depuis evenement_respiratoire
SELECT
    COUNT(CASE WHEN type_evenement LIKE '%apnÃ©e%' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'hypopnÃ©e' THEN 1 END),
    COUNT(CASE WHEN type_evenement = 'RERA' THEN 1 END),
    ROUND(AVG(duree_sec), 0),
    MAX(duree_sec)
INTO v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_duree_apnee_moy, v_duree_apnee_max
FROM evenement_respiratoire
WHERE id_nuit = p_id_nuit;

-- AJOUT NÃ‰CESSAIRE : extrapolation 2h â†’ 7h (Ã—3.5)
SET v_nb_apnees    = ROUND(v_nb_apnees * 3.5);
SET v_nb_hypopnees = ROUND(v_nb_hypopnees * 3.5);
SET v_nb_rera        = ROUND(v_nb_rera * 3.5);

-- Micro-Ã©veils : maintenant calculÃ© depuis les valeurs dÃ©jÃ  extrapolÃ©es
SET v_nb_microeveils = v_nb_apnees + v_nb_hypopnees + v_nb_rera;
    -- Insertion avec extrapolation 2h â†’ 7h
    INSERT INTO resultat_nuit (
        id_nuit, id_medecin_validateur, date_validation,
        spo2_min, spo2_moy, spo2_mediane,
        duree_hypoxie_min, position_dominante,
        decibels_max, decibels_moy, nb_ronflements_forts,
        nb_apnees, nb_hypopnees, nb_rera, nb_microeveils,
        duree_apnee_moy_sec, duree_apnee_max_sec,
        iah, duree_sommeil_min
    )
    VALUES (
        p_id_nuit,
        1,
        CURDATE(),
        p_spo2_min, p_spo2_moy, p_spo2_mediane,
        p_duree_hypoxie_min, v_position,
        p_decibels_max, p_decibels_moy, p_nb_ronflements_forts,
        v_nb_apnees, v_nb_hypopnees, v_nb_rera, v_nb_microeveils,
        v_duree_apnee_moy, v_duree_apnee_max,
        ROUND((v_nb_apnees + v_nb_hypopnees)/7, 2),   --
        420
    )
    ON DUPLICATE KEY UPDATE
        spo2_min = VALUES(spo2_min),
        spo2_moy = VALUES(spo2_moy),
        spo2_mediane = VALUES(spo2_mediane),
        duree_hypoxie_min = VALUES(duree_hypoxie_min),
        position_dominante = VALUES(position_dominante),
        decibels_max = VALUES(decibels_max),
        decibels_moy = VALUES(decibels_moy),
        nb_ronflements_forts = VALUES(nb_ronflements_forts),
        nb_apnees = VALUES(nb_apnees),
        nb_hypopnees = VALUES(nb_hypopnees),
        nb_rera = VALUES(nb_rera),
        nb_microeveils = VALUES(nb_microeveils),
        duree_apnee_moy_sec = VALUES(duree_apnee_moy_sec),
        duree_apnee_max_sec = VALUES(duree_apnee_max_sec),
        iah = VALUES(iah),
        duree_sommeil_min = VALUES(duree_sommeil_min),
        date_validation = CURDATE();

    SELECT 'OK' AS status,
           v_nb_apnees AS apnees,
           v_nb_hypopnees AS hypopnees,
           v_nb_microeveils AS microeveils,
           ROUND((v_nb_apnees + v_nb_hypopnees) /7, 2) AS iah;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_lire_resultat_nuit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_lire_resultat_nuit`(
    IN  p_id_nuit  INT
)
BEGIN

    -- Une seule requÃªte qui rassemble tout ce dont le rapport
    -- a besoin : identitÃ© patient, infos nuit, et rÃ©sultat complet.
    -- Le rapport Python n'a donc qu'un seul appel Ã  faire,
    -- pas de jointures Ã  gÃ©rer cÃ´tÃ© Python.
    SELECT
        -- IdentitÃ© patient
        p.id_patient,
        p.nom,
        p.prenom,

        -- Contexte de la nuit
        n.id_nuit,
        n.date_nuit,
        n.type_etude,

        -- MÃ©decin qui a validÃ© le rÃ©sultat
        m.id_personnel   AS id_medecin,
        per.nom          AS nom_medecin,
        per.prenom       AS prenom_medecin,

        -- RÃ©sultat complet de la nuit
        r.iah,
        r.severite_iah,
        r.spo2_min,
        r.spo2_moy,
        r.spo2_mediane,
        r.nb_apnees,
        r.nb_hypopnees,
        r.nb_rera,
        r.nb_microeveils,
        r.duree_sommeil_min,
        r.duree_hypoxie_min,
        r.position_dominante,
        r.duree_apnee_moy_sec,
        r.duree_apnee_max_sec,
        r.decibels_max,
        r.decibels_moy,
        r.nb_ronflements_forts,
        r.commentaire_medical,
        r.date_validation

    FROM resultat_nuit r
    JOIN nuit_etude n        ON n.id_nuit = r.id_nuit
    JOIN patient p           ON p.id_patient = n.id_patient
    JOIN medecin m            ON m.id_personnel = r.id_medecin_validateur
    JOIN personnel per        ON per.id_personnel = m.id_personnel

    WHERE r.id_nuit = p_id_nuit;
 END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-22 11:24:02