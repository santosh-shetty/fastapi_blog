from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update this connection string with your MySQL credentials
DATABASE_URL = "mysql+pymysql://root:@localhost/fastapi_blog"

# Create an instance of the engine using pymysql
engine = create_engine(DATABASE_URL)

# Set up Base and SessionLocal
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
