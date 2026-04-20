def validate_zip(event):
    intent_name = lex.get_intent(event)
    entered_zip = lex.get_slot(event, 'ZipCode')
    ani_zip = lex.get_session_attribute(event, 'Retail_AniZipCode')

    if not entered_zip:
		message = "Please enter your zip code"
        return lex.elicit_slot_response(event, intent_name, 'ZipCode', message, lex.SSML)
		
    elif entered_zip.strip() == ani_zip.strip():
		message = 'Zip code validated.'
        return lex.delegate_intent_response(event, intent_name, lex.IN_PROGRESS, message, lex.SSML)
    else:
		message = 'Zip code does not match. Please try again.'
        return lex.elicit_slot_response(event, intent_name, 'ZipCode', message, lex.SSML)