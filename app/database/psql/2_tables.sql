\connect smart_house
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

-- device SECTION 
CREATE TABLE public.devices(
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    last_known_ip TEXT,
    updated time without time zone
);

--  Line groups
CREATE TABLE public.elements_groups (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE public.elements_types(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.elements_categories(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.elements (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    name text NOT NULL,
    group_id uuid not null,
    device_id text DEFAULT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    settings jsonb,
    --  //time integer NOT NULL DEFAULT 10,
    --  //intervals integer NOT NULL DEFAULT 2,
    --  //time_wait integer NOT NULL DEFAULT 15,
    --  //relay_num integer,
    FOREIGN KEY(group_id) REFERENCES elements_groups(id)
    FOREIGN KEY(device_id) REFERENCES devices(name),
    FOREIGN KEY(type) REFERENCES elements_types(name),
    FOREIGN KEY(category) REFERENCES elements_categories(name),
);


CREATE TABLE public.actuators_autostart (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    description text NOT NULL,
    actuator_id uuid,
    start_type text default 'event',
    start_at text,
    active boolean default true,
    FOREIGN KEY(actuator_id) REFERENCES elements(id)
);

-- Queue section
CREATE TABLE public.life (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    interval_id TEXT,
    actuator_id UUID NOT NULL,
    expected_state jsonb NOT NULL,
    execution_time timestamp without time zone NOT NULL,
    --  rule_id INTEGER NOT NULL,
    --  state INTEGER DEFAULT 0 NOT NULL,
    --   active INTEGER DEFAULT 1 NOT NULL,
    --    time INTEGER default 0 NOT NULL,
    FOREIGN KEY(actuator_id) REFERENCES elements(id)
);