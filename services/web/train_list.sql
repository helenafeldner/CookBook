--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7 (Homebrew)
-- Dumped by pg_dump version 14.7 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Drop constraints if they exist
ALTER TABLE IF EXISTS public.reviews DROP CONSTRAINT IF EXISTS reviews_uid_fkey;
ALTER TABLE IF EXISTS public.reviews DROP CONSTRAINT IF EXISTS reviews_tid_fkey;
ALTER TABLE IF EXISTS public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS public.trains DROP CONSTRAINT IF EXISTS trains_pkey;
ALTER TABLE IF EXISTS public.reviews DROP CONSTRAINT IF EXISTS reviews_pkey;
ALTER TABLE IF EXISTS public.listed_trains DROP CONSTRAINT IF EXISTS listed_trains_pkey;

-- Drop tables if they exist
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.trains;
DROP TABLE IF EXISTS public.reviews;
DROP TABLE IF EXISTS public.listed_trains;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: listed_trains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listed_trains (
    uid integer NOT NULL,
    tid integer NOT NULL
);


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reviews (
    uid integer NOT NULL,
    tid integer NOT NULL,
    rating integer,
    comment character(300)
);


--
-- Name: trains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trains (
    id integer NOT NULL,
    name text,
    operators text,
    family text,
    manufacturer text,
    power_supply text,
    max_speed_operational text,
    max_speed_designed text,
    max_speed_record text,
    in_service text,
    picture text
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name text,
    mail text,
    password text
);


--
-- Data for Name: listed_trains; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.listed_trains (uid, tid) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reviews (uid, tid, rating, comment) FROM stdin;
1	1	4	Great train! The Acela Express provides a comfortable and smooth ride. The speed is impressive.                                                                                                                                                                                                             
2	9	5	The AVE Class 100 is fantastic. The train is fast, and the seats are spacious and comfortable.                                                                                                                                                                                                              
3	14	3	The BR Class 43 (InterCity 125) is a classic train. It has a nostalgic charm, but the ride can be a bit bumpy.                                                                                                                                                                                              
4	20	5	The BR Class 395 Javelin is perfect for commuting. It offers a fast and reliable service.                                                                                                                                                                                                                   
5	30	4	The CRH1E is a great high-speed train. It provides a smooth and quiet journey.                                                                                                                                                                                                                              
                                                                                                                                                                                                              
\.


--
-- Data for Name: trains; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trains (id, name, operators, family, manufacturer, power_supply, max_speed_operational, max_speed_designed, max_speed_record, in_service, picture) FROM stdin;
1	Acela Express (1st generation)	Amtrak	TGV & LRC derived	Alstom Bombardier	25 kV 60 Hz AC 12 kV 60 Hz AC 12 kV 25 Hz AC	240 (150 mph)	266 (165 mph)	266 (165 mph)	2000	images/Acela Express (1st generation).png
2	Afrosiyob	Uzbekistan Railways	Talgo 250	Talgo	25 kV 50 Hz AC	250	250	\N	2011	images/Afrosiyob.png
3	AGV 575	NTV	AGV	Alstom	25 kV 50 Hz AC 3 kV DC	300	360	\N	2012	images/AGV 575.png
4	Alfa Pendular	CP	Pendolino	Fiat Ferroviaria Adtranz Siemens	25 kV 50 Hz AC	220[1]	250	\N	1999[1]	images/Alfa Pendular.png

\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, mail, password) FROM stdin;
1	John Doe	johndoe@example.com	pass123
2	Jane Smith	janesmith@example.com	hello456

\.


--
-- Name: listed_trains listed_trains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listed_trains
    ADD CONSTRAINT listed_trains_pkey PRIMARY KEY (uid, tid);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (uid, tid);


--
-- Name: trains trains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trains
    ADD CONSTRAINT trains_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_tid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_tid_fkey FOREIGN KEY (tid) REFERENCES public.trains(id);


--
-- Name: reviews reviews_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

