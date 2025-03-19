# Use an official Python runtime as a parent image
FROM python

#define default flask application
ENV FLASK_APP app.py

WORKDIR ./

#aggiornamento pip
RUN pip install --upgrade pip

# installare requirements
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

#run confgurations needed for the first start of the application
RUN "bash first_start.sh"

# Run app.py when the container launches
CMD ["flask" , "run"]