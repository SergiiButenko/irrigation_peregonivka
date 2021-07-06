\connect smart_house
INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'irrigation_relay1',
        'Контроллер поливу огорода',
        'Relay8ch',
        'v1'
    );

INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'irrigation_relay2',
        'Контроллер насосу поливу огорода'
        'Relay8ch',
        'v1'
    );

INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'greenhouse_relay1',
        'Контроллер підігріва теплиці'
        'Relay2ch',
        'v1'
    );

INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'greenhouse_relay2',
        'Освітлення в теплиці'
        'Relay2ch',
        'v1'

    );

INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'basement_relay1',
        'Освітлення на дворі'
        'Relay4ch',
        'v1'
    );

INSERT INTO
    public.devices(name, description, type, version)
VALUES
    (
        'kids_house_relay1',
        'Освітлення на дитячому будинку'
        'Relay8ch',
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
    public.components_categories(name, description)
VALUES
    (
        'temperature_sensor',
        'Датчик темеператури'
    );
