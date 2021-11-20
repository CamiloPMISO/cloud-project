FROM python:3.8
ARG postgres_host
ARG postgres_pass
ARG redis_host
ARG aws_access_key_id
ARG aws_secret_access_key
ARG aws_session_token
ENV POSTGRES_HOST=$postgres_host
ENV POSTGRES_PASS=$postgres_pass
ENV REDIS_HOST=$redis_host
ENV AWS_ACCES_KEY_ID=$aws_access_key_id
ENV AWS_SECRET_ACCES_KEY=$aws_secret_access_key
ENV AWS_SESSION_TOKEN=$aws_session_token
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD . /app
RUN apt update -y --fix-missing && apt upgrade -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["sh", "entrypoint.sh"]