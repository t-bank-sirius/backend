from fastapi.responses import JSONResponse


async def is_auth(headers, auth):
    access_token = headers.get('Authorization')
    
    if access_token is None:
        return JSONResponse({'response': 'Вы не передали access token'}, 403)
    
    validate = auth.decode_token(access_token)
    
    if isinstance(validate, str):
        return JSONResponse({'response': validate}, 403)
    
    return validate