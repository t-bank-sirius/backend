from datetime import timedelta
from fastapi.responses import JSONResponse


async def cookies(response: JSONResponse, access, refresh):
    response.set_cookie(
        key='access_token',
        value=access,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=timedelta(minutes=120).total_seconds()
        )
    
    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True,
        secure=True,
        samesite='strict',
        max_age=timedelta(days=14).total_seconds()
    )
    
    return response