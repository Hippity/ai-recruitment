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
        required_fields = ['job_id', 'candidate_data']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: job_id, candidate_data'
            }), 400
        
        job_id = data['job_id']
        candidate_data = data['candidate_data']
        
        # Validate job_id is integer
        try:
            job_id = int(job_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'job_id must be a valid integer'
            }), 400
        
        # Validate candidate_data is string and not empty
        if not isinstance(candidate_data, str) or not candidate_data.strip():
            return jsonify({
                'success': False,
                'error': 'candidate_data must be a non-empty string'
            }), 400
        
        # Process assessment
        processor = AssessmentProcessor()
        result = processor.process_min_qualification_assessment(job_id, candidate_data)
        
        if not result['success']:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@min_qualification_bp.route('/batch-assess', methods=['POST'])
def batch_assess_min_qualification():
    """
    Assess multiple candidates against minimum qualification criteria
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_id', 'candidates']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: job_id, candidates'
            }), 400
        
        job_id = data['job_id']
        candidates = data['candidates']
        
        # Validate job_id
        try:
            job_id = int(job_id)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'job_id must be a valid integer'
            }), 400
        
        # Validate candidates array
        if not isinstance(candidates, list) or not candidates:
            return jsonify({
                'success': False,
                'error': 'candidates must be a non-empty array'
            }), 400
        
        # Limit batch size to prevent abuse
        max_batch_size = 10
        if len(candidates) > max_batch_size:
            return jsonify({
                'success': False,
                'error': f'Batch size cannot exceed {max_batch_size} candidates'
            }), 400
        
        # Process each candidate
        processor = AssessmentProcessor()
        results = []
        
        for i, candidate_info in enumerate(candidates):
            # Validate candidate structure
            if not isinstance(candidate_info, dict) or 'candidate_data' not in candidate_info:
                results.append({
                    'candidate_index': i,
                    'success': False,
                    'error': 'Invalid candidate structure - missing candidate_data'
                })
                continue
            
            candidate_data = candidate_info['candidate_data']
            candidate_id = candidate_info.get('candidate_id', f'candidate_{i}')
            
            # Validate candidate_data
            if not isinstance(candidate_data, str) or not candidate_data.strip():
                results.append({
                    'candidate_index': i,
                    'candidate_id': candidate_id,
                    'success': False,
                    'error': 'candidate_data must be a non-empty string'
                })
                continue
            
            # Process assessment
            result = processor.process_min_qualification_assessment(job_id, candidate_data)
            result['candidate_index'] = i
            result['candidate_id'] = candidate_id
            
            results.append(result)
        
        # Calculate summary statistics
        successful_assessments = [r for r in results if r.get('success', False)]
        passed_candidates = [r for r in successful_assessments 
                           if r.get('ai_response', {}).get('overall_result') == 'PASS']
        
        summary = {
            'total_candidates': len(candidates),
            'successful_assessments': len(successful_assessments),
            'passed_candidates': len(passed_candidates),
            'failed_candidates': len(successful_assessments) - len(passed_candidates),
            'processing_errors': len(results) - len(successful_assessments)
        }
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'summary': summary,
            'results': results
        }), 200
        
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