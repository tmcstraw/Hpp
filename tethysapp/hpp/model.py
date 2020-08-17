import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from .model import *


Base = declarative_base()
# Base2 = declarative_base()


# SQLAlchemy ORM definition for the dams table
class Criteria(Base):
    """
    SQLAlchemy Dam DB Model
    """
    __tablename__ = 'criteria'

    # Columns
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    criteria_name = Column(String)
    field_name = Column(String)
    agg_method = Column(String)
    risk_scores = Column(String)
    criteria_type = Column(String)
    num_classes = Column(String)
    min_1 = Column(Float)
    max_1 = Column(Float)
    risk_score_1 = Column(Integer)
    min_2 = Column(Float)
    max_2 = Column(Float)
    risk_score_2 = Column(Integer)
    min_3 = Column(Float)
    max_3 = Column(Float)
    risk_score_3 = Column(Integer)
    min_4 = Column(Float)
    max_4 = Column(Float)
    risk_score_4 = Column(Integer)
    min_5 = Column(Float)
    max_5 = Column(Float)
    risk_score_5 = Column(Integer)
    criteria_weight = Column(Float)
    tot_criteria_score = Column(Float)

class Zoneclass(Base):

    __tablename__ = 'zone_class'

    # Columns
    risk_analysis_name = Column(String, primary_key=True)
    row1col1 = Column(String)
    row1col2 = Column(String)
    row1col3 = Column(String)
    row1col4 = Column(String)
    row1col5 = Column(String)
    row2col1 = Column(String)
    row2col2 = Column(String)
    row2col3 = Column(String)
    row2col4 = Column(String)
    row2col5 = Column(String)
    row3col1 = Column(String)
    row3col2 = Column(String)
    row3col3 = Column(String)
    row3col4 = Column(String)
    row3col5 = Column(String)
    row4col1 = Column(String)
    row4col2 = Column(String)
    row4col3 = Column(String)
    row4col4 = Column(String)
    row4col5 = Column(String)
    row5col1 = Column(String)
    row5col2 = Column(String)
    row5col3 = Column(String)
    row5col4 = Column(String)
    row5col5 = Column(String)

def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """

    # Create all the tables
    Base.metadata.create_all(engine)
    # Base2.metadata.create_all(engine)
    if first_time:
    # Add data

        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize database with two dams

        # Add the dams to the session, commit, and close

        session.close()

def init_zone_db(engine, first_time):
    """
    Initializer for the primary database.
    """

    # Create all the tables
    Base2.metadata.create_all(engine)
    if first_time:
    # Add data

        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize database with two dams

        # Add the dams to the session, commit, and close

        session.close()