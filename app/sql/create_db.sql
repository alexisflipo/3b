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
