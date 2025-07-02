from datetime import datetime
from app import db

class UsageTracking(db.Model):
    __tablename__ = 'usage_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)
    candidate_id = db.Column(db.String(100))
    
    prompt_tokens = db.Column(db.Integer, default=0)
    completion_tokens = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    
    model_used = db.Column(db.String(50))
    estimated_cost = db.Column(db.Numeric(10, 6), default=0.0)
    processing_time_ms = db.Column(db.Integer)
    success = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    @classmethod
    def log_usage(cls, job_id, assessment_type, usage_data, success=True, 
                  candidate_id=None, processing_time_ms=None):
        try:
            record = cls(
                job_id=job_id,
                assessment_type=assessment_type,
                candidate_id=candidate_id,
                prompt_tokens=usage_data.get('prompt_tokens', 0),
                completion_tokens=usage_data.get('completion_tokens', 0),
                total_tokens=usage_data.get('total_tokens', 0),
                model_used=usage_data.get('model'),
                estimated_cost=cls._calculate_cost(usage_data),
                processing_time_ms=processing_time_ms,
                success=success
            )
            
            db.session.add(record)
            db.session.commit()
            return record
        except:
            db.session.rollback()
            return None
    
    @classmethod
    def _calculate_cost(cls, usage_data):
        model = usage_data.get('model', '')
        prompt_tokens = usage_data.get('prompt_tokens', 0)
        completion_tokens = usage_data.get('completion_tokens', 0)
        
        if 'gpt-4-turbo' in model.lower():
            prompt_rate, completion_rate = 0.01, 0.03
        elif 'gpt-4' in model.lower():
            prompt_rate, completion_rate = 0.03, 0.06
        elif 'gpt-3.5-turbo' in model.lower():
            prompt_rate, completion_rate = 0.0015, 0.002
        else:
            prompt_rate, completion_rate = 0.03, 0.06
        
        return (prompt_tokens / 1000) * prompt_rate + (completion_tokens / 1000) * completion_rate
    
    @classmethod
    def get_stats(cls, job_id=None):
        query = cls.query.filter_by(job_id=job_id) if job_id else cls.query
        records = query.all()
        
        if not records:
            return {'total_assessments': 0, 'total_tokens': 0, 'total_cost': 0.0}
        
        return {
            'total_assessments': len(records),
            'successful_assessments': sum(1 for r in records if r.success),
            'total_tokens': sum(r.total_tokens for r in records),
            'total_cost': round(sum(float(r.estimated_cost or 0) for r in records), 4)
        }