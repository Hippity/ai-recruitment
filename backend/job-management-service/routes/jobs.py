from flask import Blueprint, request, jsonify
from models import Job, Entity
from utils.database import db

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/', methods=['GET'])
def get_jobs():
    entity_id = request.args.get('entity_id')
    status = request.args.get('status')
    
    query = Job.query
    
    if entity_id:
        query = query.filter_by(entity_id=entity_id)
    if status:
        query = query.filter_by(status=status)
    
    jobs = query.order_by(Job.created_at.desc()).all()
    return jsonify([job.to_dict() for job in jobs])

@jobs_bp.route('', methods=['POST'])
def create_job():
    data = request.get_json()
    
    required_fields = ['entity_id', 'reference_number', 'title', 'description']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if entity exists
    entity = Entity.query.get(data['entity_id'])
    if not entity:
        return jsonify({'error': 'Entity not found'}), 404
    
    # Check if reference number is unique
    existing_job = Job.query.filter_by(reference_number=data['reference_number']).first()
    if existing_job:
        return jsonify({'error': 'Reference number already exists'}), 400
    
    job = Job(
        entity_id=data['entity_id'],
        reference_number=data['reference_number'],
        title=data['title'],
        description=data['description'],
        cutoff_grade=data.get('cutoff_grade'),
        status=data.get('status', 'draft')
    )
    
    try:
        db.session.add(job)
        db.session.commit()
        return jsonify(job.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create job'}), 500

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        job.title = data['title']
    if 'description' in data:
        job.description = data['description']
    if 'cutoff_grade' in data:
        job.cutoff_grade = data['cutoff_grade']
    if 'status' in data:
        if data['status'] not in ['draft', 'active', 'closed']:
            return jsonify({'error': 'Invalid status'}), 400
        job.status = data['status']
    
    try:
        db.session.commit()
        return jsonify(job.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update job'}), 500

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete job'}), 500

@jobs_bp.route('/<int:job_id>/criteria', methods=['GET'])
def get_job_criteria(job_id):
    job = Job.query.get_or_404(job_id)
    
    min_qual_criteria = sorted(job.min_qualification_criteria, key=lambda x: x.order_index)
    formal_criteria = sorted(job.formal_assessment_criteria, key=lambda x: x.order_index)
    
    return jsonify({
        'job_id': job_id,
        'min_qualification_criteria': [criteria.to_dict() for criteria in min_qual_criteria],
        'formal_assessment_criteria': [criteria.to_dict() for criteria in formal_criteria]
    })