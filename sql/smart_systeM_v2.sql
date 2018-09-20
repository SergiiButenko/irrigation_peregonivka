PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
    line_id integer NOT NULL,
    rule_id integer NOT NULL,
    execution_start_time timestamp without time zone NOT NULL,
    execution_time integer default 0 NOT NULL,
    state integer DEFAULT 1,
    interval_id text,
    FOREIGN KEY(line_id) REFERENCES lines(id),
    FOREIGN KEY(rule_id) REFERENCES type_of_rule(id),
    FOREIGN KEY(state) REFERENCES state_of_rule(id)
);

## RAIN MEASURMENTS ##

CREATE TABLE rain (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    volume REAL NOT NULL
);

## LINES ##

CREATE TABLE line_settings (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    type text NOT NULL,
    is_pump integer not null,
    pump_enabled integer,
    pump_pin integer,
    pin integer,
    s0 integer, 
    s1 integer, 
    s2 integer, 
    s3 integer, 
    en integer, 
    multiplex integer,
    base_url text
);
INSERT INTO line_settings VALUES(1, 'Полив з бочки', 'irrigation');
INSERT INTO line_settings VALUES(2, 'Освітлення', 'lighting');
INSERT INTO line_settings VALUES(3, 'Теплиця', 'greenhouse');
INSERT INTO line_settings VALUES(4, 'Верхня бочка', 'tank');

CREATE TABLE linked_sensors (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    base_url text
);
INSERT INTO linked_sensors VALUES(1, 'upper_tank', '192.168.1.55');


CREATE TABLE lines (          
    id INTEGER PRIMARY KEY,             
    name text NOT NULL,           
    time integer NOT NULL,
    intervals integer NOT NULL,
    time_wait integer NOT NULL,
    start_time time without time zone NOT NULL,
    line_setting integer NOT NULL,
    relay_num integer,
    device_id integer,
    FOREIGN KEY(line_setting) REFERENCES line_settings(id),
    FOREIGN KEY(device_id) REFERENCES linked_sensors(id)
);

INSERT INTO lines VALUES(1,1,'Насос AL-KO',10,2,15,'2017-06-29 18:34:00','irrigation',NULL,0,NULL,16,1,1,1,NULL,NULL,NULL);
INSERT INTO lines VALUES(2,2,'Полуниця клумба',10,2,15,'2017-06-29 19:00:00','irrigation',NULL,1,15,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(3,3,'Квіти',15,2,15,'2017-06-29 07:00:00','irrigation',NULL,1,14,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(4,4,'Малина',10,2,15,'2017-06-29 20:00:00','irrigation',NULL,1,13,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(5,5,'Огірки',10,2,15,'2017-06-29 21:00:00','irrigation',NULL,1,2,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(6,6,'Томати',10,2,15,'2017-06-29 06:00:00','irrigation',NULL,1,1,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(10,10,'Повітря в теплиці',0,0,0,'2017-06-29 18:30:00','air_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL,NULL);
INSERT INTO lines VALUES(11,11,'Повітря на вулиці',0,0,0,'2017-06-29 18:30:00','ground_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL,NULL);
INSERT INTO lines VALUES(12,12,'Підігрів',10800,1,1,'2017-06-29 18:34:00','greenhouse','192.168.1.102',0,1,NULL,4,0,1,NULL,NULL,NULL);
INSERT INTO lines VALUES(13,13,'Полуниця альтанка',10,2,15,'2017-06-29 08:00:00','irrigation',NULL,1,5,NULL,2,0,0,16,NULL,NULL);
INSERT INTO lines VALUES(14,14,'Верхня бочка',480,1,1,'2017-06-29 02:00:00','tank',NULL,0,NULL,20,5,0,1,NULL, 'upper_tank', '192.168.1.55');
INSERT INTO lines VALUES(16,16,'Дитячий будинок',300,1,1,'2017-06-29 18:34:00','lighting','192.168.1.234',0,2,NULL,4,0,1,NULL,NULL,NULL);
INSERT INTO lines VALUES(19,19,'Газон',15,2,15,'2017-06-29 01:00:00','irrigation',NULL,1,3,NULL,2,0,0,16,NULL,NULL);

INSERT INTO lines VALUES(7,7,'Ліхтар',300,1,1,'2017-06-29 18:34:00','lighting','192.168.1.133',0,2,NULL,4,0,1,NULL,NULL);

CREATE TABLE temperature (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    line_id integer NOT NULL,
    temp REAL NOT NULL DEFAULT 0,
    hum REAL NOT NULL DEFAULT 0
);

CREATE TABLE sensors (
    id INTEGER PRIMARY KEY,
    sensor_id integer NOT NULL,
    short_name text,
    description text
);

INSERT INTO sensors VALUES(1,1,'weather_station', 'Погодна станція');

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


CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    name text,
    short_name text,
    value int,
    json_value json
);
INSERT INTO settings VALUES(1,'Температура в теплиці','temp_min_max',NULL,'{''min'': ''14'', ''max'': ''18''}');
INSERT INTO settings VALUES(2,'Автоматичне керування температурой в теплиці','greenhouse_auto',NULL,'{''enabled'': ''0''}');
INSERT INTO settings VALUES(3,'Автоматичне керування температурой в теплиці','greenhouse_auto',NULL,'{''enabled'': ''0''}');
COMMIT;
