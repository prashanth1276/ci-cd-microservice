import os


class Config:
    ENV = os.getenv("APP_ENV", "dev")
    DEBUG = ENV == "dev"