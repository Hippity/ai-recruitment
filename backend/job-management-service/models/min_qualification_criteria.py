from utils.database import db
from datetime import datetime

class MinQualificationCriteria(db.Model):
    __tablename__ = 'min_qualification_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    criteria = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'area': self.area,
            'criteria': self.criteria,
            'explanation': self.explanation,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }