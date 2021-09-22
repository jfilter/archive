from __future__ import with_statement
import os, sys
sys.path.append(os.getcwd())
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from app import app
from app.models import db

# This is the 'Generic' alembic modified with some settings
# specific to this app

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Overwrite the sqlalchemy.url in the alembic.ini file.
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.metadata