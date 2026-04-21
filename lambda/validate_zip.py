def validate_zip(event):
    intent_name = lex.get_intent(event)
    entered_zip = lex.get_slot(event, 'ZipCode')
    ani_zip = lex.get_session_attribute(event, 'Retail_AniZipCode')
    
    # No input — silence
    if not entered_zip:
        silence_input_counter(event)
        message = "Please enter your zip code"
        return lex.elicit_slot_response(event, intent_name, 'ZipCode', message, lex.SSML)
    
    # ZIP matches — validated
    elif entered_zip.strip() == ani_zip.strip():
        reset_silence_input_counter(event)
        reset_no_match_counter(event)
        message = 'Zip code validated.'
        return lex.delegate_intent_response(event, intent_name, lex.IN_PROGRESS, message, lex.SSML)
    
    # ZIP is not 5 digits — invalid format
    elif len(entered_zip.strip()) != 5:
        invalid_input_counter(event)
        message = 'Please enter a valid 5 digit zip code.'
        return lex.elicit_slot_response(event, intent_name, 'ZipCode', message, lex.SSML)
    
    # ZIP is 5 digits but doesn't match — no match
    else:
        no_match_counter(event)
        message = 'Zip code does not match. Please try again.'
        return lex.elicit_slot_response(event, intent_name, 'ZipCode', message, lex.SSML)
        
        
        
        
def no_match_counter(event):
	session_attributes = lex.get_session_attributes(event)
    count = int(session_attributes.get("noMatchInputCount", 0))
    count += 1
    lex.set_session_attribute(event, "noMatchInputCount", str(count))
    return count
    
def silence_input_counter(event):
    session_attributes = lex.get_session_attributes(event)
    count = int(session_attributes.get('silenceInput', 0))
    count += 1
    lex.set_session_attribute(event, "silenceInput", str(count))
    return count 
    
def reset_silence_input_counter(event):
    lex.set_session_attribute(event, "silenceInput", "0")
    
def reset_no_match_counter(event):
    lex.set_session_attribute(event, "noMatchInputCount", "0")