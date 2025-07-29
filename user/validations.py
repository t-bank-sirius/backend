from fastapi import Depends, Request, HTTPException
from auth.auth_conf import UserAuth


async def is_auth(request: Request, auth: UserAuth = Depends()):
    access_token = request.headers.get('Authorization', 'None')
    access_token = access_token.split('Bearer ')[-1]

    if access_token is None:
        raise HTTPException(detail='Вы не передали access token', status_code=403)
    
    validate = await auth.decode_token(access_token)
    
    if isinstance(validate, str):
        raise HTTPException(detail=validate, status_code=403)
    
    return validate


async def is_auth_headers(request: Request, auth: UserAuth = Depends()):
    header_type = auth.app_secret.HEADER_TYPE
    jwt_secret = auth.jwt_secret.SECRET
    
    headers = request.headers
    valid_header = headers.get(header_type)
    
    if valid_header != jwt_secret:
        raise HTTPException(detail='Access denied. Please, set header!', status_code=403)
    
    return True