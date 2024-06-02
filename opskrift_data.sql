SELECT * FROM opskrift;

DELETE FROM opskrift; 

CREATE TABLE public.opskrift (
    oid SERIAL PRIMARY KEY,
    titel character(50),
--    rating integer,
    comment character(50)
);

INSERT INTO public.opskrift(
	titel, comment)
	VALUES ('risengrød', 'Mad man spiser til jul.'), ('rødgrød', 'Mad man spiser til sommer.'), ('flæskesteg', 'Mad man spiser til jul.');

