import { useState, useEffect, useCallback } from 'react';
import { jobService } from '../services/jobService';
import { criteriaService } from '../services/criteriaService';

export const useCriteria = (jobId) => {
  const [criteria, setCriteria] = useState({
    min_qualification_criteria: [],
    formal_assessment_criteria: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCriteria = useCallback(async () => {
    if (!jobId) return;
    
    setLoading(true);
    setError(null);
    try {
      const data = await jobService.getJobCriteria(jobId);
      setCriteria({
        min_qualification_criteria: data.min_qualification_criteria || [],
        formal_assessment_criteria: data.formal_assessment_criteria || [],
      });
    } catch (err) {
      setError(err.message);
      console.error('Error fetching criteria:', err);
    } finally {
      setLoading(false);
    }
  }, [jobId]);

  // Minimum Qualification Criteria
  const createMinQualificationCriteria = useCallback(async (criteriaData) => {
    setError(null);
    try {
      const newCriteria = await criteriaService.createMinQualificationCriteria({
        ...criteriaData,
        job_id: jobId,
      });
      setCriteria(prev => ({
        ...prev,
        min_qualification_criteria: [...prev.min_qualification_criteria, newCriteria],
      }));
      return newCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [jobId]);

  const updateMinQualificationCriteria = useCallback(async (id, criteriaData) => {
    setError(null);
    try {
      const updatedCriteria = await criteriaService.updateMinQualificationCriteria(id, criteriaData);
      setCriteria(prev => ({
        ...prev,
        min_qualification_criteria: prev.min_qualification_criteria.map(
          c => c.id === id ? updatedCriteria : c
        ),
      }));
      return updatedCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const deleteMinQualificationCriteria = useCallback(async (id) => {
    setError(null);
    try {
      await criteriaService.deleteMinQualificationCriteria(id);
      setCriteria(prev => ({
        ...prev,
        min_qualification_criteria: prev.min_qualification_criteria.filter(c => c.id !== id),
      }));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const createBulkMinQualificationCriteria = useCallback(async (criteriaList) => {
    setError(null);
    try {
      const newCriteria = await criteriaService.createBulkMinQualificationCriteria(jobId, criteriaList);
      setCriteria(prev => ({
        ...prev,
        min_qualification_criteria: [...prev.min_qualification_criteria, ...newCriteria],
      }));
      return newCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [jobId]);

  // Formal Assessment Criteria
  const createFormalAssessmentCriteria = useCallback(async (criteriaData) => {
    setError(null);
    try {
      const newCriteria = await criteriaService.createFormalAssessmentCriteria({
        ...criteriaData,
        job_id: jobId,
      });
      setCriteria(prev => ({
        ...prev,
        formal_assessment_criteria: [...prev.formal_assessment_criteria, newCriteria],
      }));
      return newCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [jobId]);

  const updateFormalAssessmentCriteria = useCallback(async (id, criteriaData) => {
    setError(null);
    try {
      const updatedCriteria = await criteriaService.updateFormalAssessmentCriteria(id, criteriaData);
      setCriteria(prev => ({
        ...prev,
        formal_assessment_criteria: prev.formal_assessment_criteria.map(
          c => c.id === id ? updatedCriteria : c
        ),
      }));
      return updatedCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const deleteFormalAssessmentCriteria = useCallback(async (id) => {
    setError(null);
    try {
      await criteriaService.deleteFormalAssessmentCriteria(id);
      setCriteria(prev => ({
        ...prev,
        formal_assessment_criteria: prev.formal_assessment_criteria.filter(c => c.id !== id),
      }));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const createBulkFormalAssessmentCriteria = useCallback(async (criteriaList) => {
    setError(null);
    try {
      const newCriteria = await criteriaService.createBulkFormalAssessmentCriteria(jobId, criteriaList);
      setCriteria(prev => ({
        ...prev,
        formal_assessment_criteria: [...prev.formal_assessment_criteria, ...newCriteria],
      }));
      return newCriteria;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, [jobId]);

  useEffect(() => {
    fetchCriteria();
  }, [fetchCriteria]);

  return {
    criteria,
    loading,
    error,
    fetchCriteria,
    // Min Qualification
    createMinQualificationCriteria,
    updateMinQualificationCriteria,
    deleteMinQualificationCriteria,
    createBulkMinQualificationCriteria,
    // Formal Assessment
    createFormalAssessmentCriteria,
    updateFormalAssessmentCriteria,
    deleteFormalAssessmentCriteria,
    createBulkFormalAssessmentCriteria,
  };
};