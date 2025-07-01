import psycopg2
from dotenv import load_dotenv
import os

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    db_url = os.getenv('DATABASE_URL', '')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return

    print("Attempting to connect to database...")
    print(f"Host: my-cms-aurora-cluster.cvcwu2qwyxf6.eu-north-1.rds.amazonaws.com")
    print(f"Database: consent_db")
    print(f"User: db_master")
    
    try:
        # Try to connect
        conn = psycopg2.connect(
            host="my-cms-aurora-cluster.cvcwu2qwyxf6.eu-north-1.rds.amazonaws.com",
            database="consent_db",
            user="db_master",
            password="7995437205Th"
        )
        
        # If connection successful, print database info
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print("\nConnection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Check if we can access the database
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()
        print(f"Connected to database: {db_name[0]}")
        
        # Check user permissions
        cur.execute("SELECT current_user;")
        user = cur.fetchone()
        print(f"Connected as user: {user[0]}")
        
        cur.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print("\nConnection failed!")
        print(f"Error: {e}")
        print("\nPossible issues:")
        print("1. Security group not properly configured")
        print("2. Database credentials incorrect")
        print("3. Database server not accessible")
        print("4. Network connectivity issues")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    test_connection() 