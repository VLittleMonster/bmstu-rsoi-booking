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
-- Name: users; Type: TABLE; Schema: public; Owner: program
--

CREATE TABLE public.users (
    id integer NOT NULL,
	username varchar(80) NOT NULL,
	password_hash varchar NOT NULL,
	role varchar(80) NOT NULL CHECK (role IN ('user', 'admin')),
	first_name varchar(80) NOT NULL,
	last_name varchar(80) NOT NULL,
	patronymic varchar(80) DEFAULT '',
	phone_number varchar(15) NOT NULL,
	email varchar NOT NULL
);


ALTER TABLE public.users OWNER TO program;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: program
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO program;

--
-- Name: ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: program
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: ticket id; Type: DEFAULT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: program
--

COPY public.users (id, username, password_hash, role, first_name, last_name, phone_number, email) FROM stdin;
1	Test Max	33a52b7f827a648f9d6a527cb887c838b68357ffcf94ab257d0f27129709d088.9ab398f7c32c22ad8d056c546653fabc	user	Max	Test	88005553535	test-max@gmall.com
2	admin	2a6aa69d0c4ffff2cc4dd3115fb3f64c75fdb05523eaa73998c6ae2679d190fc.3f8d325d2367c347649e7a9312bb892b	admin	Admin	Adminov	+79779917395	admin@admin.ru
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: program
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: program
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- PostgreSQL database dump complete
--