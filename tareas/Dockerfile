FROM python:3.8
ARG postgres_host
ARG postgres_pass
ARG aws_access_key_id
ARG aws_secret_access_key
ARG aws_session_token
ARG sqs_queue_url
ARG sqs_queue_name
ENV POSTGRES_HOST=$postgres_host
ENV POSTGRES_PASS=$postgres_pass
ENV AWS_ACCESS_KEY_ID=$aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key
ENV AWS_SESSION_TOKEN=$aws_session_token
ENV SQS_QUEUE_URL=$sqs_queue_url
ENV SQS_QUEUE_NAME=$sqs_queue_name
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD . /app
RUN apt update -y --fix-missing && apt upgrade -y
RUN apt install -y --no-install-recommends libcurl4-nss-dev libssl-dev
RUN apt install -y ffmpeg
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh
WORKDIR /app
ENTRYPOINT ["sh", "entrypoint.sh"]