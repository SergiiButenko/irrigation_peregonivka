\connect smart_house
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

-- device SECTION 
CREATE TABLE public.devices(
    id TEXT NOT NULL PRIMARY KEY,
    description TEXT,
    type TEXT NOT NULL,
    version TEXT NOT NULL,
    last_known_ip TEXT,
    updated time without time zone
);

--  Line groups
CREATE TABLE public.components_groups (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE public.components_types(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.components_categories(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.components (
    id INTEGER NOT NULL,
    device_id TEXT,
    name text NOT NULL,
    group_id uuid NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,
    version TEXT NOT NULL,
    settings jsonb,
    telegram_user TEXT DEFAULT '-315337397',
    usage_type TEXT,
    --  //time integer NOT NULL DEFAULT 10,
    --  //intervals integer NOT NULL DEFAULT 2,
    --  //time_wait integer NOT NULL DEFAULT 15,
    --  //relay_num integer,
    UNIQUE (device_id, id),
    FOREIGN KEY(group_id) REFERENCES components_groups(id),
    FOREIGN KEY(device_id) REFERENCES devices(id),
    FOREIGN KEY(type) REFERENCES components_types(name),
    FOREIGN KEY(category) REFERENCES components_categories(name)
);


-- Queue section
CREATE TABLE public.rules (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    interval_uuid uuid,
    device_id TEXT NOT NULL,
    actuator_id INTEGER NOT NULL,
    expected_state TEXT NOT NULL,
    execution_time timestamp without time zone NOT NULL,
    state TEXT NOT NULL DEFAULT 'new',
    FOREIGN KEY(actuator_id, device_id) REFERENCES components(id, device_id)
);