from fastapi import FastAPI, BackgroundTasks
from api.endpoints import router as api_router
import openai
import configparser

config = configparser.ConfigParser()
config.read('api.cfg')
openai.api_key = config.get('openai', 'api_key')

app = FastAPI(
    title="Dynamic Document Generation",
    version="0.1.0",
)

app.include_router(api_router)