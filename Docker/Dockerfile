#DOCKER IMAGE MASTER

FROM python:3.9-slim



# Install packages
COPY requirements.txt /tmp/

ADD prometheus.yml /etc/prometheus/

RUN pip install --requirement /tmp/requirements.txt

# Add tasks directory
COPY locust-tasks locust-tasks


#COPY cert cert

# Set the entrypoint
COPY docker-entrypoint.sh /

WORKDIR /locust-tasks

RUN chmod +x docker-entrypoint.sh



ENTRYPOINT ["/docker-entrypoint.sh"]

#CMD ["locust", "-f", "/locust-tasks/basic.py"]


EXPOSE 5557 5558 9646 8089 3000