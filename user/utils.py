import os
import base64
import uuid


async def decode_and_save(base64_string: str) -> str:    
    uid = f"{uuid.uuid4()}.jpeg"
    path_to_save = os.path.join("uploads", "avatars", uid)
    
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",", 1)[1]

    image_data = base64.b64decode(base64_string)

    with open(path_to_save, "wb+") as f:
        f.write(image_data)

    return uid