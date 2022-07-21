-- final_project.Users definition
USE final_project;

CREATE TABLE users (
	user_id INTEGER auto_increment NOT NULL,
	email varchar(100) NOT NULL,
	first_name varchar(100) NOT NULL,
	last_name varchar(100) NOT NULL,
	password varchar(100) NOT NULL,
	CONSTRAINT Users_PK PRIMARY KEY (user_id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;
DROP TABLE IF EXISTS Users;

-- `3b`.articles definition


CREATE TABLE articles (
  description text NOT NULL,
  images varchar(100) DEFAULT NULL,
  publish_date date NOT NULL,
  titre varchar(100) NOT NULL,
  article_id bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`article_id`)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;
