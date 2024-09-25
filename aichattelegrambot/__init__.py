import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_TOKEN")
