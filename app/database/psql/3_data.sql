\connect smart_house
INSERT INTO
    public.devices(name, description)
VALUES
    (
        'irrigation_relay1',
        'Контроллер поливу огорода'
    );

INSERT INTO
    public.devices(name, description)
VALUES
    (
        'irrigation_relay2',
        'Контроллер насосу поливу огорода'
    );

INSERT INTO
    public.devices(name, description)
VALUES
    (
        'greenhouse_relay1',
        'Контроллер підігріва теплиці'
    );

INSERT INTO
    public.devices(name, description)
VALUES
    (
        'greenhouse_relay2',
        'Освітлення в теплиці'
    );

INSERT INTO
    public.devices(name, description)
VALUES
    (
        'basement_relay1',
        'Освітлення на дворі'
    );

INSERT INTO
    public.devices(name, description)
VALUES
    (
        'kids_house_relay1',
        'Освітлення на дитячому будинку'
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
    public.components_types(name, description)
VALUES
    (
        'actuator',
        'Тип девайсу, що виконує якусь дію'
    );

INSERT INTO
    public.components_types(name, description)
VALUES
    (
        'sensor',
        'Тип девайсу, що лише генерує дані'
    );

INSERT INTO
    public.components_categories(name, description)
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
