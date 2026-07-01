-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: clinique
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
) ENGINE=InnoDB AUTO_INCREMENT=455 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evenement_respiratoire`
--

LOCK TABLES `evenement_respiratoire` WRITE;
/*!40000 ALTER TABLE `evenement_respiratoire` DISABLE KEYS */;
INSERT INTO `evenement_respiratoire` (`id_evenement`, `id_nuit`, `type_evenement`, `debut_sec`, `fin_sec`, `severite`, `decibels`, `spo2_avant`, `spo2_apres`) VALUES (353,1,'apnÃ©e obstructive',60,125,'sÃ©vÃ¨re',72.40,95.20,78.40),(354,1,'apnÃ©e obstructive',191,233,'sÃ©vÃ¨re',70.80,95.00,80.20),(355,1,'apnÃ©e obstructive',305,338,'sÃ©vÃ¨re',68.40,94.80,82.60),(356,1,'apnÃ©e obstructive',436,495,'sÃ©vÃ¨re',73.20,95.10,77.80),(357,1,'apnÃ©e obstructive',560,612,'sÃ©vÃ¨re',71.60,94.90,79.40),(358,1,'apnÃ©e obstructive',673,703,'modÃ©rÃ©e',65.80,95.20,83.80),(359,1,'apnÃ©e obstructive',775,832,'sÃ©vÃ¨re',72.80,94.80,78.20),(360,1,'hypopnÃ©e',923,983,'modÃ©rÃ©e',58.40,95.40,87.60),(361,1,'apnÃ©e obstructive',1053,1112,'sÃ©vÃ¨re',71.40,94.70,79.80),(362,1,'apnÃ©e obstructive',1193,1246,'sÃ©vÃ¨re',73.60,95.00,77.60),(363,1,'apnÃ©e centrale',1337,1362,'modÃ©rÃ©e',42.80,95.20,89.40),(364,1,'apnÃ©e obstructive',1461,1496,'modÃ©rÃ©e',66.20,95.10,84.20),(365,1,'apnÃ©e obstructive',1592,1638,'sÃ©vÃ¨re',72.00,94.80,79.20),(366,1,'RERA',1712,1730,'lÃ©gÃ¨re',44.60,95.40,93.20),(367,1,'apnÃ©e obstructive',1860,1906,'sÃ©vÃ¨re',73.80,95.00,77.40),(368,1,'apnÃ©e obstructive',1988,2048,'sÃ©vÃ¨re',71.20,94.80,80.40),(369,1,'apnÃ©e obstructive',2118,2166,'sÃ©vÃ¨re',72.60,94.90,78.80),(370,1,'hypopnÃ©e',2258,2282,'modÃ©rÃ©e',56.80,95.30,88.20),(371,1,'apnÃ©e obstructive',2368,2428,'sÃ©vÃ¨re',74.00,94.70,77.00),(372,1,'apnÃ©e centrale',2524,2552,'modÃ©rÃ©e',40.40,95.20,90.20),(373,1,'apnÃ©e obstructive',2638,2698,'sÃ©vÃ¨re',73.20,94.80,78.60),(374,1,'RERA',2798,2816,'lÃ©gÃ¨re',43.20,95.40,93.80),(375,1,'apnÃ©e obstructive',2908,2964,'sÃ©vÃ¨re',71.80,94.90,79.60),(376,1,'apnÃ©e obstructive',3068,3128,'sÃ©vÃ¨re',72.40,94.70,78.80),(377,1,'apnÃ©e obstructive',3228,3272,'modÃ©rÃ©e',67.40,95.10,83.40),(378,1,'apnÃ©e obstructive',3368,3428,'sÃ©vÃ¨re',73.60,94.80,77.20),(379,1,'hypopnÃ©e',3524,3548,'modÃ©rÃ©e',57.20,95.30,87.80),(380,2,'hypopnÃ©e',60,84,'lÃ©gÃ¨re',44.20,97.20,91.80),(381,2,'hypopnÃ©e',391,405,'lÃ©gÃ¨re',42.80,97.40,92.40),(382,2,'hypopnÃ©e',861,883,'lÃ©gÃ¨re',46.40,97.10,90.80),(383,2,'RERA',1224,1238,'lÃ©gÃ¨re',38.60,97.60,95.40),(384,2,'hypopnÃ©e',1522,1539,'lÃ©gÃ¨re',44.80,97.20,91.20),(385,2,'hypopnÃ©e',2008,2029,'lÃ©gÃ¨re',45.20,97.30,91.60),(386,2,'hypopnÃ©e',2471,2486,'lÃ©gÃ¨re',43.60,97.40,92.20),(387,2,'RERA',2808,2833,'lÃ©gÃ¨re',39.20,97.50,95.80),(388,2,'hypopnÃ©e',3267,3285,'lÃ©gÃ¨re',44.00,97.20,91.40),(389,1,'apnÃ©e obstructive',130,162,'sÃ©vÃ¨re',72.00,95.20,81.20),(390,1,'apnÃ©e obstructive',238,277,'sÃ©vÃ¨re',74.30,94.90,81.60),(391,1,'apnÃ©e obstructive',343,370,'sÃ©vÃ¨re',70.10,95.20,78.50),(392,1,'apnÃ©e obstructive',382,410,'sÃ©vÃ¨re',73.30,95.00,77.70),(393,1,'hypopnÃ©e',500,541,'modÃ©rÃ©e',58.10,95.40,88.90),(394,1,'apnÃ©e centrale',617,667,'modÃ©rÃ©e',42.70,95.20,88.10),(395,1,'apnÃ©e obstructive',708,734,'sÃ©vÃ¨re',75.10,94.80,80.00),(396,1,'apnÃ©e obstructive',837,875,'sÃ©vÃ¨re',73.60,95.30,77.20),(397,1,'apnÃ©e obstructive',988,1020,'sÃ©vÃ¨re',73.30,94.60,79.80),(398,1,'apnÃ©e obstructive',1117,1151,'sÃ©vÃ¨re',73.30,95.10,81.20),(399,1,'apnÃ©e obstructive',1251,1281,'sÃ©vÃ¨re',69.80,95.20,78.10),(400,1,'apnÃ©e obstructive',1367,1411,'sÃ©vÃ¨re',71.20,94.60,79.20),(401,1,'apnÃ©e obstructive',1501,1531,'sÃ©vÃ¨re',68.00,94.70,80.00),(402,1,'hypopnÃ©e',1542,1570,'modÃ©rÃ©e',58.50,95.30,88.10),(403,1,'apnÃ©e obstructive',1643,1676,'sÃ©vÃ¨re',71.60,94.70,80.50),(404,1,'hypopnÃ©e',1735,1784,'modÃ©rÃ©e',58.40,95.40,87.10),(405,1,'hypopnÃ©e',1796,1830,'modÃ©rÃ©e',57.70,95.50,88.10),(406,1,'hypopnÃ©e',1911,1950,'modÃ©rÃ©e',58.60,95.30,85.10),(407,1,'apnÃ©e obstructive',2053,2077,'sÃ©vÃ¨re',68.80,94.70,79.50),(408,1,'hypopnÃ©e',2171,2216,'modÃ©rÃ©e',59.80,95.40,86.50),(409,1,'apnÃ©e obstructive',2287,2336,'sÃ©vÃ¨re',72.50,95.30,79.50),(410,1,'apnÃ©e obstructive',2433,2474,'sÃ©vÃ¨re',70.40,95.10,82.00),(411,1,'apnÃ©e obstructive',2485,2508,'sÃ©vÃ¨re',74.30,94.80,77.00),(412,1,'apnÃ©e obstructive',2557,2592,'sÃ©vÃ¨re',71.70,94.60,76.80),(413,1,'apnÃ©e obstructive',2703,2736,'sÃ©vÃ¨re',71.60,95.20,80.20),(414,1,'apnÃ©e centrale',2750,2779,'modÃ©rÃ©e',40.90,95.40,87.50),(415,1,'apnÃ©e obstructive',2821,2853,'sÃ©vÃ¨re',70.00,94.70,79.40),(416,1,'apnÃ©e obstructive',2969,3001,'sÃ©vÃ¨re',75.10,94.80,81.00),(417,1,'apnÃ©e obstructive',3012,3052,'sÃ©vÃ¨re',75.50,94.90,81.40),(418,1,'hypopnÃ©e',3133,3161,'modÃ©rÃ©e',59.30,95.40,85.70),(419,1,'apnÃ©e obstructive',3277,3321,'sÃ©vÃ¨re',68.60,94.70,78.80),(420,1,'hypopnÃ©e',3433,3475,'modÃ©rÃ©e',54.10,95.30,87.00),(421,1,'apnÃ©e centrale',3486,3510,'modÃ©rÃ©e',40.40,95.30,88.70),(422,1,'apnÃ©e obstructive',3553,3592,'sÃ©vÃ¨re',72.30,95.00,79.50),(423,1,'apnÃ©e obstructive',3605,3628,'sÃ©vÃ¨re',71.30,94.60,79.50),(424,1,'apnÃ©e obstructive',3642,3671,'sÃ©vÃ¨re',68.40,94.50,78.10),(425,1,'apnÃ©e obstructive',3686,3719,'sÃ©vÃ¨re',69.80,95.10,77.00),(426,1,'hypopnÃ©e',3735,3783,'modÃ©rÃ©e',56.60,95.50,86.70),(427,1,'hypopnÃ©e',3803,3847,'modÃ©rÃ©e',58.80,95.20,85.70),(428,1,'apnÃ©e obstructive',3864,3911,'sÃ©vÃ¨re',70.20,94.80,79.40),(429,1,'apnÃ©e obstructive',3924,3971,'sÃ©vÃ¨re',69.60,94.90,80.20),(430,1,'apnÃ©e obstructive',3986,4027,'sÃ©vÃ¨re',73.20,95.20,76.50),(431,1,'apnÃ©e obstructive',4053,4082,'sÃ©vÃ¨re',73.40,95.10,81.00),(432,1,'apnÃ©e obstructive',4110,4156,'sÃ©vÃ¨re',69.20,94.60,80.60),(433,1,'apnÃ©e obstructive',4176,4202,'sÃ©vÃ¨re',73.20,94.60,81.20),(434,1,'apnÃ©e obstructive',4224,4254,'sÃ©vÃ¨re',73.70,95.00,80.60),(435,1,'apnÃ©e obstructive',4276,4309,'sÃ©vÃ¨re',72.90,94.80,76.30),(436,1,'apnÃ©e obstructive',4336,4358,'sÃ©vÃ¨re',70.70,95.00,77.10),(437,1,'apnÃ©e obstructive',4369,4418,'sÃ©vÃ¨re',69.40,94.60,79.00),(438,1,'hypopnÃ©e',4440,4484,'modÃ©rÃ©e',59.80,95.50,85.10),(439,1,'apnÃ©e obstructive',4501,4530,'sÃ©vÃ¨re',71.00,95.00,76.60),(440,1,'apnÃ©e obstructive',4560,4603,'sÃ©vÃ¨re',74.40,94.70,78.70),(441,1,'apnÃ©e obstructive',4616,4663,'sÃ©vÃ¨re',74.30,95.20,76.50),(442,1,'apnÃ©e obstructive',4679,4723,'sÃ©vÃ¨re',74.50,95.20,81.00),(443,1,'hypopnÃ©e',4745,4774,'modÃ©rÃ©e',58.60,95.30,86.30),(444,1,'hypopnÃ©e',4786,4834,'modÃ©rÃ©e',54.30,95.40,86.20),(445,1,'apnÃ©e obstructive',4857,4907,'sÃ©vÃ¨re',69.30,95.30,81.30),(446,2,'hypopnÃ©e',184,204,'lÃ©gÃ¨re',45.10,97.50,90.50),(447,2,'hypopnÃ©e',505,518,'lÃ©gÃ¨re',45.90,97.10,91.40),(448,2,'hypopnÃ©e',983,996,'lÃ©gÃ¨re',44.60,97.30,90.10),(449,2,'RERA',1338,1352,'lÃ©gÃ¨re',37.80,97.70,94.80),(450,2,'hypopnÃ©e',1639,1656,'lÃ©gÃ¨re',43.80,97.50,90.60),(451,2,'hypopnÃ©e',1873,1891,'lÃ©gÃ¨re',45.50,97.20,90.00),(452,2,'hypopnÃ©e',2129,2149,'lÃ©gÃ¨re',45.90,97.30,92.30),(453,2,'hypopnÃ©e',2358,2374,'lÃ©gÃ¨re',47.90,97.00,91.50),(454,2,'hypopnÃ©e',2586,2606,'lÃ©gÃ¨re',44.00,97.10,92.30);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-17  9:15:55