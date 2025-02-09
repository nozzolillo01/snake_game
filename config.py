import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'game.db'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # In production, SECRET_KEY should be set in environment variables
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = 'test_game.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}