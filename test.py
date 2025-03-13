import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("CREDENTIALS_FILE","no encontrado"))