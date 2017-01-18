from __future__ import print_function


import os


import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm.exc import NoResultFound
import yaml


import smashdb.models as models


# UTILITY

def get_url(role=None):
    if role is None:
        role = os.environ['SMASHDB_ROLE']
    home = os.path.expanduser('~')
    config_file_name = os.path.join(home, ".smashdb", "config.yml")
    with open(config_file_name, 'r') as stream:
        parameters = yaml.load(stream)[role]
    url = r'mysql+mysqldb://{}:{}@{}'.format(
            parameters['USERNAME'],
            parameters['PASSWORD'],
            parameters['HOST'])
    return url


def make_session(role, echo=False):
    url = get_url(role)
    engine = sa.create_engine(url, echo=echo)
    return orm.sessionmaker(bind=engine)()


def get_or_create(session, model, get_params, create_params=None):
    """Get a or create an instance in the database.
    Args:
        session:
        model: Class of the object to create.
        get_params (dict): parameters needed to uniquely identify an already
            existing entity.
        create_params (dict): Additional parameters needed if the entity does
            not already exist and has to be created

    Returns:
        an ORM object representing the instance.
        (bool): True if the instance was created, False if it already existed.
    """
    if create_params is None:
        create_params = {}
    try:
        instance = session.query(model).filter_by(**get_params).one()
    except NoResultFound:
        instance = None
    if instance:
        created = False
    else:
        all_params = dict(get_params.items() + create_params.items())
        instance = model(**all_params)
        session.add(instance)
        created = True
    return instance, created

