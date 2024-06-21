import os
from app.utils.qdrant_utils import save_to_qdrant
from app.utils.file_utils import save_temp_file

def upload_to_qdrant(file_content: bytes, user_id: str, redis_client, job_description: str, session_id: str, voice: str, num_questions: int):
    try:
        file_path = save_temp_file(file_content, user_id)
        save_to_qdrant(file_path, user_id, session_id)
        
        key = f"session:{session_id}"
        redis_client.hset(key, "user_id", user_id)
        redis_client.hset(key, "job_description", job_description)
        redis_client.hset(key, "num_questions", num_questions)
        redis_client.hset(key, "voice", voice)
    except Exception as e:
        print(e)
