import { jobManagementApi } from './api.js';

export const criteriaService = {
  // Minimum Qualification Criteria
  async createMinQualificationCriteria(criteriaData) {
    return jobManagementApi.post('/api/criteria/min-qualification', criteriaData);
  },

  async updateMinQualificationCriteria(id, criteriaData) {
    return jobManagementApi.put(`/api/criteria/min-qualification/${id}`, criteriaData);
  },

  async deleteMinQualificationCriteria(id) {
    return jobManagementApi.delete(`/api/criteria/min-qualification/${id}`);
  },

  async createBulkMinQualificationCriteria(jobId, criteriaList) {
    return jobManagementApi.post('/api/criteria/min-qualification/bulk', {
      job_id: jobId,
      criteria_list: criteriaList,
    });
  },

  // Formal Assessment Criteria
  async createFormalAssessmentCriteria(criteriaData) {
    return jobManagementApi.post('/api/criteria/formal-assessment', criteriaData);
  },

  async updateFormalAssessmentCriteria(id, criteriaData) {
    return jobManagementApi.put(`/api/criteria/formal-assessment/${id}`, criteriaData);
  },

  async deleteFormalAssessmentCriteria(id) {
    return jobManagementApi.delete(`/api/criteria/formal-assessment/${id}`);
  },

  async createBulkFormalAssessmentCriteria(jobId, criteriaList) {
    return jobManagementApi.post('/api/criteria/formal-assessment/bulk', {
      job_id: jobId,
      criteria_list: criteriaList,
    });
  },
};