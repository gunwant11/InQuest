def save_temp_file(file_content: bytes, user_id: str) -> str:
    file_path = f"/tmp/{user_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path
