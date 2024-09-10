--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: hotels; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.hotels (
    id integer NOT NULL PRIMARY KEY,
    hotel_uid uuid NOT NULL UNIQUE,
    name varchar(255) NOT NULL,
    country varchar(80) NOT NULL,
    city varchar(80) NOT NULL,
    adress varchar(255) NOT NULL,
    stars integer,
    price integer NOT NULL
);

ALTER TABLE public.hotels OWNER TO program;

--
-- Name: hotels_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.hotels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hotels_id_seq OWNER TO program;

--
-- Name: hotels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.hotels_id_seq OWNED BY public.hotels.id;


--
-- Name: hotels id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.hotels ALTER COLUMN id SET DEFAULT nextval('public.hotels_id_seq'::regclass);


--
-- Data for Name: hotels; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.hotels (id, hotel_uid, name, country, city, adress, stars, price) FROM stdin;
1	049161bb-badd-4fa8-9d90-87c9a82b0668	Jomtien Garden Palace	Thailand	Pattaya	Jomtien st., 69	3	2599
2	049161bb-badd-4fa8-9d90-87c9a82b0667	Lady Gaga Spa Resort	USA	Los Angeles	Hot Avenue, 28	4	5000
3	049161bb-badd-4fa8-9d90-87c9a82b0666	Cortez Blood Resort	USA	NY	Taylor st., 69	3	3228
4	049161bb-badd-4fa8-9d90-87c9a82b0665	Delphin Botanic Resort	Turkey	Alanya	Amy Derya st., 64	5	2500
5	049161bb-badd-4fa8-9d90-87c9a82b0664	Delphin Premium Resort	Turkey	Alanya	Amy Derya st., 65	5	3500
6	049161bb-badd-4fa8-9d90-87c9a82b0663	Delphin Platinum Resort	Turkey	Alanya	Amy Derya st., 66	5	5500
\.


--
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.hotels_id_seq', 1, false);


--
-- Name: hotels hotels_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_pkey PRIMARY KEY (id);


--
-- Name: hotels hotels_hotel_uid_key; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_hotel_uid_key UNIQUE (hotel_uid);


--
-- Name: ix_hotel_id; Type: INDEX; Schema: public; Owner: program
--

CREATE INDEX ix_hotel_id ON public.hotels USING btree (id);


--
-- PostgreSQL database dump complete
--