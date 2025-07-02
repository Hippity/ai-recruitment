import { jobManagementApi } from './api.js';

export const jobService = {
  // Get all jobs with optional filters
  async getJobs(entityId = null, status = null) {
    let endpoint = '/api/jobs';
    const params = new URLSearchParams();
    
    if (entityId) params.append('entity_id', entityId);
    if (status) params.append('status', status);
    
    if (params.toString()) {
      endpoint += `?${params.toString()}`;
    }
    
    return jobManagementApi.get(endpoint);
  },

  // Get job by ID
  async getJob(id) {
    return jobManagementApi.get(`/api/jobs/${id}`);
  },

  // Create new job
  async createJob(jobData) {
    return jobManagementApi.post('/api/jobs', jobData);
  },

  // Update job
  async updateJob(id, jobData) {
    return jobManagementApi.put(`/api/jobs/${id}`, jobData);
  },

  // Delete job
  async deleteJob(id) {
    return jobManagementApi.delete(`/api/jobs/${id}`);
  },

  // Get job criteria
  async getJobCriteria(jobId) {
    return jobManagementApi.get(`/api/jobs/${jobId}/criteria`);
  },
};