
from dotenv import find_dotenv, load_dotenv
import os
path = find_dotenv()
print(" dotenv found at:", path)
load_dotenv(path, override=True)
print(" GITHUB_TOKENS is now:", os.getenv("GITHUB_TOKENS"))