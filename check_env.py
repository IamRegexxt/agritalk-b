import os
from dotenv import load_dotenv

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Check key environment variables
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
print(f"JWT_SECRET_KEY: {os.environ.get('JWT_SECRET_KEY')}") 