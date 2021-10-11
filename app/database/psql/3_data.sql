\connect smart_house
INSERT INTO
    public.users (id, username, hashed_password)
VALUES
    (
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf33',
        'serbut',
        '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
    );


INSERT INTO
    public.components_groups (id, name)
VALUES
    (
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf32',
        'Полив'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'irrigation_relay1',
        'Контроллер поливу огорода',
        'Relay8ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'irrigation_relay2',
        'Контроллер насосу поливу огорода',
        'Relay8ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'greenhouse_relay1',
        'Контроллер підігріва теплиці',
        'Relay2ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'greenhouse_relay2',
        'Освітлення в теплиці',
        'Relay2ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'basement_relay1',
        'Освітлення на дворі',
        'Relay4ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'kids_house_relay1',
        'Освітлення на дитячому будинку',
        'Relay8ch',
        'v1'
    );

INSERT INTO
    public.devices(id, description, type, version)
VALUES
    (
        'cesspoll_relay_sensor1',
        'Реле септика',
        'Relay2ch',
        'v1'
    );

INSERT INTO
    public.components_groups(name)
VALUES
    ('Насоси');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Полив з бочки');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Полив з системи');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Теплиця');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Теплиця Датчики');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Двір');

INSERT INTO
    public.components_groups(name)
VALUES
    ('Сад');

INSERT INTO
    public.components_categories(name, description)
VALUES
    (
        'actuator',
        'Тип девайсу, що виконує якусь дію'
    );

INSERT INTO
    public.components_categories(name, description)
VALUES
    (
        'sensor',
        'Тип девайсу, що лише генерує дані'
    );

INSERT INTO
    public.components_types(name, description)
VALUES
    (
        'relay',
        'Дискретний девайс'
    );

INSERT INTO
    public.components_types(name, description)
VALUES
    (
        'POWER_CURRENT',
        'Вимірювач наявності напруги'
    );

INSERT INTO
    public.components(
        id,
        device_id,
        name,
        group_id,
        category,
        type,
        version,
        settings,
        usage_type,
        telegram_notify
    )
VALUES
    (
        1,
        'irrigation_relay1',
        'Томати',
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf32',
        'actuator',
        'relay',
        'v1',
        NULL,
        'irrigation',
        true
    );

INSERT INTO
    public.components(
        id,
        device_id,
        name,
        group_id,
        category,
        type,
        version,
        settings,
        telegram_notify
    )
VALUES
    (
        1,
        'cesspoll_relay_sensor1',
        'Датчик рівня води в септику',
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf32',
        'sensor',
        'POWER_CURRENT',
        'v1',
        NULL,
        false
    );

INSERT INTO
    public.components(
        id,
        device_id,
        name,
        group_id,
        category,
        type,
        version,
        settings,
        telegram_notify
    )
VALUES
    (
        2,
        'cesspoll_relay_sensor1',
        'Датчик увімкнення насосу в септику',
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf32',
        'sensor',
        'POWER_CURRENT',
        'v1',
        NULL,
        false
    );