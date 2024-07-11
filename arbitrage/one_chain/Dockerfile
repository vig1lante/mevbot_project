FROM python:3.11

WORKDIR /app

COPY /arbitrage/one_chain /app/service
COPY .env /app
COPY config.json /app
COPY pyproject.toml /app
COPY poetry.lock /app
COPY /migrations /app/migrations
COPY /source /app/source
COPY /abis /app/abis
COPY alembic.ini /app
COPY service_settings.py /app


RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ENV PYTHONPATH="/app:/app/service"
EXPOSE 8081

CMD alembic upgrade head && python3 service/runservice.py


# sudo docker rm $(sudo docker ps -a -q)
# sudo docker ps -a
# sudo docker build . -t api_service
# sudo docker run -d api_service
# sudo docker logs {container_id} -f
# sudo docker exec -it {container_id} bash
# sudo docker run --publish 8081:8081 api_service
