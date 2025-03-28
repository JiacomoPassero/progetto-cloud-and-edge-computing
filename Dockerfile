# Use an official Python runtime as a parent image
FROM python:3.11

#define workdir
WORKDIR /app

#copy application inside workdir
COPY . /app

#aggiornamento pip
RUN pip install --upgrade pip

# installare requirements
RUN pip install -r requirements.txt

#define default flask application
ENV FLASK_APP=app.py

#make first_start executable
run chmod +x first_start.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
ENTRYPOINT ["./first_start.sh"]