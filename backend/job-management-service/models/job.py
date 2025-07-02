from utils.database import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    reference_number = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cutoff_grade = db.Column(db.Numeric(5, 2))
    status = db.Column(db.Enum('draft', 'active', 'closed', name='job_status'), default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    min_qualification_criteria = db.relationship('MinQualificationCriteria', backref='job', lazy=True)
    formal_assessment_criteria = db.relationship('FormalAssessmentCriteria', backref='job', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entity_id': self.entity_id,
            'reference_number': self.reference_number,
            'title': self.title,
            'description': self.description,
            'cutoff_grade': float(self.cutoff_grade) if self.cutoff_grade else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'min_qualification_criteria_count': len(self.min_qualification_criteria),
            'formal_assessment_criteria_count': len(self.formal_assessment_criteria)
        }