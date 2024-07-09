FROM python:3.9-slim

RUN apt-get update && apt-get install -y libssl-dev libasound2

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# download google cloud sdk
RUN apt-get install -y curl
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
RUN tar zxvf google-cloud-cli-linux-x86_64.tar.gz
RUN ./google-cloud-sdk/install.sh -q

# initialize google cloud sdk
RUN ./google-cloud-sdk/bin/gcloud init --console-only

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]