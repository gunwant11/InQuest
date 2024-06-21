FROM python:3.9-slim

RUN apt-get update && apt-get install -y libssl-dev libasound2

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]