from aiohttp import ClientSession, ClientTimeout
from fastapi.responses import JSONResponse


async def say_hello(chat_id: int, init_message: str):
    data_to_bot = {
        'chat_id': chat_id,
        'init_message': init_message
    }
    try:
        async with ClientSession() as session:
            async with session.post('http://127.0.0.1:5000/hello', json=data_to_bot) as response:
                print(f"Отправили привет в бот: {response.status}")
    except Exception as er:
        print('Ошибка в функции say_hello', er)


async def llm(message: str, user_id: str, role: str, system_prompt: str, image_base64: str = ''):
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
            async with session.post('http://host.docker.internal:8080/generate', json=data_to_request) as response:
                resp = await response.json()
                return JSONResponse(content={'message': resp['message'], 'image': resp['image']})
    except Exception as er:
        print('Ошибка в функции llm', er)
        return JSONResponse(content='Ошибка на стороне llm :( (Мы это починим, честно)', status_code=400)


async def generate_image(data: dict):
    timeout = ClientTimeout(total=240)
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post('http://host.docker.internal:8080/create_avatar/', json=data) as response:
                resp = await response.json()
                return JSONResponse(content={'image': resp['image']})
    except Exception as er:
        print('Ошибка в функции generate_image', er)
        return JSONResponse(content='Ошибка на стороне llm_generate_image :( (Мы это починим, честно)', status_code=400)


async def create_character(data: dict):
    timeout = ClientTimeout(total=240)
    
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.post('http://host.docker.internal:8080/create_character/', json=data) as response:
                resp = await response.json()
                return resp
    except Exception as er:
        print('Ошибка в функции create_character', er)
        return JSONResponse(content='Ошибка на стороне llm_create_character :( (Мы это починим, честно)', status_code=400)