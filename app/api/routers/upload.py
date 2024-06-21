from fastapi import APIRouter, File, Form, UploadFile, Depends
from ...services import upload_service
from ...db import get_redis_client
router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    user_id: str = Form(...),
    session_id: str = Form(...),
    voice: str = Form(...),
    num_questions: int = Form(...),
    redis_client = Depends(get_redis_client)
):
    file_content = await file.read()
    upload_service.upload_to_qdrant(file_content, user_id, redis_client, job_description, session_id, voice, num_questions)
    return {"status": "uploaded"}
