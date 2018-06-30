PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE life (
    id INTEGER PRIMARY KEY,
    line_id integer NOT NULL,
    rule_id integer NOT NULL,
    state integer DEFAULT 0 NOT NULL,
    date date NOT NULL,
    timer timestamp without time zone NOT NULL,
    active integer DEFAULT 1 NOT NULL, 
    interval_id text, 
    time integer default 0 NOT NULL, 
    ongoing_rule_id text,
    FOREIGN KEY(line_id) REFERENCES lines(number),
    FOREIGN KEY(state) REFERENCES state_of_rule(id),
    FOREIGN KEY(rule_id) REFERENCES type_of_rule(id)
);

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
INSERT INTO state_of_rule VALUES(6,'Canceled_by_humidity','Скасовано через вологість');
INSERT INTO state_of_rule VALUES(7,'Canceled_by_mistime','Скасовано через помилку з часом');

CREATE TABLE type_of_rule (
    id INTEGER PRIMARY KEY,
    name text NOT NULL
);
INSERT INTO type_of_rule VALUES(1,'Почати полив');
INSERT INTO type_of_rule VALUES(2,'Зупинити полив');

CREATE TABLE ongoing_rules (
    id INTEGER PRIMARY KEY,
    line_id integer NOT NULL,
    time integer NOT NULL,
    intervals integer NOT NULL,
    time_wait integer NOT NULL,
    repeat_value integer NOT NULL,
    date_time_start timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    active integer NOT NULL DEFAULT 1, 
    rule_id text, 
    FOREIGN KEY(line_id) REFERENCES lines(number)
);

CREATE TABLE rain (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    volume REAL NOT NULL
);

CREATE TABLE moisture (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    line_id integer NOT NULL,
    value REAL NOT NULL DEFAULT 0
);
CREATE TABLE line_groups (
id INTEGER PRIMARY KEY,
name text NOT NULL, 
s0 integer, 
s1 integer, 
s2 integer, 
s3 integer, 
en integer, 
multiplex integer default 1);
INSERT INTO line_groups VALUES(1,'Насоси',NULL,NULL,NULL,NULL,NULL,0);
INSERT INTO line_groups VALUES(2,'Полив з бочки',26,13,6,5,12,1);
INSERT INTO line_groups VALUES(3,'Полив з системи',NULL,NULL,NULL,NULL,NULL,0);
INSERT INTO line_groups VALUES(4,'Ліхтар',NULL,NULL,NULL,NULL,NULL,0);
INSERT INTO line_groups VALUES(5,'Теплиця',NULL,NULL,NULL,NULL,NULL,0);
INSERT INTO line_groups VALUES(6,'Теплиця Датчики',NULL,NULL,NULL,NULL,NULL,0);

CREATE TABLE lines (
    id INTEGER PRIMARY KEY,
    number integer NOT NULL,
    name text NOT NULL,
    time integer NOT NULL DEFAULT 10,
    intervals integer NOT NULL DEFAULT 2,
    time_wait integer NOT NULL DEFAULT 15, 
    start_time time without time zone NOT NULL DEFAULT '2017-06-29 18:34:00', 
    line_type text NOT NULL default 'irrigation', 
    base_url text, 
    pump_enabled integer NOT NULL DEFAULT 1,
    relay_num integer, 
    pin integer, 
    group_id integer not null default 0, 
    is_pump integer not null default 0, 
    is_except integer not null default 0, 
    pump_pin integer,
    moisture_id integer,
    FOREIGN KEY(group_id) REFERENCES line_groups(id));
INSERT INTO lines VALUES(1,1,'Насос AL-KO',10,2,15,'2017-06-29 18:34:00','irrigation',NULL,0,NULL,16,1,1,1,NULL,NULL);
INSERT INTO lines VALUES(2,2,'Полуниця клумба',10,2,15,'2017-06-29 19:00:00','irrigation',NULL,1,15,NULL,2,0,0,16,1);
INSERT INTO lines VALUES(3,3,'Квіти',15,2,15,'2017-06-29 07:00:00','irrigation',NULL,1,14,NULL,2,0,0,16,2);
INSERT INTO lines VALUES(4,4,'Малина',10,2,15,'2017-06-29 20:00:00','irrigation',NULL,1,13,NULL,2,0,0,16,3);
INSERT INTO lines VALUES(5,5,'Огірки',10,2,15,'2017-06-29 21:00:00','irrigation',NULL,1,2,NULL,2,0,0,16,4);
INSERT INTO lines VALUES(6,6,'Томати',10,2,15,'2017-06-29 06:00:00','irrigation',NULL,1,1,NULL,2,0,0,16,5);
INSERT INTO lines VALUES(7,7,'Ліхтар',300,1,1,'2017-06-29 18:34:00','lighting','192.168.1.133',0,2,NULL,4,0,1,NULL,NULL);
INSERT INTO lines VALUES(10,10,'Повітря в теплиці',0,0,0,'2017-06-29 18:30:00','air_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL);
INSERT INTO lines VALUES(11,11,'Повітря на вулиці',0,0,0,'2017-06-29 18:30:00','ground_sensor','192.168.1.102',0,NULL,NULL,5,0,1,NULL,NULL);
INSERT INTO lines VALUES(12,12,'Підігрів',10800,1,1,'2017-06-29 18:34:00','greenhouse','192.168.1.102',0,1,NULL,4,0,1,NULL,NULL);
INSERT INTO lines VALUES(13,13,'Полуниця альтанка',10,2,15,'2017-06-29 08:00:00','irrigation',NULL,1,5,NULL,2,0,0,16,NULL);
INSERT INTO lines VALUES(14,14,'Верхня бочка',480,1,1,'2017-06-29 00:00:00','tank',NULL,0,NULL,20,5,0,1,NULL,NULL);
INSERT INTO lines VALUES(16,16,'Будиночок',300,1,1,'2017-06-29 18:34:00','lighting','192.168.1.234',0,2,NULL,4,0,1,NULL,NULL);
INSERT INTO lines VALUES(5,5, 'Огірки',10,2,15,'2017-06-29 21:00:00','irrigation',NULL,1,2,NULL,2,0,0,16,4);
INSERT INTO lines VALUES(19,19,'Газон',10,2,15,'2017-06-29 01:00:00','irrigation',NULL,1,3,NULL,2,0,0,16,NULL);

CREATE TABLE temperature (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    line_id integer NOT NULL,
    temp REAL NOT NULL DEFAULT 0,
    hum REAL NOT NULL DEFAULT 0
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

CREATE TABLE stop_fill (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE INDEX moisture_index ON moisture (line_id);
CREATE INDEX life_index ON life (interval_id, ongoing_rule_id);
CREATE INDEX temperature_index ON temperature (line_id);
COMMIT;
