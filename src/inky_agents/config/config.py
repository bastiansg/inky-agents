from pydantic import StrictStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_dsn: StrictStr = "mongodb://inky-agents-mongo:27017"
    mongodb_db_name: StrictStr = "llm_agents"
    mongodb_collection: StrictStr = "message_history"


config = Config()
