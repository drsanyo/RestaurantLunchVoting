\c restaurantlunchvoting

-- Table: public.restaurant

-- DROP TABLE public.restaurant;

CREATE TABLE public.restaurant
(
    rst_id SERIAL NOT NULL,
    rst_name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT restaurant_pkey PRIMARY KEY (rst_id),
    CONSTRAINT uq_rst_name UNIQUE (rst_name)
)

TABLESPACE pg_default;

ALTER TABLE public.restaurant
    OWNER to docker;
    
CREATE OR REPLACE FUNCTION pr_log_out(prm_user VARCHAR)
RETURNS int
LANGUAGE plpgsql    
AS $$
BEGIN
    DELETE FROM authtoken_token
    WHERE user_id = (SELECT id FROM auth_user WHERE username = prm_user);
    RETURN 0;
END;
$$;

CREATE OR REPLACE FUNCTION pr_create_restaurant(prm_name VARCHAR)
RETURNS int
LANGUAGE plpgsql    
AS $$
DECLARE
  new_rst_id INTEGER;
BEGIN
    INSERT INTO public.restaurant(rst_name)
    VALUES (prm_name)
    RETURNING rst_id INTO new_rst_id;
    
    RETURN new_rst_id;
END;
$$;


-- Table: public.menu

-- DROP TABLE public.menu;

CREATE TABLE public.menu
(
    menu_id serial NOT NULL,
    menu_rst_id integer NOT NULL,
    menu_create_date date NOT NULL DEFAULT CURRENT_DATE,
    menu_auth_user_id integer NOT NULL,
    menu_file_name character varying(250) COLLATE pg_catalog."default" NOT NULL,
    menu_file_body bytea NOT NULL,
    CONSTRAINT menu_pkey PRIMARY KEY (menu_id),
    CONSTRAINT uq_menu_rst_id_create_date UNIQUE (menu_rst_id, menu_create_date),
    FOREIGN KEY (menu_rst_id) REFERENCES restaurant (rst_id),
    FOREIGN KEY (menu_auth_user_id) REFERENCES auth_user (id)
)

TABLESPACE pg_default;

ALTER TABLE public.menu
    OWNER to docker;
	
	
CREATE OR REPLACE FUNCTION pr_upload_menu(
	prm_rst_name VARCHAR,
	prm_user_name VARCHAR,
	prm_file_name VARCHAR,
	prm_file_body BYTEA
)
RETURNS int
LANGUAGE plpgsql    
AS $$
DECLARE
  new_menu_id INTEGER;
  _rst_id INTEGER;
  _user_id INTEGER;
BEGIN
	SELECT rst_id
	INTO _rst_id
	FROM restaurant
	WHERE rst_name = prm_rst_name;
	
	IF _rst_id IS NULL THEN
		RAISE EXCEPTION 'Unknown reataurant: %, please add restaurant first.', prm_rst_name;
	END IF;
	
	SELECT id
	INTO _user_id
	FROM auth_user
	WHERE username = prm_user_name;
	
	IF _user_id IS NULL THEN
		RAISE EXCEPTION 'Unknown user: %, please add user first.', prm_user_name;
	END IF;
	

	SELECT menu_id
	INTO new_menu_id
	FROM menu	
	WHERE (1=1)
		AND menu_rst_id = _rst_id
		AND menu_create_date = current_date;
	
	IF new_menu_id IS NOT NULL THEN
		RAISE EXCEPTION 'Menu for restaurant: % already exists, please delete menu first.', prm_rst_name;
	END IF;

    INSERT INTO public.menu(menu_rst_id, menu_auth_user_id, menu_file_name, menu_file_body)
	VALUES (_rst_id, _user_id, prm_file_name, prm_file_body)
    RETURNING menu_id INTO new_menu_id;
    
    RETURN new_menu_id;
END;
$$;


-- View: public.vw_current_day_menu

-- DROP VIEW public.vw_current_day_menu;

CREATE OR REPLACE VIEW public.vw_current_day_menu
 AS
 SELECT menu.menu_id AS id,
    restaurant.rst_name,
    menu.menu_file_body AS menu
   FROM menu
     JOIN restaurant ON restaurant.rst_id = menu.menu_rst_id
  WHERE menu.menu_create_date = CURRENT_DATE;

ALTER TABLE public.vw_current_day_menu
    OWNER TO docker;


-- Table: public.user_vote

-- DROP TABLE public.user_vote;

CREATE TABLE public.user_vote
(
    uv_id serial NOT NULL,
    uv_date date NOT NULL DEFAULT CURRENT_DATE,
    uv_rst_id integer NOT NULL,
    uv_auth_user_id integer NOT NULL,
    CONSTRAINT user_vote_pkey PRIMARY KEY (uv_id),
    CONSTRAINT uq_date_rst_user UNIQUE (uv_date, uv_rst_id, uv_auth_user_id),
	FOREIGN KEY (uv_rst_id) REFERENCES restaurant (rst_id),
	FOREIGN KEY (uv_auth_user_id) REFERENCES auth_user (id)
)

TABLESPACE pg_default;

ALTER TABLE public.user_vote
    OWNER to docker;
	
	
CREATE OR REPLACE FUNCTION pr_user_vote(
	prm_rst_name VARCHAR,
	prm_user_name VARCHAR
)
RETURNS int
LANGUAGE plpgsql    
AS $$
DECLARE
  new_uv_id INTEGER;
  _rst_id INTEGER;
  _user_id INTEGER;
  _voted_count INTEGER;
BEGIN
	SELECT rst_id
	INTO _rst_id
	FROM restaurant
	WHERE rst_name = prm_rst_name;
	
	IF _rst_id IS NULL THEN
		RAISE EXCEPTION 'Unknown reataurant: %, please add restaurant first.', prm_rst_name;
	END IF;
	
	SELECT id
	INTO _user_id
	FROM auth_user
	WHERE username = prm_user_name;
	
	IF _user_id IS NULL THEN
		RAISE EXCEPTION 'Unknown user: %, please add user first.', prm_user_name;
	END IF;
	

	SELECT uv_id
	INTO new_uv_id
	FROM user_vote	
	WHERE (1=1)
		AND uv_rst_id = _rst_id
		AND uv_auth_user_id = _user_id 
		AND uv_date = current_date;
	
	IF new_uv_id IS NOT NULL THEN
		RAISE EXCEPTION 'User has already voted for this restaurant (%) today!', prm_rst_name;
	END IF;

    INSERT INTO public.user_vote(
	uv_rst_id, uv_auth_user_id)
	VALUES (_rst_id, _user_id);
    
	SELECT COUNT(0)
	INTO _voted_count
	FROM user_vote
	WHERE (1=1)
		AND uv_rst_id = _rst_id
		AND uv_date = current_date;
	
    RETURN _voted_count;
END;
$$;
