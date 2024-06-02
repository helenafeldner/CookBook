--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7 (Homebrew)
-- Dumped by pg_dump version 14.7 (Homebrew)

-- Drop constraints if they exist

-- Drop tables if they exist
DROP TABLE IF EXISTS public.opskriftrating;
DROP TABLE IF EXISTS public.opskriftingrediens;
DROP TABLE IF EXISTS public.opskrift;
DROP TABLE IF EXISTS public.ingredienser;
DROP TABLE IF EXISTS public.ratingtype;



--
-- Name: reviews; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.opskrift (
    oid SERIAL PRIMARY KEY,
    titel character(50),
--    rating integer,
    comment character(50)
);


--
-- Name: trains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ingredienser (
    name character(50) PRIMARY KEY 
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ratingtype (
    stjerner integer PRIMARY KEY,
    beskrivelse character(50)
);



CREATE TABLE public.opskriftrating (
    oid integer REFERENCES opskrift, 
    stjerner integer REFERENCES ratingtype
);
--
-- Data for Name: listed_trains; Type: TABLE DATA; Schema: public; Owner: -
--


CREATE TABLE public.opskriftingredienser (
    oid integer REFERENCES opskrift, 
    name character(50) REFERENCES ingredienser,
    mængde integer,
    PRIMARY KEY (oid, name)
);


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

