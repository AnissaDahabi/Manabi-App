-- ============================================
--  MANABI — Script de déploiement
-- ============================================

CREATE DATABASE IF NOT EXISTS manabi_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE manabi_db;

-- ============================================
--  TABLES
-- ============================================

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','professeur','eleve') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `cours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intitule` varchar(100) NOT NULL,
  `niveau` varchar(5) DEFAULT NULL,
  `prof_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prof_id` (`prof_id`),
  CONSTRAINT `cours_ibfk_1` FOREIGN KEY (`prof_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cours_id` int(11) NOT NULL,
  `prof_id` int(11) NOT NULL,
  `date_session` date NOT NULL,
  `heure_debut` time NOT NULL,
  `heure_fin` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cours_id` (`cours_id`),
  KEY `prof_id` (`prof_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`cours_id`) REFERENCES `cours` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`prof_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` int(11) NOT NULL,
  `eleve_id` int(11) NOT NULL,
  `date_reservation` timestamp NULL DEFAULT current_timestamp(),
  `statut` varchar(20) DEFAULT 'en attente',
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`),
  KEY `eleve_id` (`eleve_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`eleve_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================
--  DONNÉES
-- ============================================

INSERT INTO `users` (`id`, `nom`, `prenom`, `email`, `password`, `role`) VALUES
(1, 'Moreau', 'Sophie', 'sophie.moreau@manabi.com', 'admin1234', 'admin'),
(2, 'Tanaka', 'Hiroshi', 'hiroshi.tanaka@manabi.com', 'prof1234', 'professeur'),
(3, 'Yamamoto', 'Aiko', 'aiko.yamamoto@manabi.com', 'prof1234', 'professeur'),
(4, 'Dupont', 'Alice', 'alice.dupont@manabi.com', 'prof1234', 'professeur'),
(5, 'Martin', 'Lucas', 'lucas.martin@gmail.com', 'eleve1234', 'eleve'),
(6, 'Bernard', 'Camille', 'camille.bernard@gmail.com', 'eleve1234', 'eleve'),
(7, 'Leroy', 'Thomas', 'thomas.leroy@yahoo.fr', 'eleve1234', 'eleve'),
(8, 'Petit', 'Emma', 'emma.petit@hotmail.com', 'eleve1234', 'eleve'),
(9, 'Dubois', 'Antoine', 'antoine.dubois@gmail.com', 'eleve1234', 'eleve'),
(10, 'Moreau', 'Léa', 'lea.moreau@gmail.com', 'eleve1234', 'eleve'),
(12, 'Laurent', 'Chloé', 'chloe.laurent@yahoo.fr', 'eleve1234', 'eleve');

INSERT INTO `cours` (`id`, `intitule`, `niveau`, `prof_id`, `description`) VALUES
(1, 'Hiragana et Katakana', 'N5', 2, 'Apprenez les deux syllabaires fondamentaux du japonais. Ce cours couvre la lecture et l\'écriture des 46 hiragana et 46 katakana, indispensables pour débuter.'),
(2, 'Vocabulaire quotidien N5', 'N5', 2, 'Acquisition des 800 mots essentiels du niveau N5 : salutations, chiffres, couleurs, famille, nourriture et expressions de la vie courante.'),
(3, 'Grammaire de base N5', 'N5', 3, 'Introduction aux structures grammaticales fondamentales : particules は, が, を, に, les verbes en -masu, les adjectifs en -i et -na.'),
(4, 'Kanji N5 - 80 caractères', 'N5', 3, 'Étude des 80 kanji du niveau N5 avec leur lecture kun\'yomi et on\'yomi, leur sens et leur utilisation dans des mots courants.'),
(5, 'Grammaire intermédiaire N4', 'N4', 2, 'Approfondissement grammatical : forme te, forme conditionnelle, expressions de cause et conséquence, verbes de déplacement.'),
(6, 'Vocabulaire N4', 'N4', 3, 'Les 1500 mots du niveau N4 organisés par thèmes : travail, transports, santé, nature, émotions et vie sociale.'),
(7, 'Kanji N4 - 166 caractères', 'N4', 4, 'Étude approfondie des 166 kanji N4 : composition, radicaux, lecture et pratique à travers des textes authentiques.'),
(8, 'Conversation japonaise N4', 'N4', 4, 'Cours axé sur l\'expression orale : dialogues du quotidien, jeux de rôle, prononciation et intonation naturelle.'),
(9, 'Grammaire avancée N3', 'N3', 4, 'Structures complexes du N3 : formes passives et causatives, expressions de politesse avancées, connecteurs logiques.'),
(10, 'Lecture de textes N3', 'N3', 3, 'Analyse de textes authentiques : articles de presse, notices, menus et documents administratifs simples en japonais.');

INSERT INTO `sessions` (`id`, `cours_id`, `prof_id`, `date_session`, `heure_debut`, `heure_fin`) VALUES
(1, 1, 2, '2026-04-07', '10:00:00', '12:00:00'),
(2, 1, 2, '2026-04-14', '10:00:00', '12:00:00'),
(3, 1, 2, '2026-04-21', '10:00:00', '12:00:00'),
(4, 1, 2, '2026-04-28', '10:00:00', '12:00:00'),
(5, 2, 2, '2026-04-08', '14:00:00', '16:00:00'),
(6, 2, 2, '2026-04-15', '14:00:00', '16:00:00'),
(7, 2, 2, '2026-04-22', '14:00:00', '16:00:00'),
(8, 3, 3, '2026-04-09', '10:00:00', '12:00:00'),
(9, 3, 3, '2026-04-16', '10:00:00', '12:00:00'),
(10, 3, 3, '2026-04-23', '10:00:00', '12:00:00'),
(11, 3, 3, '2026-04-30', '10:00:00', '12:00:00'),
(12, 4, 3, '2026-04-10', '14:00:00', '16:00:00'),
(13, 4, 3, '2026-04-17', '14:00:00', '16:00:00'),
(14, 4, 3, '2026-04-24', '14:00:00', '16:00:00'),
(15, 5, 2, '2026-05-05', '10:00:00', '12:00:00'),
(16, 5, 2, '2026-05-12', '10:00:00', '12:00:00'),
(17, 5, 2, '2026-05-19', '10:00:00', '12:00:00'),
(18, 6, 3, '2026-05-06', '14:00:00', '16:00:00'),
(19, 6, 3, '2026-05-13', '14:00:00', '16:00:00'),
(20, 6, 3, '2026-05-20', '14:00:00', '16:00:00'),
(21, 7, 4, '2026-05-07', '10:00:00', '12:00:00'),
(22, 7, 4, '2026-05-14', '10:00:00', '12:00:00'),
(23, 7, 4, '2026-05-21', '10:00:00', '12:00:00'),
(24, 8, 4, '2026-05-08', '14:00:00', '16:00:00'),
(25, 8, 4, '2026-05-15', '14:00:00', '16:00:00'),
(26, 8, 4, '2026-05-22', '14:00:00', '16:00:00'),
(27, 9, 4, '2026-06-02', '10:00:00', '12:00:00'),
(28, 9, 4, '2026-06-09', '10:00:00', '12:00:00'),
(29, 9, 4, '2026-06-16', '10:00:00', '12:00:00'),
(30, 10, 3, '2026-06-03', '14:00:00', '16:00:00'),
(31, 10, 3, '2026-06-10', '14:00:00', '16:00:00'),
(32, 10, 3, '2026-06-17', '14:00:00', '16:00:00');

INSERT INTO `reservations` (`id`, `session_id`, `eleve_id`, `date_reservation`, `statut`) VALUES
(1, 1, 5, '2026-03-20 08:15:00', 'en attente'),
(2, 2, 5, '2026-03-20 08:16:00', 'en attente'),
(3, 5, 5, '2026-03-20 08:17:00', 'en attente'),
(4, 8, 5, '2026-03-20 08:18:00', 'en attente'),
(5, 1, 6, '2026-03-21 09:00:00', 'en attente'),
(6, 5, 6, '2026-03-21 09:01:00', 'en attente'),
(7, 6, 6, '2026-03-21 09:02:00', 'en attente'),
(8, 12, 6, '2026-03-21 09:03:00', 'en attente'),
(9, 15, 7, '2026-03-22 13:30:00', 'confirmee'),
(10, 16, 7, '2026-03-22 13:31:00', 'annulee'),
(11, 21, 7, '2026-03-22 13:32:00', 'confirmee'),
(12, 24, 7, '2026-03-22 13:33:00', 'confirmee'),
(13, 1, 8, '2026-03-23 07:00:00', 'confirmee'),
(14, 8, 8, '2026-03-23 07:01:00', 'en attente'),
(15, 9, 8, '2026-03-23 07:02:00', 'confirmee'),
(16, 18, 8, '2026-03-23 07:03:00', 'confirmee'),
(17, 15, 9, '2026-03-24 10:00:00', 'en attente'),
(18, 18, 9, '2026-03-24 10:01:00', 'en attente'),
(19, 24, 9, '2026-03-24 10:02:00', 'confirmee'),
(20, 25, 9, '2026-03-24 10:03:00', 'en attente'),
(21, 27, 10, '2026-03-25 15:00:00', 'en attente'),
(22, 28, 10, '2026-03-25 15:01:00', 'confirmee'),
(23, 30, 10, '2026-03-25 15:02:00', 'annulee'),
(24, 31, 10, '2026-03-25 15:03:00', 'annulee'),
(28, 21, 12, '2026-03-27 12:00:00', 'annulee'),
(29, 27, 12, '2026-03-27 12:01:00', 'confirmee'),
(30, 30, 12, '2026-03-27 12:02:00', 'confirmee'),
(31, 17, 5, '2026-03-26 08:30:23', 'confirmee'),
(32, 3, 5, '2026-03-26 09:27:11', 'confirmee'),
(33, 25, 5, '2026-03-26 10:43:26', 'confirmee'),
(75, 19, 5, '2026-03-27 23:21:26', 'annulee'),
(76, 13, 5, '2026-03-30 08:38:03', 'confirmee'),
(77, 4, 5, '2026-05-07 07:46:21', 'en attente'),
(78, 14, 5, '2026-05-07 08:46:50', 'en attente');

COMMIT;
