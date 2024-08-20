import os
import dotenv
from sqlalchemy import create_engine, text

def database_connection_url():
    dotenv.load_dotenv()
    
    # Neon connection string format
    db_url = os.environ.get("NEON_DATABASE_URL")
    if not db_url:
        raise ValueError("NEON_DATABASE_URL environment variable is not set")
    
    return db_url



engine = create_engine(database_connection_url(), pool_pre_ping=True)

# Test the connection
with engine.connect() as connection:
    try:
        result = connection.execute(text("SELECT * FROM documents"))
        print("Connected successfully!")
        print("Columns in 'documents' table:", result.keys())
        for row in result:
            print(row)
    except Exception as e:
        print(f"An error occurred: {e}")
        # If the 'documents' table doesn't exist, try a simple SELECT
        result = connection.execute(text("SELECT 1"))
        print("Connected successfully, but 'documents' table might not exist.")