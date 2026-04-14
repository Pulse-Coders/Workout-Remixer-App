import os
from dotenv import load_dotenv
from sqlmodel import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URI")
if not DATABASE_URL:
    raise Exception("DATABASE_URI not found")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = [row[0] for row in result]
    print("Tables in database:", tables)