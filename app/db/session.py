from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # pode mudar depois

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # só pro SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)