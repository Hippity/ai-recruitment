import { useState, useEffect, useCallback } from 'react';
import { jobService } from '../services/jobService';

export const useJobs = (entityId = null) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchJobs = useCallback(async (filters = {}) => {
    setLoading(true);
    setError(null);
    try {
      const data = await jobService.getJobs(
        filters.entityId || entityId, 
        filters.status
      );
      setJobs(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  }, [entityId]);

  const getJob = useCallback(async (id) => {
    try {
      return await jobService.getJob(id);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const createJob = useCallback(async (jobData) => {
    setError(null);
    try {
      const newJob = await jobService.createJob(jobData);
      setJobs(prev => [newJob, ...prev]);
      return newJob;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const updateJob = useCallback(async (id, jobData) => {
    setError(null);
    try {
      const updatedJob = await jobService.updateJob(id, jobData);
      setJobs(prev => 
        prev.map(job => job.id === id ? updatedJob : job)
      );
      return updatedJob;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const deleteJob = useCallback(async (id) => {
    setError(null);
    try {
      await jobService.deleteJob(id);
      setJobs(prev => prev.filter(job => job.id !== id));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const getJobCriteria = useCallback(async (jobId) => {
    try {
      return await jobService.getJobCriteria(jobId);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  return {
    jobs,
    loading,
    error,
    fetchJobs,
    getJob,
    createJob,
    updateJob,
    deleteJob,
    getJobCriteria,
  };
};