-- Table: public.restaurant

-- DROP TABLE public.restaurant;

CREATE TABLE public.restaurant
(
    rst_id integer NOT NULL DEFAULT nextval('restaurant_rst_id_seq'::regclass),
    rst_name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT restaurant_pkey PRIMARY KEY (rst_id),
    CONSTRAINT uq_rst_name UNIQUE (rst_name)
)

TABLESPACE pg_default;

ALTER TABLE public.restaurant
    OWNER to docker;