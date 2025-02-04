
import click

from app import app
from models import User, db


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User(username='bob', email='bob@mail.com', password='bobpass')
  db.session.add(bob)
  db.session.commit()
  print(f'Initialized database with {bob}')
  #print('Database initialized')

@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command('create-user')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_user(username, email, password):
    newuser = User(username=username, email=email, password=password)  # Use keyword arguments
    try:
        db.session.add(newuser)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Undo any previous transaction steps
        print("Username or email already taken!")  # Show user-friendly error message
    else:
        print(newuser)  # Print the newly created user
