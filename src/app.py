import os
import click
import sqlalchemy as sa
from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str]=mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"

#representação de user
class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String,unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int]=mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates='user') # aqui terminamos nosso mapeamento

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"

#representação de post (com nome, titulo e corpo do post, e também com id do author)
class Post(db.Model): # devemos lembrar de extender a classe pelo db-model, pq se não ela não sobe no bd
    id: Mapped[str] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str]=mapped_column(sa.String, nullable=False)
    body: Mapped[str]=mapped_column(sa.String, nullable=False)
    created:Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id:Mapped[int] = mapped_column(sa.ForeignKey("user.id")) # chave extrangeira, 
    # usamos o sa.foreignkey("nome_da_tabela") pra poder referenciar o nome da tabela 
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})" 
    # esta função acima serve para nos retornar um print com estas informações,posso chamar isso de
    # mascara ? provavelmente sim

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= "dev",
        SQLALCHEMY_DATABASE_URI= os.environ["DATABASE_URL"],
        JWT_SECRET_KEY= "top-secret",
    )
    migrate = Migrate(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instances folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # register cli commands
    app.cli.add_command(init_db_command)

    # initalizing extensions 
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #register blueprint
    from src.controllers import user, auth, role

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)


    return app