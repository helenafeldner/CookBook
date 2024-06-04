-- Drop constraints if they exist
-- Drop tables if they exist
DROP TABLE IF EXISTS public.opskriftrating CASCADE;
DROP TABLE IF EXISTS public.opskriftingrediens CASCADE;
DROP TABLE IF EXISTS public.opskrift CASCADE;
DROP TABLE IF EXISTS public.ingredienser CASCADE;
DROP TABLE IF EXISTS public.ratingtype CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;

-- Create Users Table
CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    mail VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create Recipe Table
CREATE TABLE public.opskrift (
    oid SERIAL PRIMARY KEY,
    titel VARCHAR(50),
    comment VARCHAR(50)
);

INSERT INTO public.opskrift (oid, titel, comment) VALUES
    (1, 'risengrød', 'Mad man spiser til jul.'),
    (2, 'rødgrød', 'Mad man spiser til sommer.'),
    (3, 'flæskesteg', 'Mad man spiser til jul.');
    (4, 'svamperisotto', 'Svampe = klammo, men risotto er lækkert.')
    (5, 'spejlæg', 'Ren gourmetglæde.')

-- Create Ingredients Table
CREATE TABLE public.ingredienser (
    name VARCHAR(50) PRIMARY KEY
);

INSERT INTO public.ingredienser (name) VALUES ('gulerod'), ('tomat'), ('svin');

-- Drop the old primary key constraint on the opskriftrating table
ALTER TABLE public.opskriftrating DROP CONSTRAINT IF EXISTS opskriftrating_pkey;

-- Create Rating Type Table
CREATE TABLE public.ratingtype (
    stjerner INTEGER PRIMARY KEY,
    beskrivelse VARCHAR(50)
);

INSERT INTO public.ratingtype (stjerner, beskrivelse) VALUES
    (1, 'dårligt'),
    (2, 'spiseligt'),
    (3, 'ok'),
    (4, 'ikke ringe'),
    (5, 'lækkert');


-- Create Recipe Rating Table with a new primary key constraint
CREATE TABLE public.opskriftrating (
    id SERIAL PRIMARY KEY,
    oid INTEGER REFERENCES opskrift(oid),
    stjerner INTEGER REFERENCES ratingtype(stjerner)
);

INSERT INTO public.opskriftrating (oid, stjerner) VALUES (2, 5);

-- Create Recipe Ingredients Table
CREATE TABLE public.opskriftingrediens (
    oid INTEGER REFERENCES opskrift(oid),
    name VARCHAR(50) REFERENCES ingredienser(name),
    mængde INTEGER,
    PRIMARY KEY (oid, name)
);

INSERT INTO public.opskriftingrediens (oid, name, mængde) VALUES (2, 'tomat', 10);