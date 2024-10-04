from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BotRouter.app.data import config
from models import Base

DATABASE_URL = f"postgresql://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_tables():
    """
    Function to create all tables in the database using the models defined.
    """
    print("Creating all tables...")
    # Create all tables based on Base metadata
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")


create_all_tables()
