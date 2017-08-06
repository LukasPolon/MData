from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from mdata import common

BASE = declarative_base()


class DbDriver(object):
    def __init__(self):
        pass

    def register_engine(self, poolclass=NullPool):
        """ Create database engine, and register it to metadata.

            Args:
                poolclass(sqlalchemy.pool): pool option

            Returns:
                engine(Engine): database engine, which
                        were created between database and client
        """
        engine = create_engine('{conn}{db}'.format(db=common.TEST_DATABASE,
                                                   conn=common.DB_CONNECTION),
                               poolclass=poolclass)
        BASE.metadata.bind = engine
        return engine

    def create_db_session(self, engine):
        """ Create session object, which will be used
            to execute transaction.

            Args:
                engine(Engine): database engine

            Returns:
                session(Session): database session object
        """
        dbsession = sessionmaker(bind=engine)
        session = dbsession()
        return session

    def close_db_session(self, session):
        """ Close current session, and return it to the pool.

            Args:
                session(Session): database session object
        """
        session.close()


def database_session(func):
    """ Decorator, which establishes the session,
        invokes the function, and closes session.

        Decorator is adapted for methods only.

        Passed function have to accept session object as argument.

        Args:
            func(callable): decorated function

        Returns:
            func_wrapper(function): inner decorator function
    """
    def func_wrapper(self, *args, **kwargs):
        db_driver = DbDriver()
        engine = db_driver.register_engine()
        session = db_driver.create_db_session(engine)

        kwargs.update({'session': session})
        result = func(self, *args, **kwargs)

        db_driver.close_db_session(session)
        return result
    return func_wrapper


