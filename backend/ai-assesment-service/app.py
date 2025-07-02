
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes import min_qualification_bp, formal_assessment_bp
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(min_qualification_bp, url_prefix='/api/min-qualification')
    app.register_blueprint(formal_assessment_bp, url_prefix='/api/formal-assessment')
    
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ai-assessment', 'port': 5004}
    
    @app.route('/')
    def home():
        return {
            'message': 'AI Assessment Service',
            'version': '1.0.0',
            'endpoints': {
                'min_qualification': '/api/min-qualification/*',
                'formal_assessment': '/api/formal-assessment/*',
                'health': '/health'
            }
        }
    
    return app

if __name__ == '__main__':
    if not Config.OPENAI_API_KEY:
        print("OPENAI_API_KEY environment variable is required!")
        exit(1)
    
    app = create_app()
    app.run(host='0.0.0.0', port=5004, debug=True)