import pg8000
from dotenv import load_dotenv
import os
import sys

def create_database():
    # Load environment variables
    load_dotenv()

    # Get database URL and modify it to connect to postgres database
    db_url = os.getenv('DATABASE_URL', '')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        sys.exit(1)

    # Parse the DATABASE_URL to extract connection parameters
    # Format: postgresql://username:password@host:port/database
    try:
        # Remove postgresql:// prefix
        url_part = db_url.replace('postgresql://', '')
        
        # Split into credentials and host/database
        if '@' in url_part:
            credentials, host_db = url_part.split('@', 1)
            username, password = credentials.split(':', 1)
        else:
            username, password = '', ''
            host_db = url_part
        
        # Split host and database
        if '/' in host_db:
            host_port, database = host_db.rsplit('/', 1)
        else:
            host_port = host_db
            database = 'postgres'
        
        # Split host and port
        if ':' in host_port:
            host, port = host_port.split(':', 1)
            port = int(port)
        else:
            host = host_port
            port = 5432
        
        print(f"Attempting to connect to PostgreSQL server at {host}:{port}...")
        
        # Connect to postgres database (not consent_db)
        conn = pg8000.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database='postgres'
        )
        
        cursor = conn.cursor()

        # Check if database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'consent_db'")
        exists = cursor.fetchone()
        
        if exists:
            print("Database 'consent_db' already exists!")
        else:
            # Create the database
            cursor.execute('CREATE DATABASE consent_db')
            print("Database 'consent_db' created successfully!")

    except pg8000.OperationalError as e:
        print(f"Error connecting to database: {e}")
        print("\nPlease check:")
        print("1. Your database credentials in .env file")
        print("2. If the database server is running")
        print("3. If your IP is allowed to connect to the database")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_database() 