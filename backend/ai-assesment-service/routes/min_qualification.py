from flask import Blueprint, request, jsonify
from services.assessment_processor import AssessmentProcessor

min_qualification_bp = Blueprint('min_qualification', __name__)

@min_qualification_bp.route('/assess', methods=['POST'])
def assess_min_qualification():
    """
    Assess a candidate against minimum qualification criteria
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_id', 'candidate_id', 'candidate_data']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: job_id, candidate_id, candidate_data'
            }), 400
        
        job_id = data['job_id']
        candidate_id = data['candidate_id']
        candidate_data = data['candidate_data']
        
        # Validate job_id is integer
        try:
            job_id = int(job_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'job_id must be a valid integer'
            }), 400
        
        # Validate candidate_data is dict
        if not isinstance(candidate_data, dict):
            return jsonify({
                'success': False,
                'error': 'candidate_data must be a dictionary'
            }), 400
        
        # Process assessment
        processor = AssessmentProcessor()
        result = processor.process_min_qualification_assessment(job_id, candidate_id, candidate_data)
        
        if not result['success']:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@min_qualification_bp.route('/preview', methods=['POST'])
def preview_assessment():
    """
    Preview minimum qualification assessment without using AI tokens
    """
    try:
        data = request.get_json()
        
        required_fields = ['job_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: job_id'
            }), 400
        
        job_id = data['job_id']
        
        try:
            job_id = int(job_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'job_id must be a valid integer'
            }), 400
        
        # Get job data and criteria without processing
        processor = AssessmentProcessor()
        
        job_data = processor.fetch_job_data(job_id)
        if not job_data:
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
        
        criteria_data = processor.fetch_job_criteria(job_id)
        if not criteria_data:
            return jsonify({
                'success': False,
                'error': 'Job criteria not found'
            }), 404
        
        min_qual_criteria = criteria_data.get('min_qualification_criteria', [])
        
        return jsonify({
            'success': True,
            'job_data': {
                'id': job_data['id'],
                'title': job_data['title'],
                'description': job_data['description']
            },
            'criteria_count': len(min_qual_criteria),
            'criteria': min_qual_criteria,
            'assessment_type': 'min_qualification'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500