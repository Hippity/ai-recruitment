from flask import Blueprint, request, jsonify
from services.assessment_processor import AssessmentProcessor

formal_assessment_bp = Blueprint('formal_assessment', __name__)

@formal_assessment_bp.route('/assess', methods=['POST'])
def assess_formal():
    """
    Conduct formal assessment of a candidate using AI scoring
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
        
        # Validate job_id
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
        result = processor.process_formal_assessment(job_id, candidate_id, candidate_data)
        
        if not result['success']:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@formal_assessment_bp.route('/batch-assess', methods=['POST'])
def batch_assess_formal():
    """
    Conduct formal assessment for multiple candidates
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
        
        # Limit batch size
        max_batch_size = 5  # Smaller for formal assessments due to higher token usage
        if len(candidates) > max_batch_size:
            return jsonify({
                'success': False,
                'error': f'Batch size cannot exceed {max_batch_size} candidates for formal assessments'
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
            result = processor.process_formal_assessment(job_id, candidate_data)
            result['candidate_index'] = i
            result['candidate_id'] = candidate_id
            
            results.append(result)
        
        # Calculate summary statistics
        successful_assessments = [r for r in results if r.get('success', False)]
        
        # Analyze results
        grade_distribution = {}
        recommendation_distribution = {}
        scores = []
        
        for result in successful_assessments:
            ai_response = result.get('ai_response', {})
            overall_score = ai_response.get('overall_score', {})
            
            # Grade distribution
            grade = overall_score.get('grade', 'Unknown')
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1
            
            # Recommendation distribution
            recommendation = ai_response.get('overall_recommendation', 'Unknown')
            recommendation_distribution[recommendation] = recommendation_distribution.get(recommendation, 0) + 1
            
            # Score collection
            percentage = overall_score.get('percentage', 0)
            scores.append(percentage)
        
        # Calculate statistics
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        
        summary = {
            'total_candidates': len(candidates),
            'successful_assessments': len(successful_assessments),
            'processing_errors': len(results) - len(successful_assessments),
            'grade_distribution': grade_distribution,
            'recommendation_distribution': recommendation_distribution,
            'score_statistics': {
                'average': round(avg_score, 2),
                'maximum': round(max_score, 2),
                'minimum': round(min_score, 2)
            }
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

@formal_assessment_bp.route('/preview', methods=['POST'])
def preview_formal_assessment():
    """
    Preview formal assessment criteria and scoring structure
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
        
        # Get job data and criteria
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
        
        formal_criteria = criteria_data.get('formal_assessment_criteria', [])
        
        # Calculate total possible scores (no weights)
        total_max_score = sum(float(c.get('max_score', 0)) for c in formal_criteria)
        
        return jsonify({
            'success': True,
            'job_data': {
                'id': job_data['id'],
                'title': job_data['title'],
                'description': job_data['description'],
                'cutoff_grade': job_data.get('cutoff_grade')
            },
            'criteria_count': len(formal_criteria),
            'criteria': formal_criteria,
            'scoring_summary': {
                'total_max_score': round(total_max_score, 2),
                'average_max_score': round(total_max_score / len(formal_criteria) if formal_criteria else 0, 2)
            },
            'assessment_type': 'formal_assessment'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500