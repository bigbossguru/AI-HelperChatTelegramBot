import os
import openai

from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ["OPENAI_ORG"]
openai.api_key = os.environ["OPENAI_TOKEN"]
