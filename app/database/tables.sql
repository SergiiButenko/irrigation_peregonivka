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
CREATE TABLE type_of_rule (
    id INTEGER PRIMARY KEY,
    name text NOT NULL
);
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
CREATE INDEX moisture_index ON moisture (line_id);
CREATE INDEX life_index ON life (interval_id, ongoing_rule_id);
CREATE TABLE temperature (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    line_id integer NOT NULL,
    temp REAL NOT NULL DEFAULT 0,
    hum REAL NOT NULL DEFAULT 0
);
CREATE INDEX temperature_index ON temperature (line_id);
CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    name text,
    short_name text,
    value int,
    json_value json
);
CREATE TABLE stop_fill (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime'))
);
CREATE TABLE lines (     id INTEGER PRIMARY KEY,     number integer NOT NULL,     name text NOT NULL,     time integer NOT NULL DEFAULT 10,     intervals integer NOT NULL DEFAULT 2,     time_wait integer NOT NULL DEFAULT 15,     start_time time without time zone NOT NULL DEFAULT '2017-06-29 18:34:00',     line_type text NOT NULL default 'irrigation',     base_url text,     pump_enabled integer NOT NULL DEFAULT 1,     relay_num integer,     pin integer,     group_id integer not null default 0,     is_pump integer not null default 0,     is_except integer not null default 0,     pump_pin integer,     device_id text DEFAULT NULL,     device_url text DEFAULT NULL, start_mode text DEFAULT 'manual', linked_device_id text, linked_device_url text,     FOREIGN KEY(group_id) REFERENCES line_groups(id));
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY,
    sensor_id integer NOT NULL,
    short_name text,
    description text
);
CREATE TABLE weather_station (
    id INTEGER PRIMARY KEY,
    datetime time without time zone NOT NULL DEFAULT (datetime('now','localtime')),
    sensor_id integer NOT NULL,
    temp REAL NOT NULL DEFAULT 0,
    hum REAL NOT NULL DEFAULT 0,
    press REAL NOT NULL DEFAULT 0, voltage REAL NOT NULL DEFAULT 0,
    FOREIGN KEY(sensor_id) REFERENCES sensors(sensor_id)
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "switchers_to_lines"  (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
device_id VARCHAR,
switch_num INTEGER,
line_id INTEGER,
FOREIGN KEY(line_id) REFERENCES lines(id)
);
CREATE TABLE lines__tmp__ (id INTEGER PRIMARY KEY, number integer NOT NULL, name text NOT NULL, time integer NOT NULL DEFAULT 10, intervals integer NOT NULL DEFAULT 2, time_wait integer NOT NULL DEFAULT 15, start_time time without time zone NOT NULL DEFAULT '2017-06-29 18:34:00', line_type text NOT NULL default 'irrigation', base_url text, pump_enabled integer NOT NULL DEFAULT 1, relay_num integer, pin integer, group_id integer not null default 0, is_pump integer not null default 0, pump_pin integer, device_id text DEFAULT NULL, device_url text DEFAULT NULL, start_mode text DEFAULT 'manual', FOREIGN KEY(group_id) REFERENCES line_groups(id));
CREATE TABLE IF NOT EXISTS "devices"  (
  "id" integer PRIMARY KEY,
  "device_id" text NOT NULL UNIQUE,
  "last_known_ip" text,
  "updated" time without time zone NOT NULL DEFAULT (datetime('now','localtime'))
);
