"""
Prompt templates for AI-powered candidate assessment
"""

# System prompts
SYSTEM_PROMPT_MIN_QUALIFICATION = """
You are an expert HR evaluator specializing in candidate pre-screening for recruitment processes. 
Your role is to assess whether candidates meet minimum qualification requirements with high accuracy and fairness.
Always provide structured, objective evaluations based on the provided criteria.
"""

SYSTEM_PROMPT_FORMAL_ASSESSMENT = """
You are a senior HR assessment specialist conducting formal candidate evaluations. 
Your expertise includes scoring candidates across multiple competency areas using standardized rubrics.
Provide detailed, evidence-based assessments that are fair, consistent, and actionable.
"""

# Minimum qualification assessment template
MIN_QUALIFICATION_TEMPLATE = """
**ROLE**
You are evaluating a candidate's eligibility for a position based on minimum qualification criteria.

**TASK**
Determine if the candidate meets each minimum qualification requirement. This is a pass/fail assessment where candidates must meet ALL criteria to proceed.

**JOB INFORMATION**
Job Title: {job_title}
Job Description: {job_description}

**MINIMUM QUALIFICATION CRITERIA**
{criteria_list}

**CANDIDATE INFORMATION**
{candidate_data}

**EVALUATION INSTRUCTIONS**
1. Assess each criterion individually
2. Look for concrete evidence in the candidate's background
3. Be strict but fair - minimum qualifications are non-negotiable
4. Consider equivalent experience where explicitly stated in criteria

**OUTPUT FORMAT**
Return your evaluation as a JSON object with this exact structure:
{{
  "overall_result": "PASS" or "FAIL",
  "criteria_assessments": [
    {{
      "criterion_id": {criterion_id},
      "criterion_area": "{criterion_area}",
      "result": "PASS" or "FAIL",
      "evidence": "Brief explanation of evidence found or missing",
      "recommendation": "Additional notes if needed"
    }}
  ],
  "summary": "Overall assessment summary",
  "recommendation": "PROCEED" or "REJECT"
}}
"""

# Formal assessment template
FORMAL_ASSESSMENT_TEMPLATE = """
**ROLE**
You are conducting a formal assessment of a candidate for a {job_title} position.

**TASK**
Evaluate the candidate across multiple competency areas using the provided scoring rubrics. Provide detailed scores and justifications.

**JOB INFORMATION**
Job Title: {job_title}
Job Description: {job_description}
Cutoff Grade: {cutoff_grade}

**ASSESSMENT CRITERIA**
{criteria_list}

**CANDIDATE INFORMATION**
{candidate_data}

**SCORING INSTRUCTIONS**
1. Evaluate each criterion independently using the provided scale
2. Provide specific evidence from the candidate's background
3. Consider the weight of each criterion in your assessment
4. Be objective and consistent in your scoring approach
5. Look for concrete examples and achievements

**OUTPUT FORMAT**
Return your evaluation as a JSON object with this exact structure:
{{
  "overall_score": {{
    "raw_score": 0.00,
    "weighted_score": 0.00,
    "percentage": 0.00,
    "grade": "A/B/C/D/F"
  }},
  "criteria_scores": [
    {{
      "criterion_id": {criterion_id},
      "criterion_area": "{criterion_area}",
      "raw_score": 0.00,
      "max_score": 0.00,
      "weight": 0.00,
      "weighted_score": 0.00,
      "percentage": 0.00,
      "evidence": "Specific evidence from candidate background",
      "justification": "Detailed explanation for the score"
    }}
  ],
  "strengths": ["Key strengths identified"],
  "areas_for_improvement": ["Areas where candidate could improve"],
  "overall_recommendation": "HIGHLY_RECOMMENDED/RECOMMENDED/ACCEPTABLE/NOT_RECOMMENDED",
  "summary": "Comprehensive assessment summary",
  "meets_cutoff": true/false
}}
"""

# Experience evaluation template (section-specific)
EXPERIENCE_EVALUATION_TEMPLATE = """
**ROLE**
You are an expert HR evaluator assessing candidates for a {job_title} position.

**TASK**
Evaluate the candidate's professional experience based on the job requirements and scoring rubric.

**JOB REQUIREMENTS**
{job_requirements}

**SCORING RUBRIC**
{scoring_rubric}

**CANDIDATE EXPERIENCE**
{candidate_experience}

**EVALUATION CRITERIA**
- Relevance of experience to the role
- Duration and depth of experience
- Level of responsibility and leadership
- Quality of achievements and outcomes
- Progression and career development

**OUTPUT FORMAT**
Return your evaluation as a JSON object:
{{
  "score": [integer based on rubric scale],
  "justification": "Clear explanation for the score",
  "key_evidence": ["Specific examples supporting the score"],
  "experience_highlights": ["Most relevant experience points"],
  "concerns": ["Any gaps or concerns identified"]
}}
"""

def format_criteria_list(criteria, assessment_type="min_qualification"):
    """
    Format criteria list for prompt inclusion
    """
    if assessment_type == "min_qualification":
        formatted = []
        for i, criterion in enumerate(criteria, 1):
            formatted.append(f"{i}. **{criterion['area']}**: {criterion['criteria']}")
            if criterion.get('explanation'):
                formatted.append(f"   Explanation: {criterion['explanation']}")
        return "\n".join(formatted)
    
    elif assessment_type == "formal_assessment":
        formatted = []
        for i, criterion in enumerate(criteria, 1):
            formatted.append(f"{i}. **{criterion['area']}** (Max Score: {criterion['max_score']}, Weight: {criterion['weight']})")
            formatted.append(f"   Criteria: {criterion['criteria']}")
            if criterion.get('explanation'):
                formatted.append(f"   Explanation: {criterion['explanation']}")
            formatted.append("")
        return "\n".join(formatted)
    
    return ""

def build_min_qualification_prompt(job_data, criteria, candidate_data):
    """
    Build complete minimum qualification assessment prompt
    """
    criteria_list = format_criteria_list(criteria, "min_qualification")
    
    return MIN_QUALIFICATION_TEMPLATE.format(
        job_title=job_data.get('title', ''),
        job_description=job_data.get('description', ''),
        criteria_list=criteria_list,
        candidate_data=candidate_data
    )

def build_formal_assessment_prompt(job_data, criteria, candidate_data):
    """
    Build complete formal assessment prompt
    """
    criteria_list = format_criteria_list(criteria, "formal_assessment")
    cutoff_grade = job_data.get('cutoff_grade', 'Not specified')
    
    return FORMAL_ASSESSMENT_TEMPLATE.format(
        job_title=job_data.get('title', ''),
        job_description=job_data.get('description', ''),
        cutoff_grade=cutoff_grade,
        criteria_list=criteria_list,
        candidate_data=candidate_data
    )

def build_experience_evaluation_prompt(job_title, job_requirements, scoring_rubric, candidate_experience):
    """
    Build experience-specific evaluation prompt
    """
    return EXPERIENCE_EVALUATION_TEMPLATE.format(
        job_title=job_title,
        job_requirements=job_requirements,
        scoring_rubric=scoring_rubric,
        candidate_experience=candidate_experience
    )