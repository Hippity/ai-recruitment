import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from services.openai_client import OpenAIClient
from utils.prompts import (
    SYSTEM_PROMPT_MIN_QUALIFICATION,
    SYSTEM_PROMPT_FORMAL_ASSESSMENT
)
from config import Config
from models import UsageTracking
from models.min_qualification_results import MinQualificationResult
from models.formal_assessment_results import FormalAssessmentResult
from utils.database import db

class AssessmentProcessor:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.job_service_url = Config.JOB_MANAGEMENT_SERVICE_URL
    
    def fetch_job_data(self, job_id: int) -> Dict[str, Any]:
        """
        Fetch job data from job management service
        """
        try:
            response = requests.get(f"{self.job_service_url}/api/jobs/{job_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def fetch_job_criteria(self, job_id: int) -> Dict[str, Any]:
        """
        Fetch job criteria from job management service
        """
        try:
            response = requests.get(f"{self.job_service_url}/api/jobs/{job_id}/criteria")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def process_min_qualification_assessment(self, job_id: int, candidate_id: str, candidate_data: dict) -> Dict[str, Any]:
        """
        Process minimum qualification assessment area by area
        """
        start_time = datetime.utcnow()
        
        try:
            # Fetch job criteria
            criteria_data = self.fetch_job_criteria(job_id)
            if not criteria_data:
                return {"success": False, "error": "Failed to fetch job criteria"}
            
            min_qual_criteria = criteria_data.get('min_qualification_criteria', [])
            if not min_qual_criteria:
                return {"success": False, "error": "No minimum qualification criteria found"}
            
            results = []
            overall_pass = True
            
            # Process each area separately
            for criterion in min_qual_criteria:
                area = criterion['area']
                
                # Get candidate data for this specific area
                area_data = self._extract_area_data(candidate_data, area)
                
                # Build area-specific prompt
                prompt = self._build_min_qual_area_prompt(criterion, area_data)
                
                # Generate AI assessment for this area
                ai_response = self.openai_client.generate_completion(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_MIN_QUALIFICATION
                )
                
                if not ai_response["success"]:
                    overall_pass = False
                    continue
                
                content = ai_response["content"]
                result = content.get("result", "FAIL")
                
                # Save result to database
                area_result = MinQualificationResult(
                    job_id=job_id,
                    candidate_id=candidate_id,
                    criteria_id=criterion['id'],
                    area=area,
                    result=result,
                    justification=content.get("justification", ""),
                    evidence_found=content.get("evidence_found", "")
                )
                
                db.session.add(area_result)
                results.append(area_result.to_dict())
                
                if result == "FAIL":
                    overall_pass = False
                
                # Track usage for this area
                if Config.TRACK_USAGE:
                    UsageTracking.log_usage(
                        job_id=job_id,
                        assessment_type="min_qualification",
                        usage_data=ai_response["usage"],
                        success=True,
                        candidate_id=candidate_id
                    )
            
            db.session.commit()
            
            processing_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            return {
                "success": True,
                "assessment_type": "min_qualification",
                "job_id": job_id,
                "candidate_id": candidate_id,
                "overall_result": "PASS" if overall_pass else "FAIL",
                "area_results": results,
                "processing_time_ms": processing_time
            }
            
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def process_formal_assessment(self, job_id: int, candidate_id: str, candidate_data: dict) -> Dict[str, Any]:
        """
        Process formal assessment area by area
        """
        start_time = datetime.utcnow()
        
        try:
            # Fetch job data and criteria
            job_data = self.fetch_job_data(job_id)
            if not job_data:
                return {"success": False, "error": "Failed to fetch job data"}
            
            criteria_data = self.fetch_job_criteria(job_id)
            if not criteria_data:
                return {"success": False, "error": "Failed to fetch job criteria"}
            
            formal_criteria = criteria_data.get('formal_assessment_criteria', [])
            if not formal_criteria:
                return {"success": False, "error": "No formal assessment criteria found"}
            
            results = []
            total_score = 0
            total_max_score = 0
            
            # Process each area separately
            for criterion in formal_criteria:
                area = criterion['area']
                max_score = float(criterion['max_score'])
                
                # Get candidate data for this specific area
                area_data = self._extract_area_data(candidate_data, area)
                
                # Build area-specific prompt (experience needs job description)
                if area.lower() == 'professional experience':
                    prompt = self._build_formal_experience_prompt(criterion, area_data, job_data)
                else:
                    prompt = self._build_formal_area_prompt(criterion, area_data)
                
                # Generate AI assessment for this area
                ai_response = self.openai_client.generate_completion(
                    prompt=prompt,
                    system_prompt=SYSTEM_PROMPT_FORMAL_ASSESSMENT
                )
                
                if not ai_response["success"]:
                    continue
                
                content = ai_response["content"]
                raw_score = min(float(content.get("raw_score", 0)), max_score)
                percentage = (raw_score / max_score * 100) if max_score > 0 else 0
                
                # Save result to database
                area_result = FormalAssessmentResult(
                    job_id=job_id,
                    candidate_id=candidate_id,
                    criteria_id=criterion['id'],
                    area=area,
                    raw_score=raw_score,
                    max_score=max_score,
                    percentage=percentage,
                    evidence=content.get("evidence", ""),
                    justification=content.get("justification", "")
                )
                
                db.session.add(area_result)
                results.append(area_result.to_dict())
                
                total_score += raw_score
                total_max_score += max_score
                
                # Track usage for this area
                if Config.TRACK_USAGE:
                    UsageTracking.log_usage(
                        job_id=job_id,
                        assessment_type="formal_assessment",
                        usage_data=ai_response["usage"],
                        success=True,
                        candidate_id=candidate_id
                    )
            
            db.session.commit()
            
            # Calculate overall score
            overall_percentage = (total_score / total_max_score * 100) if total_max_score > 0 else 0
            grade = self._calculate_grade(overall_percentage)
            
            processing_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            return {
                "success": True,
                "assessment_type": "formal_assessment",
                "job_id": job_id,
                "candidate_id": candidate_id,
                "overall_score": {
                    "total_score": round(total_score, 2),
                    "total_max_score": round(total_max_score, 2),
                    "percentage": round(overall_percentage, 2),
                    "grade": grade
                },
                "area_results": results,
                "processing_time_ms": processing_time
            }
            
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _extract_area_data(self, candidate_data: dict, area: str) -> str:
        """
        Extract relevant data for specific area
        """
        area_lower = area.lower()
        
        if 'personal' in area_lower:
            return candidate_data.get('personal_information', '')
        elif 'address' in area_lower:
            return candidate_data.get('address', '')
        elif 'education' in area_lower:
            return candidate_data.get('education', '')
        elif 'experience' in area_lower:
            return candidate_data.get('professional_experience', '')
        elif 'years' in area_lower:
            return candidate_data.get('years_of_experience', '')
        elif 'computer' in area_lower:
            return candidate_data.get('computer_proficiency', '')
        elif 'public' in area_lower:
            return candidate_data.get('public_sector_employment', '')
        elif 'language' in area_lower:
            return candidate_data.get('language_proficiency', '')
        elif 'skill' in area_lower:
            return candidate_data.get('additional_skills', '')
        elif 'other' in area_lower:
            return candidate_data.get('other_information', '')
        elif 'certification' in area_lower:
            return candidate_data.get('certification_statement', '')
        else:
            return str(candidate_data)
    
    def _build_min_qual_area_prompt(self, criterion: dict, area_data: str) -> str:
        """
        Build prompt for single minimum qualification area
        """
        return f"""
Evaluate if the candidate meets the minimum qualification for this area:

Area: {criterion['area']}
Criteria: {criterion['criteria']}
{f"Additional Info: {criterion['explanation']}" if criterion.get('explanation') else ""}

Candidate Data for this area:
{area_data}

Return JSON:
{{
  "result": "PASS" or "FAIL",
  "justification": "Clear explanation why candidate passes/fails",
  "evidence_found": "Specific evidence from candidate data"
}}
"""
    
    def _build_formal_area_prompt(self, criterion: dict, area_data: str) -> str:
        """
        Build prompt for single formal assessment area
        """
        return f"""
Score the candidate for this area:

Area: {criterion['area']}
Criteria: {criterion['criteria']}
Max Score: {criterion['max_score']}
{f"Additional Info: {criterion['explanation']}" if criterion.get('explanation') else ""}

Candidate Data for this area:
{area_data}

Return JSON:
{{
  "raw_score": 0.00,
  "evidence": "Specific evidence from candidate data",
  "justification": "Detailed explanation for the score"
}}
"""
    
    def _build_formal_experience_prompt(self, criterion: dict, area_data: str, job_data: dict) -> str:
        """
        Build prompt for experience assessment with job description
        """
        return f"""
Score the candidate's experience against the job requirements:

Job Title: {job_data.get('title', '')}
Job Description: {job_data.get('description', '')}

Assessment Area: {criterion['area']}
Criteria: {criterion['criteria']}
Max Score: {criterion['max_score']}
{f"Additional Info: {criterion['explanation']}" if criterion.get('explanation') else ""}

Candidate Experience:
{area_data}

Evaluate how the candidate's experience aligns with the job requirements.

Return JSON:
{{
  "raw_score": 0.00,
  "evidence": "Specific evidence from candidate experience",
  "justification": "Detailed explanation comparing experience to job requirements"
}}
"""
    
    def _calculate_grade(self, percentage: float) -> str:
        """
        Calculate letter grade based on percentage
        """
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"