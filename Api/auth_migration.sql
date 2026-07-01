-- ============================================================
--  MIGRATION AUTH  –  Clinique Sommeil
--  À exécuter UNE seule fois sur ta base clinique2nuitsv2
-- ============================================================

-- 1. Ajouter le mot de passe hashé sur la table personnel
ALTER TABLE personnel
  ADD COLUMN password_hash VARCHAR(255) NULL AFTER email;

-- 2. Table des rôles (medecin / infirmier)
--    Calculé automatiquement depuis medecin / infirmier,
--    mais on le stocke aussi pour les queries rapides
CREATE TABLE IF NOT EXISTS user_role (
  id_personnel INT       NOT NULL,
  role         ENUM('medecin','infirmier') NOT NULL,
  PRIMARY KEY (id_personnel, role),
  FOREIGN KEY (id_personnel) REFERENCES personnel(id_personnel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Table des refresh tokens (pour déconnexion sécurisée)
CREATE TABLE IF NOT EXISTS refresh_token (
  id          INT          NOT NULL AUTO_INCREMENT,
  id_personnel INT         NOT NULL,
  token_hash  VARCHAR(255) NOT NULL,
  expires_at  DATETIME     NOT NULL,
  revoked     TINYINT(1)   NOT NULL DEFAULT 0,
  created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX idx_token (token_hash),
  FOREIGN KEY (id_personnel) REFERENCES personnel(id_personnel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Remplir user_role à partir des tables existantes
INSERT IGNORE INTO user_role (id_personnel, role)
  SELECT id_personnel, 'medecin'   FROM medecin;

INSERT IGNORE INTO user_role (id_personnel, role)
  SELECT id_personnel, 'infirmier' FROM infirmier;

-- 5. Mot de passe temporaire pour les tests : "Clinique2024!"
--    (bcrypt hash généré par le script seed.js)
--    Tu DOIS appeler `node seed.js` après la migration pour
--    générer les vrais hashes.
