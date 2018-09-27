PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE line_settings (
    name text PRIMARY KEY,
    type text NOT NULL
);

INSERT INTO settings(short_name, python_type) VALUES('irrigation_time', 'int');
INSERT INTO settings(short_name, python_type) VALUES('intervals', 'int');
INSERT INTO settings(short_name, python_type) VALUES('irrigation_time_wait', 'int');
INSERT INTO settings(short_name, python_type) VALUES('relay_num', 'int');
INSERT INTO settings(short_name, python_type) VALUES('pump_id', 'int');

CREATE TABLE line_type (
    id INTEGER NOT NULL PRIMARY KEY,
    name text NOT NULL,
    description text
);
INSERT INTO groups VALUES (1, 'water_out', 'Для подачі води');
INSERT INTO groups VALUES (2, 'irrigation', 'Для керування поливом');


CREATE TABLE lines (          
    id INTEGER NOT NULL PRIMARY KEY,
    description text NOT NULL,
    type text NOT NULL,
    FOREIGN KEY(type) REFERENCES line_type(name)
);

INSERT INTO lines(id, description, type) VALUES(1, 'Насос AL-KO', 'water_out');
INSERT INTO lines(id, description, type) VALUES(2, 'Полуниця клумба', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(3, 'Полуниця альтанка', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(4, 'Квіти', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(5, 'Малина', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(6, 'Огірки', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(7, 'Томати', 'irrigation');
INSERT INTO lines(id, description, type) VALUES(8, 'Газон', 'irrigation');


CREATE TABLE line_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    line_id INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (line_id) REFERENCES lines(id),
    FOREIGN KEY (setting) REFERENCES settings(short_name)
);

INSERT INTO line_personal_settings(line_id, setting, value) VALUES (2, 'relay_num', 1);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (3, 'relay_num', 2);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (4, 'relay_num', 3);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (5, 'relay_num', 4);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (6, 'relay_num', 5);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (7, 'relay_num', 6);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (8, 'relay_num', 7);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (9, 'relay_num', 1);




CREATE TABLE user_lines (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    line_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(line_id) REFERENCES lines(id)
);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 1);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 2);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 3);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 4);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 5);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 6);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 7);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 8);
INSERT INTO user_lines (user_id, line_id) VALUES (1, 9);
COMMIT;



select l.id, l.description, g.id, g.description, ts.setting, ts.value from lines l 
join line_groups lg on l.id = lg.line_id
join groups g on g.id = lg.group_id
join group_type gt on g.id = gt.group_id
join types_settings ts on gt.type = ts.type_name
UNION
select l.id, l.description, g.id, g.description, lps.setting, lps.value from lines l 
join line_groups lg on l.id = lg.line_id
join groups g on g.id = lg.group_id
join line_personal_settings lps on lps.line_id = l.id;
