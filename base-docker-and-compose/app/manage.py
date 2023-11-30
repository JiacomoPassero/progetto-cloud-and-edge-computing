from flask.cli import FlaskGroup

from sqlalchemy import text

from app import app, db, Worker


cli = FlaskGroup(app)

@cli.command("ready")
def test():
    while True:
        try:
            db.session.execute(text('SELECT 1'))
            print('\n\n----------- Connection successful !')
            break
        except Exception as e:
            ...


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Worker(email="adminuser@example.com", fullname="User Admin"))
    db.session.commit()


if __name__ == "__main__":
    cli()