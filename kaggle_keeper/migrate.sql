DROP DATABASE kaggle;
CREATE DATABASE kaggle;
USE kaggle;

CREATE TABLE competition (
       id INTEGER NOT NULL,
       title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE kernel (
       id INTEGER NOT NULL,
       title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       lang ENUM('R', 'Python'),
       notebook BOOLEAN,
       votes INTEGER,
       best_score FLOAT,
       competition_id INTEGER,
       source_version INTEGER,
       CONSTRAINT competition_kernel_fk FOREIGN KEY(competition_id) REFERENCES competition(id),
       PRIMARY KEY(id));

CREATE TABLE category (
       id INTEGER NOT NULL AUTO_INCREMENT,
       title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       description VARCHAR(300) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE technology (
       id INTEGER NOT NULL AUTO_INCREMENT,
       title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE data_link (
       id INTEGER NOT NULL AUTO_INCREMENT,
       link VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       title VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       source_type VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
       PRIMARY KEY(id),
       UNIQUE(title));

CREATE TABLE category_relation (
       id INTEGER NOT NULL AUTO_INCREMENT,
       kernel_id INTEGER,
       competition_id INTEGER,
       category_id INTEGER,
       CONSTRAINT kernel_category_fk FOREIGN KEY(kernel_id) REFERENCES kernel(id),
       CONSTRAINT competition_category_fk FOREIGN KEY(competition_id) REFERENCES competition(id),
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
