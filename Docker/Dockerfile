FROM python:3.12-slim

COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

COPY locust-tasks locust-tasks

RUN chmod -R 755 /locust-tasks

COPY /locust-tasks/docker-entrypoint.sh /

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

#CMD ["locust", "-f", "/locust-tasks/basic.py"]

EXPOSE 5557 5558 9646 8089 3000