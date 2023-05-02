# Using official python runtime base image
FROM python:3.10
RUN apt update
RUN apt-get install -y postgresql-client

ENV PYTHONUNBUFFERED=1
# Set the application directory
WORKDIR /manufacturing
COPY requirements.txt /manufacturing/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /manufacturing/

ENTRYPOINT ["/manufacturing/entrypoint.sh"]

