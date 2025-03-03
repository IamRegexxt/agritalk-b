import psycopg2
# for debugging purposes only to test its connection from postgresql to python
def test_connection():
    try:
        # Manually set the database URL
        db_url = "postgresql://postgres:iamthemaster@localhost:5432/agritalk"
        print(f"Connecting to database: {db_url}")  # Debugging output

        # Connect to the database
        conn = psycopg2.connect(db_url)

        # Create a cursor
        cur = conn.cursor()

        # Execute a simple query
        cur.execute('SELECT version();')

        # Fetch the result
        version = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        conn.close()

        print(f"Successfully connected to PostgreSQL: {version[0]}")
        return True

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False

if __name__ == "__main__":
    test_connection()
