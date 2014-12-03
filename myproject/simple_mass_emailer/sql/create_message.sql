
CREATE OR REPLACE FUNCTION create_message(
    p_template_code text,
    OUT return_id int,
    OUT status_message text
)
AS $$
DECLARE
    t_emailtemplate_id int;
    t_template_code text;
    t_email text;
    t_url_key_code text;
    t_message_from text;
    t_message_subject text;
    t_message_text text;

    t_message_html text;
    t_email_html text;
    t_email_text text;
    t_emailmessage_id int;

    t_time_created timestamp;
    t_target text;
    t_recruit_email text;

    t_sponsor_email text;
    t_sponsor_first_name text;
    t_sponsor_last_name text;
    t_loop_count int = 0;
BEGIN
    SELECT id, template_code, target, message_from,
            message_subject, message_text, message_html
        INTO t_emailtemplate_id, t_template_code, t_target, t_message_from,
            t_message_subject, t_message_text, t_message_html
        FROM simple_mass_emailer_emailtemplate
        WHERE template_code = p_template_code;

    IF t_emailtemplate_id IS NULL THEN
        -- Makes no sense to continue with a p_template_code that does not exist.
        return_id := -1;
        status_message := 'Error: Template code not found.';
        RETURN;
    END IF;

    -- Get rid of return characters in html message because Gmail and others
    -- are not too friendly with html email message that contain carriage-returns.
    t_message_html := regexp_replace(t_message_html, E'[\\n\\r\\u2028]+', ' ', 'g');

    -- Loop through simple-mass-emailer_recruit and create email message
    -- record in simple-mass-emailer_emailmessage.
    FOR t_recruit_email, t_sponsor_email, t_sponsor_first_name, t_sponsor_last_name IN
        SELECT A.email, B.email, B.first_name, B.last_name
            FROM simple_mass_emailer_recruit A, auth_user B
            WHERE A.sponsor_id = B.id
            ORDER BY B.id
    LOOP

        -- Check if a record exists in simple-mass-emailer_emailmessage.
        SELECT A.id
            INTO t_emailmessage_id
            FROM simple_mass_emailer_emailmessage A, simple_mass_emailer_emailtemplate B
            WHERE A.email = t_recruit_email
                AND A.email_template_id = B.id
                AND B.template_code = p_template_code;

        -- Create a random md5 hash.
        t_url_key_code := md5(random()::text);
        t_email_html := t_message_html;
        t_email_text := t_message_text;

        -----------------------------------------------------------------------------------------
        --
        -- This is where preparation of the email message happens.
        --
        -- The general format is:
        -- t_emailmessage := replace(t_emailmessage, 'ANY_STRING_YOU_WANT_REPLACED', t_VARIABLE);
        --
        -- Where:
        --    ANY_STRING_YOU_WANT_REPLACED = the string you want replaced in the
        --         template messge.
        --    t_VARIABLE = the replacement string from any "t_*" variable in this
        --         PostgreSQL stored function.
        --
        t_email_html := replace(t_email_html, '##_RECRUIT_EMAIL_##', t_recruit_email);
        t_email_html := replace(t_email_html, '##_SPONSOR_EMAIL_##', t_sponsor_email);
        t_email_html := replace(t_email_html, '##_SPONSOR_##', t_sponsor_first_name||' '||t_sponsor_last_name);
        t_email_html := replace(t_email_html, '##_MD5RANDOM_##', t_url_key_code);
        --
        t_email_text := replace(t_email_text, '##_RECRUIT_EMAIL_##', t_recruit_email);
        t_email_text := replace(t_email_text, '##_SPONSOR_EMAIL_##', t_sponsor_email);
        t_email_text := replace(t_email_text, '##_SPONSOR_##', t_sponsor_first_name||' '||t_sponsor_last_name);
        t_email_text := replace(t_email_text, '##_MD5RANDOM_##', t_url_key_code);
        --
        -----------------------------------------------------------------------------------------

        -- RAISE NOTICE 't_emailmessage = %', t_emailmessage;

        IF t_emailmessage_id IS NULL THEN
            -- No record in simple-mass-emailer_emailmessage so create it.
            INSERT INTO simple_mass_emailer_emailmessage (
                email, message_from, message_text, message_html, url_key_code,
                email_template_id, time_created, message_subject)
            VALUES (
                t_recruit_email, t_message_from, t_email_text, t_email_html, t_url_key_code,
                t_emailtemplate_id, now(), t_message_subject)
            RETURNING id INTO t_emailmessage_id;

        ELSE
            -- An email message record already exists so just update it.
            UPDATE simple_mass_emailer_emailmessage
                SET email = t_recruit_email,
                    message_from = t_message_from,
                    message_text = t_email_text,
                    message_html = t_email_html,
                    url_key_code = t_url_key_code,
                    email_template_id = t_emailtemplate_id,
                    time_created = now(),
                    message_subject = t_message_subject
                WHERE id = t_emailmessage_id;

        END IF;
        t_loop_count := t_loop_count + 1;
    END LOOP;

    return_id := t_loop_count;
    status_message := 'Success: Email records created.';
END;
$$ LANGUAGE plpgsql;
