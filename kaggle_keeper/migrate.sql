DROP DATABASE kaggle;
CREATE DATABASE kaggle;
USE kaggle;

CREATE TABLE kernel (
       id INTEGER NOT NULL,
       title VARCHAR(100),
       lang ENUM('R', 'Python'),
       notebook BOOLEAN,
       votes INTEGER,
       PRIMARY KEY(id));

CREATE TABLE category (
       id INTEGER NOT NULL AUTO_INCREMENT,
       title VARCHAR(100),
       description VARCHAR(300),
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE technology (
       id INTEGER NOT NULL AUTO_INCREMENT,
       title VARCHAR(100),
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE data_link (
       id INTEGER NOT NULL AUTO_INCREMENT,
       link VARCHAR(100),
       title VARCHAR(100),
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE category_relation (
       id INTEGER NOT NULL AUTO_INCREMENT,
       kernel_id INTEGER,
       category_id INTEGER,
       CONSTRAINT kernel_category_fk FOREIGN KEY(kernel_id) REFERENCES kernel(id),
       CONSTRAINT category_fk FOREIGN KEY(category_id) REFERENCES category(id),
       PRIMARY KEY(id));

CREATE TABLE technology_relation (
       id INTEGER NOT NULL AUTO_INCREMENT,
       kernel_id INTEGER,
       technology_id INTEGER,
       CONSTRAINT kernel_technology_fk FOREIGN KEY(kernel_id) REFERENCES kernel(id),
       CONSTRAINT technology_fk FOREIGN KEY(technology_id) REFERENCES technology(id),
       PRIMARY KEY(id));

CREATE TABLE data_link_relation (
       id INTEGER NOT NULL AUTO_INCREMENT,
       kernel_id INTEGER,
       data_link_id INTEGER,
       CONSTRAINT kernel_data_link_fk FOREIGN KEY(kernel_id) REFERENCES kernel(id),
       CONSTRAINT data_link_fk FOREIGN KEY(data_link_id) REFERENCES data_link(id),
       PRIMARY KEY(id));
