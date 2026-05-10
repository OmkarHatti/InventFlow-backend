from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection URL
DATABASE_URL = "mysql+pymysql://root:OmkarHatti@127.0.0.1/fastapi"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(bind=engine)