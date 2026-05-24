import urllib.parse

# Database Configurations
escaped_password = urllib.parse.quote_plus("tarun@123")
DATABASE_URL = f"mysql+pymysql://root:{escaped_password}@localhost/fastapi"

# JWT Security Configurations
SECRET_KEY = "super-secret-dev-key-keep-it-safe-in-prod-environments"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
