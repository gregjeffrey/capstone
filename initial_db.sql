
USE nuinstig_goats;

DROP TABLE IF EXISTS locations;
CREATE TABLE locations
(
	location_no 	INT 		PRIMARY KEY,
    field_name 		VARCHAR(20) NOT NULL,
    plant_type 		VARCHAR(20) NOT NULL,
    health_change 	DOUBLE,
    last_pic_saved 	LONGBLOB,
    ts_of_last_pic 	TIMESTAMP,
    alert_present 	BOOL		NOT NULL
    
);

DROP TABLE IF EXISTS measurements;
CREATE TABLE measurements
(
	id				INT 		PRIMARY KEY		AUTO_INCREMENT,
    tstamp 			TIMESTAMP 	NOT NULL,
    location_no 	INT 		NOT NULL,
    insects_present BOOL 		NOT NULL,
    image 			LONGBLOB,
    ndvi_val 		DOUBLE 		NOT NULL,
    water_content	DOUBLE		NOT NULL,
    chlor_a			DOUBLE		NOT NULL,
    chlor_b			DOUBLE		NOT NULL,
    
    CONSTRAINT fkey_location
    FOREIGN KEY (location_no)
    REFERENCES locations (location_no)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DELIMITER //
CREATE PROCEDURE plant_data(IN plant VARCHAR(20))
BEGIN
	SELECT tstamp, location_no, ndvi_val
    FROM measurements
    JOIN locations ON locations.location_no = measurements.location_no
    WHERE locations.plant_type = plant;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE farm_data(IN fieldname VARCHAR(20))
BEGIN
	SELECT tstamp, location_no, ndvi_val
    FROM measurements
    JOIN locations ON locations.location_no = measurements.location_no
    WHERE locations.field_name = fieldname;
END//
DELIMITER ;



