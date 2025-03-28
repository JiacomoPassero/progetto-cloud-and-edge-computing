#!/bin/bash

flask db init;

#migrate allow to keep track of db changes and avoid applyinf directly or automatically
flask db migrate;

#apply migrate changes to db
flask db upgrade;

#start de application 
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app;

#mantain server running
tail -f /dev/null;