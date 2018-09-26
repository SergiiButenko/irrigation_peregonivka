PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE line_settings (
    short_name text PRIMARY KEY,
    python_type text NOT NULL
);
INSERT INTO settings(short_name, python_type) VALUES('type', 'str');
INSERT INTO settings(short_name, python_type) VALUES('pump_enabled', 'int');
INSERT INTO settings(short_name, python_type) VALUES('s0', 'int');
INSERT INTO settings(short_name, python_type) VALUES('s1', 'int');
INSERT INTO settings(short_name, python_type) VALUES('s2', 'int');
INSERT INTO settings(short_name, python_type) VALUES('s3', 'int');
INSERT INTO settings(short_name, python_type) VALUES('en', 'int');
INSERT INTO settings(short_name, python_type) VALUES('multiplex', 'int');
INSERT INTO settings(short_name, python_type) VALUES('irrigation_time', 'int');
INSERT INTO settings(short_name, python_type) VALUES('intervals', 'int');
INSERT INTO settings(short_name, python_type) VALUES('irrigation_time_wait', 'int');
INSERT INTO settings(short_name, python_type) VALUES('base_url', 'str');
INSERT INTO settings(short_name, python_type) VALUES('temp_max', 'float');
INSERT INTO settings(short_name, python_type) VALUES('temp_min', 'float');
INSERT INTO settings(short_name, python_type) VALUES('greenhouse_auto', 'int');
INSERT INTO settings(short_name, python_type) VALUES('relay_num', 'int');
INSERT INTO settings(short_name, python_type) VALUES('linked_sensor_id', 'int');
INSERT INTO settings(short_name, python_type) VALUES('pump_id', 'int');
INSERT INTO settings(short_name, python_type) VALUES('pin', 'int');
    

CREATE TABLE line_groups (
    name text NOT NULL PRIMARY KEY,
    description text
);
INSERT INTO types VALUES ('irrigation_quick', 'Quick irrigation mode');
INSERT INTO types VALUES ('irrigation_medium', 'Medium irrigation mode');
INSERT INTO types VALUES ('irrigation_heavy', 'Heavy irrigation mode');
INSERT INTO types VALUES ('multiplex', 'If analog multiplex is needed');
INSERT INTO types VALUES ('use_pump', 'If pump station needs to be turned on');
INSERT INTO types VALUES ('kids_house', 'Remote controller in kids house');
INSERT INTO types VALUES ('pump', 'Pump station');
INSERT INTO types VALUES ('irrigation', 'Irrigation controller');




CREATE TABLE line_groups_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    type_name INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT Null,
    FOREIGN KEY (type_name) REFERENCES types(name),
    FOREIGN KEY (setting) REFERENCES settings(short_name)
);
INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation', 'type', 'irrigation');
INSERT INTO types_settings(type_name, setting, value) VALUES ('pump', 'type', 'pump');
INSERT INTO types_settings(type_name, setting, value) VALUES ('ligtning', 'type', 'ligtning');

INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_quick', 'irrigation_time', '10');
INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_quick', 'intervals', '2');
INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_quick', 'irrigation_time_wait', '15');

INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_medium', 'irrigation_time', '15');
INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_medium', 'intervals', '2');
INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_medium', 'irrigation_time_wait', '15');

INSERT INTO types_settings(type_name, setting, value) VALUES ('irrigation_use_pump', 'pump_enabled', '1');

INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 's0', '1');
INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 's1', '1');
INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 's2', '1');
INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 's3', '1');
INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 'en', '1');
INSERT INTO types_settings(type_name, setting, value) VALUES ('multiplex', 'multiplex', '1');



CREATE TABLE lines (          
    id INTEGER NOT NULL PRIMARY KEY,
    description text
);

INSERT INTO lines(id, description) VALUES(1, 'Насос AL-KO');
INSERT INTO lines(id, description) VALUES(2, 'Полуниця клумба');
INSERT INTO lines(id, description) VALUES(3, 'Полуниця альтанка');
INSERT INTO lines(id, description) VALUES(4, 'Квіти');
INSERT INTO lines(id, description) VALUES(5, 'Малина');
INSERT INTO lines(id, description) VALUES(6, 'Огірки');
INSERT INTO lines(id, description) VALUES(7, 'Томати');
INSERT INTO lines(id, description) VALUES(8, 'Газон');
INSERT INTO lines(id, description) VALUES(9, 'Освітлення внутрішнє');
-- INSERT INTO lines VALUES(8, 'Повітря в теплиці');
-- INSERT INTO lines VALUES(9, 'Повітря на вулиці');
-- INSERT INTO lines VALUES(9, 'Підігрів');
-- INSERT INTO lines VALUES(10, 'Верхня бочка');


CREATE TABLE groups (
    id INTEGER NOT NULL PRIMARY KEY,
    description text
);
INSERT INTO groups VALUES (1, 'Насоси');
INSERT INTO groups VALUES (2, 'Полив з бочки');
INSERT INTO groups VALUES (3, 'Дитячий будинок');

CREATE TABLE line_groups (
    id INTEGER NOT NULL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    line_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (line_id) REFERENCES lines(id)
);
INSERT INTO line_groups(group_id, line_id) VALUES (1, 1);

INSERT INTO line_groups(group_id, line_id) VALUES (2, 2);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 3);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 4);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 5);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 6);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 7);
INSERT INTO line_groups(group_id, line_id) VALUES (2, 8);

INSERT INTO line_groups(group_id, line_id) VALUES (3, 9);


CREATE TABLE group_type (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    type INTEGER NOT NULL,
    FOREIGN KEY (type) REFERENCES types(name),
    FOREIGN KEY (group_id) REFERENCES line_groups(group_id)
);

INSERT INTO group_type(group_id, type) VALUES (1, 'pump');

INSERT INTO group_type(group_id, type) VALUES (2, 'irrigation');
INSERT INTO group_type(group_id, type) VALUES (2, 'irrigation_quick');
INSERT INTO group_type(group_id, type) VALUES (2, 'irrigation_use_pump');
INSERT INTO group_type(group_id, type) VALUES (2, 'multiplex');

INSERT INTO group_type(group_id, type) VALUES (3, 'ligtning');

CREATE TABLE line_personal_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    line_id INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT Null,
    FOREIGN KEY (line_id) REFERENCES lines(id),
    FOREIGN KEY (setting) REFERENCES settings(short_name)
);

INSERT INTO line_personal_settings(line_id, setting, value) VALUES (1, 'pin', 16);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (2, 'relay_num', 1);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (2, 'linked_sensor_id', 5);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (3, 'relay_num', 2);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (4, 'relay_num', 3);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (5, 'relay_num', 4);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (6, 'relay_num', 5);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (7, 'relay_num', 6);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (8, 'relay_num', 7);
INSERT INTO line_personal_settings(line_id, setting, value) VALUES (9, 'relay_num', 1);

CREATE TABLE permission (
    name text NOT NULL PRIMARY KEY,
    description text
);
INSERT INTO permission(name, description) VALUES ('create_branch', 'Ability to add branches for user');
INSERT INTO permission(name, description) VALUES ('read_branch', 'Ability to add branches for user');
INSERT INTO permission(name, description) VALUES ('update_branch', 'Ability to add branches for user');
INSERT INTO permission(name, description) VALUES ('delete_branch', 'Ability to delete branches for user');


CREATE TABLE roles (
    name text NOT NULL PRIMARY KEY,
    description text
);
INSERT INTO roles(name, description) VALUES ('user', 'Simple user');
INSERT INTO roles(name, description) VALUES ('branch_admin', 'User with ability to create branches');

CREATE TABLE role_permissions (
    role_name INTEGER NOT NULL PRIMARY KEY,
    permission_name INTEGER NOT NULL,
    FOREIGN KEY(permission_name) REFERENCES permission(name),
    FOREIGN KEY(role_name) REFERENCES roles(name)
);
INSERT INTO role_permissions (role_name, permission_name) VALUES ('branch_admin', 'create_branch');
INSERT INTO role_permissions (role_name, permission_name) VALUES ('branch_admin', 'read_branch');
INSERT INTO role_permissions (role_name, permission_name) VALUES ('branch_admin', 'update_branch');
INSERT INTO role_permissions (role_name, permission_name) VALUES ('branch_admin', 'delete_branch');

INSERT INTO role_permissions (role_name, permission_name) VALUES ('user', 'read_branch');

CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY,
    email text NOT NULL,
    password text NOT NULL,
    salt text NOT NULL
);
INSERT INTO users (email, password, salt) VALUES ('test@test.com', 'qwerty', '123456')


CREATE TABLE user_roles (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role_name INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(role_name) REFERENCES roles(name)
);
INSERT INTO user_roles(user_id, name) VALUES (1, 'branch_admin')

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
