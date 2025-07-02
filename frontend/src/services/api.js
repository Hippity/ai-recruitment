import axios from 'axios';

// Base configurations for different services
const JOB_MANAGEMENT_BASE_URL = import.meta.env.VITE_JOB_MANAGEMENT_API_URL || 'http://localhost:5003';
const AI_ASSESSMENT_BASE_URL = import.meta.env.VITE_AI_ASSESSMENT_API_URL || 'http://localhost:5004';

// Create axios instances for different services
export const jobManagementApi = axios.create({
  baseURL: JOB_MANAGEMENT_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const aiAssessmentApi = axios.create({
  baseURL: AI_ASSESSMENT_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generic API client for custom base URLs
class ApiClient {
  constructor(baseURL) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        const message = error.response?.data?.error || error.message || 'An error occurred';
        throw new Error(message);
      }
    );
  }

  async get(endpoint) {
    return this.client.get(endpoint);
  }

  async post(endpoint, data) {
    return this.client.post(endpoint, data);
  }

  async put(endpoint, data) {
    return this.client.put(endpoint, data);
  }

  async delete(endpoint) {
    return this.client.delete(endpoint);
  }
}

// Add response interceptors to existing instances
jobManagementApi.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.error || error.message || 'An error occurred';
    throw new Error(message);
  }
);

aiAssessmentApi.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.error || error.message || 'An error occurred';
    throw new Error(message);
  }
);

export { ApiClient };
export default jobManagementApi;