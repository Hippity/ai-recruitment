from datetime import datetime
from app import db

class MinQualificationResult(db.Model):
    __tablename__ = 'min_qualification_results'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    candidate_id = db.Column(db.String(100), nullable=False)
    criteria_id = db.Column(db.Integer, nullable=False)
    area = db.Column(db.String(255), nullable=False)
    result = db.Column(db.Enum('PASS', 'FAIL', name='min_qual_result'), nullable=False)
    justification = db.Column(db.Text, nullable=False)
    evidence_found = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'candidate_id': self.candidate_id,
            'criteria_id': self.criteria_id,
            'area': self.area,
            'result': self.result,
            'justification': self.justification,
            'evidence_found': self.evidence_found,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }