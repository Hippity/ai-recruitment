from flask import Blueprint, request, jsonify
from models import Job, MinQualificationCriteria, FormalAssessmentCriteria
from utils.database import db

criteria_bp = Blueprint('criteria', __name__)

# MINIMUM QUALIFICATION CRITERIA ROUTES
@criteria_bp.route('/min-qualification', methods=['POST'])
def create_min_qualification_criteria():
    data = request.get_json()
    
    required_fields = ['job_id', 'area', 'criteria']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job = Job.query.get(data['job_id'])
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    max_order = db.session.query(db.func.max(MinQualificationCriteria.order_index))\
                          .filter_by(job_id=data['job_id']).scalar() or 0
    
    criteria = MinQualificationCriteria(
        job_id=data['job_id'],
        area=data['area'],
        criteria=data['criteria'],
        explanation=data.get('explanation'),
        order_index=data.get('order_index', max_order + 1)
    )
    
    try:
        db.session.add(criteria)
        db.session.commit()
        return jsonify(criteria.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create criteria'}), 500

@criteria_bp.route('/min-qualification/<int:criteria_id>', methods=['PUT'])
def update_min_qualification_criteria(criteria_id):
    criteria = MinQualificationCriteria.query.get_or_404(criteria_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'area' in data:
        criteria.area = data['area']
    if 'criteria' in data:
        criteria.criteria = data['criteria']
    if 'explanation' in data:
        criteria.explanation = data['explanation']
    if 'order_index' in data:
        criteria.order_index = data['order_index']
    
    try:
        db.session.commit()
        return jsonify(criteria.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update criteria'}), 500

@criteria_bp.route('/min-qualification/<int:criteria_id>', methods=['DELETE'])
def delete_min_qualification_criteria(criteria_id):
    criteria = MinQualificationCriteria.query.get_or_404(criteria_id)
    
    try:
        db.session.delete(criteria)
        db.session.commit()
        return jsonify({'message': 'Criteria deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete criteria'}), 500

# FORMAL ASSESSMENT CRITERIA ROUTES
@criteria_bp.route('/formal-assessment', methods=['POST'])
def create_formal_assessment_criteria():
    data = request.get_json()
    
    required_fields = ['job_id', 'area', 'criteria']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job = Job.query.get(data['job_id'])
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    max_order = db.session.query(db.func.max(FormalAssessmentCriteria.order_index))\
                          .filter_by(job_id=data['job_id']).scalar() or 0
    
    criteria = FormalAssessmentCriteria(
        job_id=data['job_id'],
        area=data['area'],
        criteria=data['criteria'],
        explanation=data.get('explanation'),
        max_score=data.get('max_score', 10.00),
        weight=data.get('weight', 1.00),
        order_index=data.get('order_index', max_order + 1)
    )
    
    try:
        db.session.add(criteria)
        db.session.commit()
        return jsonify(criteria.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create criteria'}), 500

@criteria_bp.route('/formal-assessment/<int:criteria_id>', methods=['PUT'])
def update_formal_assessment_criteria(criteria_id):
    criteria = FormalAssessmentCriteria.query.get_or_404(criteria_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'area' in data:
        criteria.area = data['area']
    if 'criteria' in data:
        criteria.criteria = data['criteria']
    if 'explanation' in data:
        criteria.explanation = data['explanation']
    if 'max_score' in data:
        criteria.max_score = data['max_score']
    if 'weight' in data:
        criteria.weight = data['weight']
    if 'order_index' in data:
        criteria.order_index = data['order_index']
    
    try:
        db.session.commit()
        return jsonify(criteria.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update criteria'}), 500

@criteria_bp.route('/formal-assessment/<int:criteria_id>', methods=['DELETE'])
def delete_formal_assessment_criteria(criteria_id):
    criteria = FormalAssessmentCriteria.query.get_or_404(criteria_id)
    
    try:
        db.session.delete(criteria)
        db.session.commit()
        return jsonify({'message': 'Criteria deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete criteria'}), 500

# BULK OPERATIONS
@criteria_bp.route('/min-qualification/bulk', methods=['POST'])
def create_bulk_min_qualification_criteria():
    data = request.get_json()
    
    if not data or 'job_id' not in data or 'criteria_list' not in data:
        return jsonify({'error': 'Missing job_id or criteria_list'}), 400
    
    job_id = data['job_id']
    criteria_list = data['criteria_list']
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    created_criteria = []
    
    try:
        for index, criteria_data in enumerate(criteria_list):
            if not all(field in criteria_data for field in ['area', 'criteria']):
                return jsonify({'error': f'Missing required fields in criteria {index}'}), 400
            
            criteria = MinQualificationCriteria(
                job_id=job_id,
                area=criteria_data['area'],
                criteria=criteria_data['criteria'],
                explanation=criteria_data.get('explanation'),
                order_index=criteria_data.get('order_index', index + 1)
            )
            
            db.session.add(criteria)
            created_criteria.append(criteria)
        
        db.session.commit()
        return jsonify([criteria.to_dict() for criteria in created_criteria]), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create bulk criteria'}), 500

@criteria_bp.route('/formal-assessment/bulk', methods=['POST'])
def create_bulk_formal_assessment_criteria():
    data = request.get_json()
    
    if not data or 'job_id' not in data or 'criteria_list' not in data:
        return jsonify({'error': 'Missing job_id or criteria_list'}), 400
    
    job_id = data['job_id']
    criteria_list = data['criteria_list']
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    created_criteria = []
    
    try:
        for index, criteria_data in enumerate(criteria_list):
            if not all(field in criteria_data for field in ['area', 'criteria']):
                return jsonify({'error': f'Missing required fields in criteria {index}'}), 400
            
            criteria = FormalAssessmentCriteria(
                job_id=job_id,
                area=criteria_data['area'],
                criteria=criteria_data['criteria'],
                explanation=criteria_data.get('explanation'),
                max_score=criteria_data.get('max_score', 10.00),
                weight=criteria_data.get('weight', 1.00),
                order_index=criteria_data.get('order_index', index + 1)
            )
            
            db.session.add(criteria)
            created_criteria.append(criteria)
        
        db.session.commit()
        return jsonify([criteria.to_dict() for criteria in created_criteria]), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create bulk criteria'}), 500