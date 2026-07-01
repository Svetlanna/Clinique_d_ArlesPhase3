DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE sp_compteur_all()
BEGIN
    SELECT COUNT(*) AS total
    FROM evenement_respiratoire;
END $$

CREATE DEFINER=`root`@`localhost` PROCEDURE sp_compteur_rera()
BEGIN
    SELECT COUNT(*) AS total
    FROM evenement_respiratoire
    WHERE type_evenement = 'RERA';
END $$

CREATE DEFINER=`root`@`localhost` PROCEDURE sp_compteur_apnees()
BEGIN
    SELECT COUNT(*) AS total
    FROM evenement_respiratoire
    WHERE type_evenement IN ('apnée obstructive', 'apnée centrale');
END $$

CREATE DEFINER=`root`@`localhost` PROCEDURE sp_compteur_hypopnee()
BEGIN
    SELECT COUNT(*) AS total
    FROM evenement_respiratoire
    WHERE type_evenement = 'hypopnée';
END $$

DELIMITER ;