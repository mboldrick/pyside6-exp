from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Enum('individual', 'company', name='person_type'))
    company_name = Column(String, nullable=True)
    email = Column(String)
    phone = Column(String)

    projects = relationship("Project", back_populates="client")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(Date)
    legacy_client_id = Column(Integer)
    client_id = Column(Integer, ForeignKey('people.id'))

    client = relationship("People", back_populates="projects")

engine = create_engine('sqlite:///invoice3001.db')
Base.metadata.create_all(engine)
