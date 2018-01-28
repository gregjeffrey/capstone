
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
CREATE PROCEDURE add_measurements(IN t datetime, loc_no INT, insects BOOL, ndvi DOUBLE, water DOUBLE, chlora DOUBLE, chlorb DOUBLE)
BEGIN
	INSERT INTO measurements (tstamp, location_no, insects_present, ndvi_val, water_content, chlor_a, chlor_b) VALUES
    (t, loc_no, insects, ndvi, water, chlora, chlorb);
END//
DELIMITER ;

