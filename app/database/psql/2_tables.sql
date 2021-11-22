\connect smart_house
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

-- users section
CREATE TABLE public.users(
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    username TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    email TEXT,
    full_name TEXT,
    disabled BOOL DEFAULT false
);

-- device SECTION 
CREATE TABLE public.devices(
    id TEXT NOT NULL PRIMARY KEY,
    description TEXT,
    type TEXT NOT NULL,
    version TEXT NOT NULL,
    last_known_ip TEXT,
    settings jsonb,
    updated time without time zone
);

--  Line groups
CREATE TABLE public.groups (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    short_name TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    user_id uuid NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE public.components_types(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.components_categories(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.components_purpose(
    name TEXT NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE public.device_components (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    device_id TEXT,
    mapped_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,
    version TEXT NOT NULL,
    purpose TEXT,
    settings jsonb,
    telegram_notify BOOL NOT NULL,
    telegram_user TEXT DEFAULT '-315337397',
    default_state TEXT,
    UNIQUE (device_id, mapped_id),
    FOREIGN KEY(device_id) REFERENCES devices(id),
    FOREIGN KEY(type) REFERENCES components_types(name),
    FOREIGN KEY(category) REFERENCES components_categories(name),
    FOREIGN KEY(purpose) REFERENCES components_purpose(name)
);

CREATE TABLE public.components_groups (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    device_component_id uuid NOT NULL,
    group_id uuid NOT NULL,
    FOREIGN KEY(device_component_id) REFERENCES device_components(id),
    FOREIGN KEY(group_id) REFERENCES groups(id)
);

-- Queue section
CREATE TABLE public.intervals (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    device_component_id uuid NOT NULL,
    execution_time timestamp without time zone NOT NULL,
    state TEXT NOT NULL DEFAULT 'new',
    user_id uuid NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(device_component_id) REFERENCES device_components(id)
);

CREATE TABLE public.rules (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    interval_id uuid,
    device_component_id uuid NOT NULL,
    expected_state TEXT NOT NULL,
    execution_time timestamp without time zone NOT NULL,
    state TEXT NOT NULL DEFAULT 'new',
    FOREIGN KEY(device_component_id) REFERENCES device_components(id),
    FOREIGN KEY(interval_id) REFERENCES intervals(id)
);