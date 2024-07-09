FROM python:3.9-slim

RUN apt-get update && apt-get install -y libssl-dev libasound2

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Google Cloud SDK
RUN apt-get install -y curl gnupg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y google-cloud-sdk

# Set environment variable for service account key
ENV GOOGLE_APPLICATION_CREDENTIALS=service-account.json

COPY . .

# Activate service account
RUN gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]