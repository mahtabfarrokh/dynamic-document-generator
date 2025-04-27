from fastapi import FastAPI
from api.endpoints import router as api_router
import configparser
import os


config = configparser.ConfigParser()
config.read('api.cfg')
os.environ["OPENAI_API_KEY"] = config['openai']['api_key']

app = FastAPI(
    title="Dynamic Document Generation",
    version="0.1.0",
)

app.include_router(api_router)