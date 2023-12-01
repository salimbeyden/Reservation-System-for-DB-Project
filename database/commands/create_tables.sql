USE reservations;

CREATE TABLE user (
    school_id INT PRIMARY KEY,
    `name` VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    email VARCHAR(50) CHECK (email IS NOT NULL AND email LIKE '%@%.%'),
    tel_no CHAR(10) NOT NULL,
    facility_name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    gender CHAR(1) NOT NULL,
    team_id_football INT,
    team_id_volleyball INT,
    team_id_basketball INT,
    team_id_tennis INT,
    team_id_pingpong INT
);

CREATE TABLE sport (
    sport_id INT PRIMARY KEY,
    sport_type VARCHAR(15),
    is_competitive BOOLEAN,
    capacity_min TINYINT UNSIGNED,
    capacity_max TINYINT UNSIGNED
);

CREATE TABLE team (
    team_id INT PRIMARY KEY,
    `name` VARCHAR(20),
    captaid_id INT,
    team_score INT,
    foundation_date DATE,
    password_hash VARCHAR(100),
    sport_id INT,
    FOREIGN KEY (captaid_id) REFERENCES user (school_id),
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id)
);

CREATE TABLE campus (
    campus_id INT PRIMARY KEY,
    `name` VARCHAR(20),
    `address` VARCHAR(255),
    image_id VARCHAR(20)
);

CREATE TABLE facility (
    facility_id INT PRIMARY KEY,
    `name` VARCHAR(30),
    campus_id INT,
    tel_no VARCHAR(30),
    email VARCHAR(50) CHECK (email IS NOT NULL),
    `address` VARCHAR(255),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id)
);

CREATE TABLE facility_for_sport	(
    fac_per_spor_id INT PRIMARY KEY,
    facility_id INT,
    sport_id INT,
    capacity INT,
    current	INT,
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id)
);

CREATE TABLE match_history_team (
    match_id INT PRIMARY KEY,
    `date` DATE,
    team_1 INT,
    team_2 INT,
    score_1	INT,
    score_2 INT,
    campus_id INT,
    facility_id INT,
    sport_id INT,
    FOREIGN KEY (team_1) REFERENCES team (team_id),
    FOREIGN KEY (team_2) REFERENCES team (team_id),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id),
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id)
);

CREATE TABLE match_history_individual (
    match_id INT PRIMARY KEY,
    `date` DATE,
    user_1 INT,
    user_2 INT,
    score_1	INT,
    score_2 INT,
    campus_id INT,
    facility_id INT,
    sport_id INT,
    FOREIGN KEY (user_1) REFERENCES user (school_id),
    FOREIGN KEY (user_2) REFERENCES user (school_id),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id),
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id)
);

CREATE TABLE reservation_team (
    reservation_id INT PRIMARY KEY,
    sport_id INT,
    campus_id INT,
    facility_id INT,
    `date` DATE,
    team_1 INT,
    team_2 INT,
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id),
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (team_1) REFERENCES team (team_id),
    FOREIGN KEY (team_2) REFERENCES team (team_id)
);

CREATE TABLE reservation_individual (
    reservation_id INT PRIMARY KEY,
    sport_id INT,
    campus_id INT,
    facility_id INT,
    `date` DATE,
    user INT,
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id),
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (user) REFERENCES user (school_id)
);

CREATE TABLE reservation_individual_match (
    reservation_id INT PRIMARY KEY,
    sport_id INT,
    campus_id INT,
    facility_id INT,
    `date` DATE,
    user_1 INT,
    user_2 INT,
    FOREIGN KEY (sport_id) REFERENCES sport (sport_id),
    FOREIGN KEY (campus_id) REFERENCES campus (campus_id),
    FOREIGN KEY (facility_id) REFERENCES facility (facility_id),
    FOREIGN KEY (user_1) REFERENCES user (school_id),
    FOREIGN KEY (user_2) REFERENCES user (school_id)
);