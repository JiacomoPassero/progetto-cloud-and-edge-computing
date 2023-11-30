# Base Docker and Compose Project
## Development History details

Let's say you follow me in the development of this repo. I will explain step that led me to the final version of this app.

First of all I want to develop a Flask app. Hence, I will use a virtualenv with the required dependencies and some file for a better handling of Flask project.

## starting point
Let's say I want to build a Flask app with SQLAlchemy and a Postgresql Database. The structure of the folder will look like:
```
base-docker-and-compose
|
└─── app/
    |
    └─── app.py 
    |
    └─── manage.py
    |
    └─── mixin.py
|
└─── run-local.sh
|
└─── requirements.txt
```

### `app` folder
It contains all file regarding app being developed

### `app/app.py`
It contains the core of the app. Some key aspects:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite://")
```
Everything that must be configured in the project is better off with an environment variable, eventaully giving a default value. In this example the database uri could default on `sqlite://` but instead of hard-coding Postgres better taking it from an environment variable.

```python
db = SQLAlchemy(app)
```
Let's initialie DB with SQLAlchemy

```python
class Worker(db.Model, Serializer):
```
Let's define a database table by defining a class using SQLAlchemy notation. Moreover the class inherit from `Serializer` class, a class I defined to make so SQLAlchemy query result serilizable, hence allowing a "jsonification".

```python
@app.route('/api/v1/workers', methods=['GET'])
```
A simple api call to get the content of worker table, returning a json containing every entry.

### `app/manage.py`
It enable some commands useful to handle our Flask app. In particular:
- `ready` --> checks if the database is ready to answer; when the Postgres containers starts, it takes time before it is really redy to answer a request, so better wait if you want to automate things
- `create_db` --> drop everything in the db and the create empty tables as defined with classes in SQLAlchemy notation
- `seed_db` --> populate db with some dummy data

### `app/mixin.py`
A simple Mixin to make SQLAlchemy query results serializable. It will be enough to inherit `Serializer` to be able to use `serialize` a single entry (sually the result of a Object.query.get(id)) or `serialize_list` the result of a bigger query (something like Object.query.all())

### `requirements.txt`
Python requirements for the project

### `run-local.sh`
A simple script to start our development environement.
In particular, 3 main phases:
- handle the environment (create, install dependencies)

- start a postgres container and wait for it to be ready to receive calls

- create tables, populate dummy data and start Flask server


## dockerizing the app

The next step is pretty straightforward, we dockerize the Flask app. In order to do that we simply add a new file into `app` folder named `Dockerfile` (https://docs.docker.com/engine/reference/builder) and we evolve the running script to a new version `run-dockered.sh`

### `Dockerfile`

Let's define the instruction set for our image.
```Dockerfile
FROM python:3.11-slim-bookworm
```
Starting image obviously will be a python image (Dockerhub to check the available tags and choose the appropriate one).

```Dockerfile
WORKDIR /usr/src/app
```
Setting the workdir in order to avoid working in the root directory. If the path does not exist, it will be created (https://docs.docker.com/engine/reference/builder/#workdir)

```Dockerfile
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
```
`ENV` instruction allow to set environment variables. In the specific case: `PYTHONDONTWRITEBYTECODE` will prevent python from writing bytecode and `PYTHONUNBUFFERED` will prevent python from buffering stdout and stderr.

```Dockerfile
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
```
`RUN` instruction will allow the execution of a command, while `COPY` will copy file(s) from local path to container. A very similar instruction would be `ADD` but since difference are very thin and specific a general rulo would be to preferr `COPY`.
This block will first upgrade `pip`, then copy `requirements.txt` to install dependecies.

```Dockerfile
COPY . .
```
Equivalent to `COPY . /usr/src/app` since a WORKDIR has been defined.
The whole content of local folder get copied inside the container. 

### `run-dockered.sh`
A simple script to run the dockered version.
In particular, 4 main phases:
- create a common network for the services

- start a postgres container and wait for it to be ready to receive calls

- build and start flask image/container

- create tables, populate dummy data


## using docker compose

The next step will be transitioning everything to a `docker-compose.yml` file.
Having already the docker run command for the service structure, the transition will be very smooth.
Staring from `run-dockered.sh` we know that we need a common network and 2 services.
Network won't be a problem, all services inside a docker-compose by default are isolated in the same default network.

For the services we need simply to translate the `docker run` command into the equivalent `docker compose` version.

In example the command:
```bash
docker container run -e "POSTGRES_USER=hello_flask" -e "POSTGRES_PASSWORD=hello_flask" -e "POSTGRES_DB=hello_flask_dev" --name="flask-pg-localrun" -p 5432:5432 --rm -d postgres:13

```
become a services in the `docker-compose.yml` file like this:
```yaml
  db:
    container_name: flask-pg-localrun
    image: postgres:13
    environment:
      - POSTGRES_USER=hello_flask
      - POSTGRES_PASSWORD=hello_flask
      - POSTGRES_DB=hello_flask_de
    ports:
      - 5432:5432
```

Instead of a simple translation we will made little adjustement. Specifically, we will remove `ports` since postgres doesn't need to be reachable from outside the default network of the compose file. Moreover we will create a volume to make postgres data permanent.

The best way to add a volume is to define a volume in the top-level elements `volumes` and then map it to a path internal to the container.
So, in the top-level `volumes` elements:
```yaml
volumes:
  db-data:
    name: flaskproject-pgslq-data
```
And then in the service definition we add:
```yaml
volumes:
      - flaskproject-pgslq-data:/var/lib/postgresql/data/   
```
The file `detailed.docker-compose.yml` is an extended version that include most of the possible elements and attribute that can be used inside a docker compose, with direct link to documentation.


## beyond docker compose

### `entrypoint.sh`

As stated also before one of the key point before we can declare our Flask app healty is DB readyness. We have created a call in manage.py but the most common way to address the issue is by using entrypoint feature of containers.
Entrypoint are literarly point of access to our container. If we specify an entrypoint it means that before starting our container will run the entrypoint, and each and every command of our app will be handled by the entrypoint (also the `CMD` or `command` in our `Dockerfile` or `docker-compose.yml`).

Typical entrypoint for python application with DB interaction will be:
```bash
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py create_db

exec "$@"
```

In details:

```bash
if [ "$DATABASE" = "postgres" ]
```
We will understand this in detail in the next section, but it moslty serve the purpose of distinguishing between development and production case. If we use a sqlite for development, the test we are going to do is meaningless.

```bash
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
```
If postgres is our database choice, then we need to wait until it is ready to answer us. To do so we use netcat and wait until postgres server answer before continuing.
NOTE that not all images have netcat preinstalled (very few of them in reality) hence we need also to take care of this aspect by adding something like the following to our `Dockerfile`:
```Dockerfile

RUN apt-get update && apt-get install -y netcat
```

Final part of entrypoint is very application specific, we start by ensuring that the database exists BUT in production environment that would not be the case. 
```bash
python manage.py create_db

exec "$@"
```
In a production environment we most likely collect statics or similar action that can be automated without any real risk.
`exec "$@"` will allow the execution of whatever command we pass to the application.
So we usually don't close the entrypoint with a "run the application" command, rather we leave the possibility to run it to subsequent commands.

## Environment variables

To better handling the whole project everything that may change between development and production, or between instances needs to be addressed with environment variables.
We won't commit an `.env` file, it will remain "gitignored", instead we will commit a `.env.template` and eventually write a script to intialize the environment.
Typical scripts make use of `pwgen` to create passwords where needed.
For now our script will simply copy `.env.template` into `.env`


## Prod compose using profiles

As from documentation (https://docs.docker.com/compose/profiles/) we can make great use of profiles.
We define two main profile `dev` and  `prod` and using yaml fragment feature (https://docs.docker.com/compose/compose-file/10-fragments/) we make so common part get shared between services.

We create two different services, one for prod and one for dev. The prod one will also use a differente `Dockerfile` taking advantage of multi-stage feature (https://docs.docker.com/build/building/multi-stage/)
