import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from services.openai_client import OpenAIClient
from utils.prompts import (
    build_min_qualification_prompt,
    build_formal_assessment_prompt,
    SYSTEM_PROMPT_MIN_QUALIFICATION,
    SYSTEM_PROMPT_FORMAL_ASSESSMENT
)
from config import Config

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
    
    def process_min_qualification_assessment(self, job_id: int, candidate_data: str) -> Dict[str, Any]:
        """
        Process minimum qualification assessment using AI
        """
        try:
            # Fetch job data and criteria
            job_data = self.fetch_job_data(job_id)
            if not job_data:
                return {"success": False, "error": "Failed to fetch job data"}
            
            criteria_data = self.fetch_job_criteria(job_id)
            if not criteria_data:
                return {"success": False, "error": "Failed to fetch job criteria"}
            
            min_qual_criteria = criteria_data.get('min_qualification_criteria', [])
            if not min_qual_criteria:
                return {"success": False, "error": "No minimum qualification criteria found"}
            
            # Build assessment prompt
            prompt = build_min_qualification_prompt(job_data, min_qual_criteria, candidate_data)
            
            # Check token limits
            if not self.openai_client.check_token_limit(prompt, SYSTEM_PROMPT_MIN_QUALIFICATION):
                return {"success": False, "error": "Prompt exceeds token limits"}
            
            # Generate AI assessment
            ai_response = self.openai_client.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT_MIN_QUALIFICATION
            )
            
            if not ai_response["success"]:
                return {"success": False, "error": f"AI processing failed: {ai_response['error']}"}
            
            # Validate response structure
            expected_fields = ["overall_result", "criteria_assessments", "summary", "recommendation"]
            content = ai_response["content"]
            
            if not all(field in content for field in expected_fields):
                return {"success": False, "error": "Invalid AI response structure"}
            
            # Add metadata
            assessment_result = {
                "success": True,
                "assessment_type": "min_qualification",
                "job_id": job_id,
                "timestamp": datetime.utcnow().isoformat(),
                "ai_response": content,
                "usage": ai_response["usage"],
                "model": ai_response["model"]
            }
            
            return assessment_result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_formal_assessment(self, job_id: int, candidate_data: str) -> Dict[str, Any]:
        """
        Process formal assessment using AI
        """
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
            
            # Build assessment prompt
            prompt = build_formal_assessment_prompt(job_data, formal_criteria, candidate_data)
            
            # Check token limits
            if not self.openai_client.check_token_limit(prompt, SYSTEM_PROMPT_FORMAL_ASSESSMENT):
                return {"success": False, "error": "Prompt exceeds token limits"}
            
            # Generate AI assessment
            ai_response = self.openai_client.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT_FORMAL_ASSESSMENT
            )
            
            if not ai_response["success"]:
                return {"success": False, "error": f"AI processing failed: {ai_response['error']}"}
            
            # Validate response structure
            expected_fields = ["overall_score", "criteria_scores", "overall_recommendation", "summary"]
            content = ai_response["content"]
            
            if not all(field in content for field in expected_fields):
                return {"success": False, "error": "Invalid AI response structure"}
            
            # Validate and calculate scores
            validated_result = self._validate_formal_assessment_scores(content, formal_criteria)
            
            # Add metadata
            assessment_result = {
                "success": True,
                "assessment_type": "formal_assessment",
                "job_id": job_id,
                "timestamp": datetime.utcnow().isoformat(),
                "ai_response": validated_result,
                "usage": ai_response["usage"],
                "model": ai_response["model"]
            }
            
            return assessment_result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _validate_formal_assessment_scores(self, ai_content: Dict, criteria: List[Dict]) -> Dict:
        """
        Validate and recalculate scores to ensure accuracy
        """
        try:
            criteria_scores = ai_content.get("criteria_scores", [])
            total_weighted_score = 0
            total_weight = 0
            
            # Recalculate scores based on criteria
            for i, criterion in enumerate(criteria):
                if i < len(criteria_scores):
                    score_data = criteria_scores[i]
                    
                    # Ensure scores are within bounds
                    raw_score = min(float(score_data.get("raw_score", 0)), float(criterion["max_score"]))
                    weight = float(criterion["weight"])
                    max_score = float(criterion["max_score"])
                    
                    # Recalculate derived values
                    percentage = (raw_score / max_score * 100) if max_score > 0 else 0
                    weighted_score = raw_score * weight
                    
                    # Update score data
                    score_data.update({
                        "raw_score": round(raw_score, 2),
                        "max_score": max_score,
                        "weight": weight,
                        "weighted_score": round(weighted_score, 2),
                        "percentage": round(percentage, 2)
                    })
                    
                    total_weighted_score += weighted_score
                    total_weight += weight
            
            # Calculate overall scores
            overall_percentage = (total_weighted_score / (sum(float(c["max_score"]) * float(c["weight"]) for c in criteria)) * 100) if criteria else 0
            
            # Determine grade
            grade = self._calculate_grade(overall_percentage)
            
            # Update overall score
            ai_content["overall_score"] = {
                "raw_score": round(total_weighted_score / total_weight if total_weight > 0 else 0, 2),
                "weighted_score": round(total_weighted_score, 2),
                "percentage": round(overall_percentage, 2),
                "grade": grade
            }
            
            return ai_content
            
        except Exception as e:
            return ai_content
    
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
    
    def process_section_specific_assessment(self, section_type: str, job_data: Dict, 
                                           candidate_data: str, context: Dict = None) -> Dict[str, Any]:
        """
        Process section-specific assessment (e.g., experience, motivation)
        """
        try:
            # This method can be extended for section-specific evaluations
            # For now, it's a placeholder for future enhancements
            
            section_prompts = {
                "experience": self._build_experience_prompt,
                "education": self._build_education_prompt,
                "skills": self._build_skills_prompt,
                "motivation": self._build_motivation_prompt
            }
            
            if section_type not in section_prompts:
                return {"success": False, "error": f"Unknown section type: {section_type}"}
            
            # Build section-specific prompt
            prompt_builder = section_prompts[section_type]
            prompt = prompt_builder(job_data, candidate_data, context)
            
            # Generate assessment
            ai_response = self.openai_client.generate_completion(prompt)
            
            if not ai_response["success"]:
                return {"success": False, "error": f"AI processing failed: {ai_response['error']}"}
            
            return {
                "success": True,
                "section_type": section_type,
                "assessment": ai_response["content"],
                "usage": ai_response["usage"]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _build_experience_prompt(self, job_data: Dict, candidate_data: str, context: Dict = None) -> str:
        """Build experience assessment prompt"""
        return f"""
        Evaluate the candidate's experience for the {job_data.get('title', '')} position.
        
        Job Requirements: {job_data.get('description', '')}
        
        Candidate Experience: {candidate_data}
        
        Provide a detailed assessment of relevance, depth, and alignment.
        """
    
    def _build_education_prompt(self, job_data: Dict, candidate_data: str, context: Dict = None) -> str:
        """Build education assessment prompt"""
        return f"""
        Evaluate the candidate's educational background for the {job_data.get('title', '')} position.
        
        Job Requirements: {job_data.get('description', '')}
        
        Candidate Education: {candidate_data}
        
        Assess the relevance and adequacy of their educational qualifications.
        """
    
    def _build_skills_prompt(self, job_data: Dict, candidate_data: str, context: Dict = None) -> str:
        """Build skills assessment prompt"""
        return f"""
        Evaluate the candidate's skills and competencies for the {job_data.get('title', '')} position.
        
        Job Requirements: {job_data.get('description', '')}
        
        Candidate Skills: {candidate_data}
        
        Assess technical and soft skills alignment with role requirements.
        """
    
    def _build_motivation_prompt(self, job_data: Dict, candidate_data: str, context: Dict = None) -> str:
        """Build motivation assessment prompt"""
        experience_context = context.get('experience_assessment', '') if context else ''
        
        return f"""
        Evaluate the candidate's motivation and fit for the {job_data.get('title', '')} position.
        
        Job Requirements: {job_data.get('description', '')}
        
        Candidate Motivation Statement: {candidate_data}
        
        Experience Context: {experience_context}
        
        Assess their genuine interest, cultural fit, and long-term potential.
        """