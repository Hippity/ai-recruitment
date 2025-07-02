import { jobManagementApi } from './api.js';

export const entityService = {
  // Get all entities
  async getEntities() {
    return jobManagementApi.get('/api/entities');
  },

  // Get entity by ID
  async getEntity(id) {
    return jobManagementApi.get(`/api/entities/${id}`);
  },

  // Create new entity
  async createEntity(entityData) {
    return jobManagementApi.post('/api/entities', entityData);
  },

  // Update entity
  async updateEntity(id, entityData) {
    return jobManagementApi.put(`/api/entities/${id}`, entityData);
  },

  // Delete entity
  async deleteEntity(id) {
    return jobManagementApi.delete(`/api/entities/${id}`);
  },
};