from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

engine = create_engine("sqlite:///debates.db", connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
# edwd