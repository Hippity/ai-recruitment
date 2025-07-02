from datetime import datetime
from app import db

class FormalAssessmentResult(db.Model):
    __tablename__ = 'formal_assessment_results'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    candidate_id = db.Column(db.String(100), nullable=False)
    criteria_id = db.Column(db.Integer, nullable=False)
    area = db.Column(db.String(255), nullable=False)
    raw_score = db.Column(db.Numeric(5, 2), nullable=False)
    max_score = db.Column(db.Numeric(5, 2), nullable=False)
    percentage = db.Column(db.Numeric(5, 2), nullable=False)
    evidence = db.Column(db.Text, nullable=False)
    justification = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'candidate_id': self.candidate_id,
            'criteria_id': self.criteria_id,
            'area': self.area,
            'raw_score': float(self.raw_score) if self.raw_score else None,
            'max_score': float(self.max_score) if self.max_score else None,
            'percentage': float(self.percentage) if self.percentage else None,
            'evidence': self.evidence,
            'justification': self.justification,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }