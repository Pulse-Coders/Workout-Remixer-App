import os
from dotenv import load_dotenv
from sqlmodel import create_engine, text

# Load .env from the current directory (project root)
load_dotenv()

# Use the correct variable name from your .env
DATABASE_URL = os.getenv("DATABASE_URI")
if not DATABASE_URL:
    raise Exception("DATABASE_URI not found in .env file")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Check if image_url column already exists (SQLite version)
    result = conn.execute(text("PRAGMA table_info(workout)"))
    columns = [row[1] for row in result]
    if "image_url" not in columns:
        conn.execute(text("ALTER TABLE workout ADD COLUMN image_url TEXT"))
        conn.commit()
        print("Added image_url column to workout table")
    else:
        print("image_url column already exists")