CREATE TABLE IF NOT EXISTS characters (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    type TEXT,
    gender TEXT,
    origin_name TEXT,
    location_name TEXT,
    image TEXT,
    url TEXT,
    created TIMESTAMPTZ
);
