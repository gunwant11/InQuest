import os
from app.utils.qdrant_utils import save_to_qdrant
from app.utils.file_utils import save_temp_file
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_core.messages import HumanMessage, SystemMessage
project = "pacific-vault-426816-s6"
location = "us-east5"

model = ChatAnthropicVertex(
    model_name="claude-3-5-sonnet@20240620",
    project=project,
    location=location,
    max_tokens=250,
)

def upload_to_qdrant(file_content: bytes, user_id: str, redis_client, job_description: str, session_id: str, voice: str, num_questions: int, role: str):
    try:
        file_path = save_temp_file(file_content, user_id)
        messages = [
    SystemMessage(content=" the job description summarize in short and crisp to the point, keeping the importent details, in two lines"),
    HumanMessage(content=job_description),
        ]
        jd =  model.invoke(messages)
        save_to_qdrant(file_path, user_id, session_id)
        
        key = f"session:{session_id}"
        redis_client.hset(key, "user_id", user_id)
        redis_client.hset(key, "job_description", jd.content)
        redis_client.hset(key, "num_questions", num_questions)
        redis_client.hset(key, "voice", voice)
        redis_client.hset(key, "role", role)
    except Exception as e:
        print(e)
