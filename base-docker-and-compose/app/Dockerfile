FROM python:3.11-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

#entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# running command
CMD python manage.py run -h 0.0.0.0