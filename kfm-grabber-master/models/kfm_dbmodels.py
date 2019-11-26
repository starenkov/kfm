from app.creds import DB
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, Text, text, Table, JSON, String
from sqlalchemy.ext.declarative import declarative_base

logicsession = create_engine('postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{sessionname}'.format(
    user=DB.Cortigiana.user,
    passwd=DB.Cortigiana.password,
    host=DB.Cortigiana.host,
    port=DB.Cortigiana.port,
    sessionname=DB.Cortigiana.sessionname
), echo=False)

Base = declarative_base()
metadata = Base.metadata
metadata.bind = logicsession


logicsession_session = sessionmaker(bind=logicsession)
session = logicsession_session()


class KfmOrganisations(Base):
    __tablename__ = 'kfm_organisations'
    __table_args__ = {'schema': 'cortigiana'}

    id = Column(Integer, primary_key=True,)
                # server_default=text("nextval('cortigiana.kfm_organisations_id_seq'::regclass)"))
    num = Column(Text)
    org_name = Column(Text)
    note = Column(Text)


class KfmOrganisationscis(Base):
    __tablename__ = 'kfm_organisationscis'
    __table_args__ = {'schema': 'cortigiana'}

    id = Column(Integer, primary_key=True,)
                # server_default=text("nextval('cortigiana.kfm_organisationscis_id_seq'::regclass)"))
    num = Column(Text)
    org_name = Column(Text)
    org_name_en = Column(Text)
    note = Column(Text)


class KfmUnIndividuals(Base):
    __tablename__ = 'kfm_un_individuals'
    __table_args__ = {'schema': 'cortigiana'}

    id = Column(Integer, primary_key=True,)
                # server_default=text("nextval('cortigiana.kfm_un_individuals_id_seq'::regclass)"))
    dataid = Column(Text)
    versionnum = Column(Text)
    first_name = Column(Text, nullable=True)
    second_name = Column(Text, nullable=True)
    third_name = Column(Text, nullable=True)
    fourth_name = Column(Text, nullable=True)
    un_list_type = Column(Text, nullable=True)
    reference_number = Column(Text, nullable=True)
    comments1 = Column(Text, nullable=True)
    designation = Column(Text, nullable=True)
    nationality = Column(Text, nullable=True)
    listed_on = Column(Text, nullable=True)
    list_type = Column(Text, nullable=True)
    last_day_updated = Column(Text, nullable=True)
    individual_alias = Column(Text, nullable=True)
    individual_address = Column(Text, nullable=True)
    individual_date_of_birth = Column(Text, nullable=True)
    individual_place_of_birth = Column(Text, nullable=True)
    individual_document = Column(Text, nullable=True)


class KfmUnEntities(Base):
    __tablename__ = 'kfm_un_entities'
    __table_args__ = {'schema': 'cortigiana'}

    id = Column(Integer, primary_key=True,)
                # server_default=text("nextval('cortigiana.kfm_un_entities_id_seq'::regclass)"))
    dataid = Column(Text)
    versionnum = Column(Text)
    first_name = Column(Text, nullable=True)
    un_list_type = Column(Text, nullable=True)
    reference_number = Column(Text, nullable=True)
    listed_on = Column(Text, nullable=True)
    name_original_script = Column(Text, nullable=True)
    comments1 = Column(Text, nullable=True)
    list_type = Column(Text, nullable=True)
    last_day_updated = Column(Text, nullable=True)
    entity_alias = Column(Text, nullable=True)
    entity_address = Column(Text, nullable=True)


class KfmPersons(Base):
    __tablename__ = 'kfm_persons'
    __table_args__ = {'schema': 'cortigiana'}

    id = Column(Integer, primary_key=True,) # server_default=text("nextval('cortigiana.kfm_persons_id_seq'::regclass)"))
    num = Column(Text)
    lname = Column(Text)
    fname = Column(Text)
    mname = Column(Text)
    birthdate = Column(Date)
    iin = Column(Text)
    note = Column(Text)
    correction = Column(Text)


t_kfm_relevance = Table(
    'kfm_relevance', metadata,
    Column('id', Integer, primary_key=True,),
           # server_default=text("nextval('cortigiana.kfm_relevance_id_seq'::regclass)")),
    Column('persons', DateTime),
    Column('organisations', DateTime),
    Column('organisationscis', DateTime),
    Column('un_individuals', DateTime),
    Column('un_entities', DateTime),
    schema='cortigiana'

)


class KfmRelevance(Base):
    __table__ = t_kfm_relevance


t_kfm_history = Table(
    'kfm_history', metadata,
    Column('id', Integer, primary_key=True,), #server_default=text("nextval('cortigiana.kfm_history_id_seq'::regclass)")),
    Column('item', JSON),
    Column('item_type', String(1024)),
    Column('action_type', String(1024)),
    Column('action_date', DateTime),
    Column('descr', String(4094)),
    schema='cortigiana'
)


class KfmHistory(Base):
    __table__ = t_kfm_history
