from utils.database import db
from datetime import datetime

class FormalAssessmentCriteria(db.Model):
    __tablename__ = 'formal_assessment_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    max_score = db.Column(db.Numeric(5, 2), default=10.00)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'area': self.area,
            'criteria': self.criteria,
            'explanation': self.explanation,
            'max_score': float(self.max_score) if self.max_score else None,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }