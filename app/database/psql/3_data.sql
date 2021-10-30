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
    public.groups (id, short_name, name, user_id)
VALUES
    (
        'ae9f4b91-8ee5-4939-a31c-4204bcb0cf32',
        'irrigation',
        'Полив',
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf33'
    );


INSERT INTO
    public.groups (id, short_name, name, user_id)
VALUES
    (
        '49394b91-8ee5-4939-a31c-4204bcb0cf32',
        'cesspoll',
        'Септик',
        'ae9f4b91-8ee5-4939-a30c-4204bcb0cf33'
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
        component_id,
        device_id,
        name,
        category,
        type,
        version,
        settings,
        usage_type,
        telegram_notify
    )
VALUES
    (
        'b98d7199-cea3-43a8-a615-940b3a59ffa4',
        1,
        'irrigation_relay1',
        'Томати',
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
        component_id,
        device_id,
        name,
        category,
        type,
        version,
        settings,
        usage_type,
        telegram_notify
    )
VALUES
    (
        'a6157199-cea3-43a8-a615-940b3a59ffa4',
        2,
        'irrigation_relay1',
        'Огірки',
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
        component_id,
        device_id,
        name,
        category,
        type,
        version,
        settings,
        usage_type,
        telegram_notify
    )
VALUES
    (
        'cea37199-cea3-43a8-a615-940b3a59ffa4',
        3,
        'irrigation_relay1',
        'Полуниця Альтанка',
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
        component_id,
        device_id,
        name,
        category,
        type,
        version,
        settings,
        telegram_notify
    )
VALUES
    (
        '59551dc9-fa3f-4362-8a18-7678fd98c67b',
        1,
        'cesspoll_relay_sensor1',
        'Датчик рівня води в септику',
        'sensor',
        'POWER_CURRENT',
        'v1',
        NULL,
        false
    );

INSERT INTO
    public.components(
        id,
        component_id,
        device_id,
        name,
        category,
        type,
        version,
        settings,
        telegram_notify
    )
VALUES
    (
        '53dd36aa-fe23-4d48-ac0e-08948f122e09',
        2,
        'cesspoll_relay_sensor1',
        'Датчик увімкнення насосу в септику',
        'sensor',
        'POWER_CURRENT',
        'v1',
        NULL,
        false
    );


INSERT INTO
    public.components_groups(
        component_id,
        group_id
    )
VALUES
    (
        'b98d7199-cea3-43a8-a615-940b3a59ffa4',
        'ae9f4b91-8ee5-4939-a31c-4204bcb0cf32'
    );



INSERT INTO
    public.components_groups(
        component_id,
        group_id
    )
VALUES
    (
        'a6157199-cea3-43a8-a615-940b3a59ffa4',
        'ae9f4b91-8ee5-4939-a31c-4204bcb0cf32'
    );


INSERT INTO
    public.components_groups(
        component_id,
        group_id
    )
VALUES
    (
        'cea37199-cea3-43a8-a615-940b3a59ffa4',
        'ae9f4b91-8ee5-4939-a31c-4204bcb0cf32'
    );



INSERT INTO
    public.components_groups(
        component_id,
        group_id
    )
VALUES
    (
        '59551dc9-fa3f-4362-8a18-7678fd98c67b',
        '49394b91-8ee5-4939-a31c-4204bcb0cf32'
    );


INSERT INTO
    public.components_groups(
        component_id,
        group_id
    )
VALUES
    (
        '53dd36aa-fe23-4d48-ac0e-08948f122e09',
        '49394b91-8ee5-4939-a31c-4204bcb0cf32'
    );