-- final_project.Users definition*
CREATE DATABASE IF NOT EXISTS final_project
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;


USE final_project;

CREATE TABLE IF NOT EXISTS user (
	id INTEGER auto_increment NOT NULL UNIQUE,
	email varchar(100) NOT NULL UNIQUE,
  name varchar(100) NOT NULL,
	password varchar(255) NOT NULL,
  is_admin boolean DEFAULT false,
	CONSTRAINT User_PK PRIMARY KEY (id)
)
ENGINE=InnoDB;

-- `3b`.articles definition

CREATE TABLE IF NOT EXISTS articles (
  description text NOT NULL,
  images varchar(100) DEFAULT NULL,
  publish_date date NOT NULL,
  titre varchar(100) NOT NULL UNIQUE,
  id bigint(20) NOT NULL AUTO_INCREMENT UNIQUE,
  PRIMARY KEY (`id`)
)
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `books` (
  `id` INTEGER auto_increment NOT NULL UNIQUE,
  `title` varchar(255) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `description` varchar(10000) DEFAULT NULL,
  `language` varchar(100) DEFAULT NULL,
  `isbn` varchar(100) DEFAULT NULL,
  `genres` varchar(100) DEFAULT NULL,
  `numRatings` float DEFAULT NULL,
  `likedPercent` float DEFAULT NULL,
  `coverImg` varchar(10000) DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
									