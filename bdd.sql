create database WhatsApp IF NOT EXISTS;

use WhatsApp;
CREATE TABLE Utilisateur (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nom VARCHAR(40) NOT NULL,
  prenom VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  motDePasse VARCHAR(255) NOT NULL,
  photoProfil VARCHAR(255),
  dateCreation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  statutEnLigne BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE Discussion (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  type ENUM('prive','groupe') NOT NULL,
  dateCreation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Participant (
  idDiscussion BIGINT NOT NULL,
  idUser BIGINT NOT NULL,
  role ENUM('admin','membre') DEFAULT 'membre',
  dateAjout DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idDiscussion, idUser),
  FOREIGN KEY (idDiscussion) REFERENCES Discussion(id),
  FOREIGN KEY (idUser) REFERENCES Utilisateur(id)
);

CREATE TABLE Groupe (
  idDiscussion BIGINT PRIMARY KEY,
  nom VARCHAR(80) NOT NULL,
  photo VARCHAR(255),
  FOREIGN KEY (idDiscussion) REFERENCES Discussion(id)
);


CREATE TABLE Message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  idDiscussion BIGINT NOT NULL,
  idExpediteur BIGINT NOT NULL,
  contenu TEXT,
  typeMessage ENUM('texte','image','video','audio','document') NOT NULL,
  dateEnvoi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (idDiscussion) REFERENCES Discussion(id),
  FOREIGN KEY (idExpediteur) REFERENCES Utilisateur(id)
);


CREATE TABLE MessageStatut (
  idMessage BIGINT NOT NULL,
  idUser BIGINT NOT NULL,
  statut ENUM('envoye','recu','lu') NOT NULL,
  dateStatut DATETIME NOT NULL,
  PRIMARY KEY (idMessage, idUser),
  FOREIGN KEY (idMessage) REFERENCES Message(id),
  FOREIGN KEY (idUser) REFERENCES Utilisateur(id)
);


CREATE TABLE Document (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  idMessage BIGINT NOT NULL,
  nomFichier VARCHAR(150) NOT NULL,
  urlFichier VARCHAR(255) NOT NULL,
  taille BIGINT NOT NULL,
  format VARCHAR(20) NOT NULL,
  FOREIGN KEY (idMessage) REFERENCES Message(id)
);


CREATE TABLE Statut (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  idUser BIGINT NOT NULL,
  type ENUM('texte','image','video') NOT NULL,
  contenu TEXT,
  datePublication DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  dateExpiration DATETIME NOT NULL,
  FOREIGN KEY (idUser) REFERENCES Utilisateur(id)
);


CREATE TABLE Contact (
  idUser1 BIGINT NOT NULL,
  idUser2 BIGINT NOT NULL,
  dateAjout DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  bloque BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (idUser1, idUser2),
  FOREIGN KEY (idUser1) REFERENCES Utilisateur(id),
  FOREIGN KEY (idUser2) REFERENCES Utilisateur(id),
  CHECK (idUser1 < idUser2)
);

