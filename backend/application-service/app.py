from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utils.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS to handle preflight requests
    CORS(app)

    # Initialize database
    db.init_app(app)
    
    # Register blueprints

    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'application-management', 'port': 5003}
    
    @app.route('/')
    def home():
        return {'message': 'Application Management Service', 'version': '1.0.0'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003, debug=True)