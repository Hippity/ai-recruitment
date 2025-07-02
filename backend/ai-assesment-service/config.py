import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL') or 'gpt-4-turbo-preview'
    OPENAI_MAX_TOKENS = int(os.environ.get('OPENAI_MAX_TOKENS', '2000'))
    OPENAI_TEMPERATURE = float(os.environ.get('OPENAI_TEMPERATURE', '0.3'))
    
    # Job Management Service Configuration
    JOB_MANAGEMENT_SERVICE_URL = os.environ.get('JOB_MANAGEMENT_SERVICE_URL') or 'http://localhost:5003'
    
    # Usage Tracking
    TRACK_USAGE = os.environ.get('TRACK_USAGE', 'true').lower() == 'true'
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.environ.get('RATE_LIMIT_REQUESTS_PER_MINUTE', '100'))
    
    # Database for usage tracking
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///ai_assessment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False