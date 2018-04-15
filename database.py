from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import SQL_PARAMS

engine = create_engine(SQL_PARAMS, convert_unicode=True, echo=False, pool_recycle=3600)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
