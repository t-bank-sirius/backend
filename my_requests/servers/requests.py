from fastapi import HTTPException
from aiohttp import ClientSession, ClientTimeout
from fastapi.responses import JSONResponse
from models.settings import AppSettings


app = AppSettings()


async def say_hello(chat_id: int, init_message: str):
    url = app.BOT_URL
    
    data_to_bot = {
        'chat_id': chat_id,
        'init_message': init_message
    }
    try:
        async with ClientSession() as session:
            async with session.post(f'{url}/hello', json=data_to_bot) as response:
                print(f"Отправили привет в бот: {response.status}")
    except Exception as er:
        print('Ошибка в функции say_hello', er)


async def llm(message: str, user_id: str, role: str, system_prompt: str, image_base64: str = ''):
    url = app.LLM_URL
    
    data_to_request = {
        "message": message,
        "user_id": user_id,
        "role": role,
        "system_prompt": system_prompt,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.1,
        'image': image_base64,
        "max_iterations": 3
    }
    
    timeout = ClientTimeout(total=240)
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f'{url}/generate', json=data_to_request) as response:
                resp = await response.json()
                return JSONResponse(content={'message': resp['message'], 'image': resp['image']})
            
    except Exception as er:
        print('Ошибка в функции llm', er)
        raise HTTPException(detail='Ошибка на стороне llm :( (Мы это починим, честно)', status_code=400)


async def generate_image(data: dict):
    url = app.LLM_URL
    
    timeout = ClientTimeout(total=240)
    data_send = {
        'json_data': str(data)
    }
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f'{url}/create_avatar/', json=data_send) as response:
                resp = await response.json()
                return JSONResponse(content={'image': resp['image'], 'error': resp['error']})
            
    except Exception as er:
        print('Ошибка в функции generate_image', er)
        raise HTTPException(detail='Ошибка на стороне llm_generate_image :( (Мы это починим, честно)', status_code=400)


async def create_character(data: dict):
    url = app.LLM_URL
    
    timeout = ClientTimeout(total=240)
    data_send = {
        'json_data': str(data)
    }
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f'{url}/create_characters/', json=data_send) as response:
                resp = await response.json()
                return resp
            
    except Exception as er:
        print('Ошибка в функции create_character', er)
        raise HTTPException(detail='Ошибка на стороне llm_create_character :( (Мы это починим, честно)', status_code=400)


async def clear_context(user_id: int, role: str):
    url = app.LLM_URL
    
    timeout = ClientTimeout(total=240)
    data_send = {
        "user_id": str(user_id),
        "role": role
    }
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f'{url}/delete_context/', json=data_send) as response:
                resp = await response.json()
                return resp
            
    except Exception as er:
        print('Ошибка в функции create_character', er)
        raise HTTPException(detail='Ошибка на стороне llm_create_character :( (Мы это починим, честно)', status_code=400)


async def add_face(user_id: int, name: str, image: str):
    url = app.LTM_URL
    
    timeout = ClientTimeout(total=240)
    data_send = {
        "user_id": str(user_id),
        "name": name,
        "image": image 
}
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post(f'{url}/add_face/', json=data_send) as response:
                resp = await response.json()
                return resp
            
    except Exception as er:
        print('Ошибка в функции create_character', er)
        raise HTTPException(detail='Ошибка на стороне llm_create_character :( (Мы это починим, честно)', status_code=400)