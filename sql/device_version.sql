-- USER SERCTION ---
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
    id INTEGER NOT NULL PRIMARY KEY,
    role_name TEXT NOT NULL,
    permission_name TEXT NOT NULL,
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
INSERT INTO users (email, password, salt) VALUES ('test@test.com', 'qwerty', '123456');
INSERT INTO users (email, password, salt) VALUES ('test2@test.com', 'qwerty', '123456');

CREATE TABLE user_roles (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    role_name INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(role_name) REFERENCES roles(name)
);
INSERT INTO user_roles(user_id, name) VALUES (1, 'branch_admin');
INSERT INTO user_roles(user_id, name) VALUES (2, 'user');


-- HUB SERCTION ---

CREATE TABLE hub_parameters (
    name text NOT NULL PRIMARY KEY,
    description text NOT NULL
);
INSERT INTO hub_parameters(name, description) VALUES('base_url', 'URL адреса до хаба');
INSERT INTO hub_parameters(name, description) VALUES('s0', 'S0 pin');
INSERT INTO hub_parameters(name, description) VALUES('s1', 'S1 pin');
INSERT INTO hub_parameters(name, description) VALUES('s2', 'S2 pin');
INSERT INTO hub_parameters(name, description) VALUES('s3', 'S3 pin');
INSERT INTO hub_parameters(name, description) VALUES('en', 'en pin');
INSERT INTO hub_parameters(name, description) VALUES('pump1_pin', 'Насос 1. Пін');
INSERT INTO hub_parameters(name, description) VALUES('pump1_name', 'Насос 1. Назва');
INSERT INTO hub_parameters(name, description) VALUES('pump2_pin', 'Насос 2. Пін');
INSERT INTO hub_parameters(name, description) VALUES('pump2_name', 'Насос 2. Назва');

CREATE TABLE hub (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);
INSERT INTO hub (name) VALUES ('Контроллер поливу Перегонівка.');

CREATE TABLE hub_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    hub_id INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (hub_id) REFERENCES hub_settings(id),
    FOREIGN KEY (setting) REFERENCES hub_parameters(name)
);
INSERT INTO hub_settings (hub_id, 'base_url', 'http://mozz.asuscomm.com:7542');
INSERT INTO hub_settings (hub_id, 's0', 2);
INSERT INTO hub_settings (hub_id, 's1', 1);
INSERT INTO hub_settings (hub_id, 's2', 2);
INSERT INTO hub_settings (hub_id, 's3', 3);
INSERT INTO hub_settings (hub_id, 'en', 5);
INSERT INTO hub_settings (hub_id, 'pump1_name', 'Насос AL-KO');
INSERT INTO hub_settings (hub_id, 'pump1_pin', '16');

CREATE TABLE user_hub (
    id INTEGER NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    hub_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(hub_id) REFERENCES hub(id)
);
INSERT INTO user_hub(user_id, hub_id) VALUES (1, 1)
INSERT INTO user_hub(user_id, hub_id) VALUES (2, 1)


-- DEVICE SERCTION ---

CREATE TABLE device_parameters (
    name text NOT NULL PRIMARY KEY,
    description text NOT NULL
);
INSERT INTO device_parameters(name, description) VALUES('type', 'Тип датчика: реле, термо, контроль заповнення');
INSERT INTO device_parameters(name, description) VALUES('radio_type', 'Тип радіо канала датчика: WIFI, Radio');
INSERT INTO device_parameters(name, description) VALUES('outer_temp_hum', 'Виносний датчик DHT21');

CREATE TABLE device (      
    id INTEGER NOT NULL PRIMARY KEY,
    description text NOT NULL
);
INSERT INTO device(id, description) VALUES (1, 'Контроллер заповнення верхньої бочки');
INSERT INTO device(id, description) VALUES (2, 'Контроллер дитячого будинку');

CREATE TABLE device_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device(id),
    FOREIGN KEY (setting) REFERENCES device_parameters(name)
);
INSERT INTO device_settings (device_id, setting, value) VALUES (1, 'type', 'fill');
INSERT INTO device_settings (device_id, setting, value) VALUES (2, 'type', 'relay');


CREATE TABLE device_hub (
    id INTEGER NOT NULL PRIMARY KEY,
    hub_id INTEGER NOT NULL,
    device_id INTEGER NOT NULL,
    FOREIGN KEY(hub_id) REFERENCES hub(id),
    FOREIGN KEY(device_id) REFERENCES device(id)
);
INSERT INTO hub_id(hub_id, device_id) VALUES (1, 1)
INSERT INTO device_hub(hub_id, device_id) VALUES (1, 2)

-- IRRIGATION SERCTION ---
    
    irrigation_time INTEGER NOT NULL,
    irrigation_intervals INTEGER NOT NULL,
    irrigation_time_wait INTEGER NOT NULL,
    relay_num INTEGER NOT NULL,
    pump_mode TEXT DEFAULT 'no pump', -- need table with allowed settings
    

CREATE TABLE line_parameters (
    name text NOT NULL PRIMARY KEY,
    description text NOT NULL
);
INSERT INTO device_parameters(name, description) VALUES('operation_execution_time', 'Дефолтний час виконання');
INSERT INTO device_parameters(name, description) VALUES('operation_intervals', 'Дефолтне значення кількості повторів');
INSERT INTO device_parameters(name, description) VALUES('operation_time_wait', 'Дефолтне значення часу очікування');
INSERT INTO device_parameters(name, description) VALUES('relay_num', 'Номер реле');
INSERT INTO device_parameters(name, description) VALUES('pump_mode', 'Який насос вмикати, якщо взашалі вмикати');
INSERT INTO device_parameters(name, description) VALUES('type', 'Тип лінії. Потенційно потрібен');

CREATE TABLE lines (      
    id INTEGER NOT NULL PRIMARY KEY,
    description text NOT NULL
);
INSERT INTO lines(id, description) VALUES ('Полуниця клумба');
INSERT INTO lines(id, description) VALUES ('Полуниця альтанка');
INSERT INTO lines(id, description) VALUES ('Полуниця альтанка');
INSERT INTO lines(id, description) VALUES ('Квіти');
INSERT INTO lines(id, description) VALUES ('Огірки');
INSERT INTO lines(id, description) VALUES ('Томати');
INSERT INTO lines(id, description) VALUES ('Газон');
INSERT INTO lines(id, description) VALUES ('Верхня бочка');

CREATE TABLE line_settings (
    id INTEGER NOT NULL PRIMARY KEY,
    line_id INTEGER NOT NULL,
    setting TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (line_id) REFERENCES lines(id),
    FOREIGN KEY (setting) REFERENCES device_parameters(name)
);
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (1, 'relay_num', '1');

INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (2, 'relay_num', '2');

INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (3, 'relay_num', '3');

INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'operation_execution_time', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (4, 'relay_num', '4');

INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (5, 'relay_num', '5');

INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (6, 'relay_num', '6');

INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'type', 'irrigation');
INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'operation_execution_time', '10');
INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'operation_intervals', '2');
INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'operation_time_wait', '15');
INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'pump_mode', 'pump1');
INSERT INTO line_settings (line_id, setting, value) VALUES (7, 'relay_num', '7');

INSERT INTO line_settings (line_id, setting, value) VALUES (8, 'type', 'fill');
INSERT INTO line_settings (line_id, setting, value) VALUES (8, 'operation_execution_time', '480');
INSERT INTO line_settings (line_id, setting, value) VALUES (8, 'operation_intervals', '1');
INSERT INTO line_settings (line_id, setting, value) VALUES (8, 'pump_mode', 'no_pump');
INSERT INTO line_settings (line_id, setting, value) VALUES (8, 'relay_num', '13');


CREATE TABLE line_hub (
    id INTEGER NOT NULL PRIMARY KEY,
    hub_id INTEGER NOT NULL,
    line_id INTEGER NOT NULL,
    FOREIGN KEY(hub_id) REFERENCES hub(id),
    FOREIGN KEY(line_id) REFERENCES lines(id)
);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 1);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 2);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 3);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 4);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 5);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 6);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 7);
INSERT INTO line_hub(hub_id, line_id) VALUES (1, 8);























CREATE TABLE lines (          
    id INTEGER NOT NULL PRIMARY KEY,
    description text NOT NULL,
    irrigation_time INTEGER NOT NULL,
    irrigation_intervals INTEGER NOT NULL,
    irrigation_time_wait INTEGER NOT NULL,
    relay_num INTEGER NOT NULL,
    pump_mode TEXT DEFAULT 'no pump', -- need table with allowed settings
    hub_id INTEGER NOT NULL,
    FOREIGN KEY(hub_id) REFERENCES hub(id)
);

INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (2, 'Полуниця клумба', 10, 2, 15, 1, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (3, 'Полуниця альтанка', 10, 2, 15, 2, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (4, 'Полуниця альтанка', 10, 2, 15, 3, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (5, 'Квіти', 15, 2, 15, 4, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (6, 'Огірки', 10, 2, 15, 5, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (7, 'Томати', 10, 2, 15, 6, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (8, 'Газон', 15, 2, 15, 7, 'pump1', 1);
INSERT INTO lines(id, description, irrigation_time, irrigation_intervals, irrigation_time_wait, relay_num, pump_mode, hub_id) VALUES (8, 'Верхня бочка', 480, 1, 0, 13, 'no pump', 1, 1);


CREATE TABLE line_linked_device (
    id INTEGER NOT NULL PRIMARY KEY,
    line_id INTEGER NOT NULL,
    device_id INTEGER NOT NULL,
    FOREIGN KEY(line_id) REFERENCES lines(id),
    FOREIGN KEY(device_id) REFERENCES device(id)
);