from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utils.database import db
from routes import entities_bp, jobs_bp, criteria_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for direct frontend access
    CORS(app) 
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(entities_bp, url_prefix='/api/entities')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(criteria_bp, url_prefix='/api/criteria')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'job-management', 'port': 5003}
    
    @app.route('/')
    def home():
        return {'message': 'Job Management Service', 'version': '1.0.0'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003, debug=True)