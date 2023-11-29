# Base Docker and Compose Project
## Development History details

Let's say you follow me in the development of this repo. I will explain step that led me to the final version of this app.

First of all I want to develop a Flask app. Hence, I will use a virtualenv with the required dependencies and some file for a better handling of Flask project.

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

#### `app` folder
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



