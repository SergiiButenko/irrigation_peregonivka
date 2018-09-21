PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

## USERS ## 
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY,
    short_name text
);
INSERT INTO users VALUES(1, 'peregonivka');


## RULES ##
CREATE TABLE state_of_rule (
    id INTEGER PRIMARY KEY,
    short_name text NOT NULL,
    full_name text NOT NULL
);
INSERT INTO state_of_rule VALUES(1,'Pending','Заплановано');
INSERT INTO state_of_rule VALUES(2,'Done','Виконано');
INSERT INTO state_of_rule VALUES(3,'Failed','Не виконано');
INSERT INTO state_of_rule VALUES(4,'Canceled','Скасовано');
INSERT INTO state_of_rule VALUES(5,'Canceled_by_rain','Скасовано через дощ');
INSERT INTO state_of_rule VALUES(6,'Canceled_by_ground_humidity','Скасовано через вологість грунту');
INSERT INTO state_of_rule VALUES(7,'Canceled_by_mistime','Скасовано через помилку з часом');


CREATE TABLE type_of_rule (
    id INTEGER PRIMARY KEY,
    short_name text NOT NULL,
    name text NOT NULL
);
INSERT INTO type_of_rule VALUES(1, 'start', 'Почати полив');
INSERT INTO type_of_rule VALUES(2, 'stop', 'Зупинити полив');


CREATE TABLE life (
    id INTEGER PRIMARY KEY,
    unit_name text NOT NULL,
    rule_type integer NOT NULL,
    execution_start_time timestamp without time zone NOT NULL,
    execution_time integer default 0 NOT NULL,
    state integer DEFAULT 1,
    interval_id text,
    FOREIGN KEY(unit_name) REFERENCES units(short_name),
    FOREIGN KEY(rule_type) REFERENCES type_of_rule(id),
    FOREIGN KEY(state) REFERENCES state_of_rule(id)
);


## LINES ##
CREATE TABLE settings (
    short_name text PRIMARY KEY,
    python_type text NOT NULL
);
INSERT INTO settings VALUES('type', 'str');
INSERT INTO settings VALUES('is_pump', 'int');
INSERT INTO settings VALUES('pump_enabled', 'int');
INSERT INTO settings VALUES('pump_pin', 'int');
INSERT INTO settings VALUES('pin', 'int');
INSERT INTO settings VALUES('s0', 'int');
INSERT INTO settings VALUES('s1', 'int');
INSERT INTO settings VALUES('s2', 'int');
INSERT INTO settings VALUES('s3', 'int');
INSERT INTO settings VALUES('en', 'int');
INSERT INTO settings VALUES('multiplex', 'int');
INSERT INTO settings VALUES('irrigation_time', 'int');
INSERT INTO settings VALUES('intervals', 'int');
INSERT INTO settings VALUES('irrigation_time_wait', 'int');
INSERT INTO settings VALUES('irrigation_start_time', 'datetime');
INSERT INTO settings VALUES('relay_num', 'int');
INSERT INTO settings VALUES('linked_sensor_id', 'int');
INSERT INTO settings VALUES('base_url', 'str');
INSERT INTO settings VALUES('temp_max', 'float');
INSERT INTO settings VALUES('temp_min', 'float');
INSERT INTO settings VALUES('greenhouse_auto', 'int');

-- INSERT INTO settings VALUES(1,'Температура в теплиці','temp_min_max',NULL,'{''min'': ''14'', ''max'': ''18''}');
-- INSERT INTO settings VALUES(2,'Автоматичне керування температурой в теплиці','greenhouse_auto',NULL,'{''enabled'': ''0''}');
-- INSERT INTO settings VALUES(3,'Автоматичне керування температурой в теплиці','greenhouse_auto',NULL,'{''enabled'': ''0''}');


CREATE TABLE units (          
    user_id INTEGER NOT NULL,
    short_name text NOT NULL,
    description text,
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (user_id, short_name)
);

INSERT INTO units VALUES(1, 'pump_alko','Насос AL-KO');
INSERT INTO units VALUES(1, 'strauberry_1','Полуниця клумба');
INSERT INTO units VALUES(1, 'strauberry_2','Полуниця альтанка');
-- INSERT INTO units VALUES(1, 'flowers','Квіти');
-- INSERT INTO units VALUES(1, 'raspberry','Малина'); ,10,2,15,'2017-06-29 20:00:00','irrigation',NULL,1,13,NULL,2,0,0,16,NULL,NULL);
-- INSERT INTO units VALUES(1, 'cucumbers','Огірки'); ,10,2,15,'2017-06-29 21:00:00','irrigation',NULL,1,2,NULL,2,0,0,16,NULL,NULL);
-- INSERT INTO units VALUES(1, 'tomatoes','Томати'); ,10,2,15,'2017-06-29 06:00:00','irrigation',NULL,1,1,NULL,2,0,0,16,NULL,NULL);
-- INSERT INTO units VALUES(1, 'in_air_greenhouse','Повітря в теплиці'); ,0,0,0,'2017-06-29 18:30:00','air_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL,NULL);
-- INSERT INTO units VALUES(1, 'out_air_greenhouse','Повітря на вулиці'); ,0,0,0,'2017-06-29 18:30:00','ground_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL,NULL);
-- INSERT INTO units VALUES(1, 'floor_greenhouse','Підігрів'); ,10800,1,1,'2017-06-29 18:34:00','greenhouse','192.168.1.102',0,1,NULL,4,0,1,NULL,NULL,NULL)
-- INSERT INTO units VALUES(1, 'upper_tank','Верхня бочка'); ,480,1,1,'2017-06-29 02:00:00','tank',NULL,0,NULL,20,5,0,1,NULL, 'upper_tank', '192.168.1.55');
-- INSERT INTO units VALUES(1, 'kids_house','Дитячий будинок'); ,300,1,1,'2017-06-29 18:34:00','lighting','192.168.1.234',0,2,NULL,4,0,1,NULL,NULL,NULL);
-- INSERT INTO units VALUES(1, 'grass','Газон'); ,15,2,15,'2017-06-29 01:00:00','irrigation',NULL,1,3,NULL,2,0,0,16,NULL,NULL);

CREATE TABLE unit_settings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    unit_name text NOT NULL,
    settings text NOT NULL,
    value text NOT NULL,
    FOREIGN KEY(settings) REFERENCES settings(short_name),
    FOREIGN KEY(user_id, unit_name) REFERENCES units(user_id, short_name)
);

INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'pump', 'type', 'pump');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'pump', 'is_pump', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'pump', 'pin', '16');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'pump', 'base_url', 'http://');

INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'type', 'irrigation');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'is_pump', '0');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'pump_pin', '16');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'irrigation_time', '10');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'intervals', '2');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'irrigation_time_wait', '15');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'irrigation_start_time', '19:00:00');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'relay', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 's0', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 's1', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 's2', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 's3', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'en', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'multiplex', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_1', 'base_url', 'http://');

INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'type', 'irrigation');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'is_pump', '0');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'pump_pin', '16');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'irrigation_time', '10');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'intervals', '2');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'irrigation_time_wait', '15');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'irrigation_start_time', '18:00:00');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'relay', '2');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 's0', '2');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 's1', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 's2', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 's3', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'en', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'multiplex', '1');
INSERT INTO unit_settings(user_id, unit_name, settings, value) VALUES(1, 'strauberry_2', 'base_url', 'http://');


CREATE TABLE weather_station (
    id INTEGER PRIMARY KEY,
    datetime time without time zone DEFAULT (datetime('now','localtime')),
    sensor_id integer NOT NULL,
    temp REAL NOT NULL DEFAULT 0,
    hum REAL NOT NULL DEFAULT 0,
    press REAL NOT NULL DEFAULT 0,
    voltage REAL NOT NULL DEFAULT 0,
    FOREIGN KEY(sensor_id) REFERENCES sensors(sensor_id)
);
COMMIT;
