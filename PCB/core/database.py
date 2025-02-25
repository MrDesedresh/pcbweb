import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

Base = declarative_base()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    socket = Column(String, nullable=True)
    memory_type = Column(String, nullable=True)
    power = Column(Float, nullable=True)
    price = Column(Float)

    def __repr__(self):
        return f"<Component(id={self.id}, type='{self.type}', name='{self.name}', manufacturer='{self.manufacturer}', model='{self.model}')>"


class DatabaseManager:
    def __init__(self, db_url=None):
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "sqlite:///./components.db")
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logging.info("DatabaseManager initialized")

    def get_session(self):
        return self.Session()

    def load_components_from_csv(self, csv_path):
        session = self.get_session()
        try:
            logging.info(f"Loading components from CSV: {csv_path}")
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                component = Component(**row.to_dict())
                session.add(component)
            session.commit()
            logging.info("Components loaded successfully")
        except Exception as e:
            session.rollback()
            logging.error(f"Error loading components from CSV: {e}", exc_info=True)
        finally:
            session.close()

    def get_components(self, component_type=None, search_term=None, manufacturer=None):
        session = self.get_session()
        try:
            logging.info(
                f"Fetching components. Type: {component_type}, Search term: {search_term}, Manufacturer: {manufacturer}")
            query = session.query(Component)
            if component_type:
                query = query.filter(Component.type == component_type)
            if search_term:
                query = query.filter(Component.name.contains(search_term) | Component.model.contains(search_term))
            if manufacturer:
                query = query.filter(Component.manufacturer == manufacturer)
            components = query.all()
            logging.info(f"Found {len(components)} components")
            return components
        except Exception as e:
            logging.error(f"Error fetching components from database: {e}", exc_info=True)
            return []
        finally:
            session.close()

    def get_component_by_id(self, component_id):
        session = self.get_session()
        try:
            logging.info(f"Fetching component by ID: {component_id}")
            component = session.query(Component).filter(Component.id == component_id).first()
            if component:
                logging.info(f"Found component: {component}")
            else:
                logging.warning(f"Component with id {component_id} not found")
            return component
        except Exception as e:
            logging.error(f"Error fetching component by ID {component_id}: {e}", exc_info=True)
            return None
        finally:
            session.close()