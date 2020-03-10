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